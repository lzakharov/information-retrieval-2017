from lxml import html
import requests
import json
from pymystem3 import Mystem

from porter_stemmer import Porter

# Get page
site = 'http://www.mathnet.ru'
issue_url = site + '/php/archive.phtml?jrnid=ivm&wshow=issue&year=2013&volume=&volume_alt=&issue=12&issue_alt=&option_lang=rus'
issue_page = requests.get(issue_url)
issue_page.encoding = 'windows-1251'

issue = {'href': issue_url, 'articles': []}

# Parse links and titles of articles
issue_tree = html.fromstring(issue_page.text)
for article in issue_tree.xpath('//td[@width="90%"]/a[@class="SLink"]'):
    title_normal = ''.join(article.xpath('descendant-or-self::text()'))
    # Stem title using Porter algorithm
    title_porter = ' '.join((map(Porter.stem, title_normal.split())))
    # Stem title using Mystem module
    title_mystem = ''.join(Mystem().lemmatize(title_normal)).strip()
    href, = article.xpath('@href')
    issue['articles'].append({'href': site + href,
                              'title_normal': title_normal,
                              'title_porter': title_porter,
                              'title_mystem': title_mystem})

# Parse annotation and keywords for each article
for article in issue['articles']:
    article_url = article['href']
    article_page = requests.get(article_url)
    article_page.encoding = 'windows-1251'
    article_tree = html.fromstring(article_page.text)

    abstract = ''.join(article_tree.xpath("//table//text()[preceding-sibling::b[contains(text(), 'Аннотация') "
                                          "and following-sibling::b[1]]][1]/descendant-or-self::text()")).strip()
    article['abstract_normal'] = abstract
    # Stem title using Porter algorithm
    article['abstract_porter'] = ' '.join(map(Porter.stem, article['abstract_normal'].split(' ')))
    # Stem title using Mystem module
    article['abstract_mystem'] = ''.join(Mystem().lemmatize(article['abstract_normal'])).strip()
    keywords = ' '.join(article_tree.xpath("//i[preceding-sibling::b[contains(text(), 'Ключевые')]]/"
                                          "descendant-or-self::text()"))
    article['keywords'] = list(map(str.strip, keywords.split(', ')))

# Save issue into JSON file
with open('issue.json', 'w') as f:
    json.dump(issue, f, indent=4, ensure_ascii=False)
