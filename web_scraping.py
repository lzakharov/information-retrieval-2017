from lxml import html
import requests
import json


# Get page
site = 'http://www.mathnet.ru'
issue_url = site + '/php/archive.phtml?jrnid=ivm&wshow=issue&year=2013&volume=&volume_alt=&issue=12&issue_alt=&option_lang=rus'
issue_page = requests.get(issue_url)
issue_page.encoding = 'windows-1251'

issue = {'href': issue_url}

# Parse links and titles of articles
issue_tree = html.fromstring(issue_page.text)
issue['articles'] = [{'href': href, 'title': title}
                     for href, title
                     in zip(issue_tree.xpath('//td[@width="90%"]/a[@class="SLink"]/@href'),
                            issue_tree.xpath('//td[@width="90%"]/a[@class="SLink"]/text()'))]

# Parse annotation and keywords for each article
for article in issue['articles']:
    article_url = site + article['href']
    article_page = requests.get(article_url)
    article_page.encoding = 'windows-1251'
    article_tree = html.fromstring(article_page.text)
    article['annotation'] = (list(map(str.strip,
                                      article_tree.xpath("//table//text()"
                                                         "[preceding-sibling::b[contains(text(), 'Аннотация') "
                                                         "and following-sibling::b[1]]][1]"))))
    article['keywords'] = article_tree.xpath("//i[preceding-sibling::b[contains(text(), 'Ключевые')]]/text()")[0][:-1].split(', ')

# Save issue into JSON file
with open('issue.json', 'w') as f:
    json.dump(issue, f, indent=4, ensure_ascii=False)
