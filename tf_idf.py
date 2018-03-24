import json
import math
import itertools

from utils import SetEncoder

issue = json.load(open('issue.json'))
articles = issue['articles']
inverted_index_abstract = json.load(open('inverted_index_abstract_mystem.json'))
inverted_index_title = json.load(open('inverted_index_title_mystem.json'))
tf_idf = {}

for word in itertools.chain(inverted_index_abstract, inverted_index_title):
    tf_idf[word] = {}

    if word in inverted_index_abstract:
        tf = inverted_index_abstract[word]['count'] / len(articles)
        idf = math.log(len(articles) / len(inverted_index_abstract[word]['documents']))
        tf_idf[word]['abstract'] = tf * idf
    else:
        tf_idf[word]['abstract'] = 0

    if word in inverted_index_title:
        tf = inverted_index_title[word]['count'] / len(articles)
        idf = math.log(len(articles) / len(inverted_index_title[word]['documents']))
        tf_idf[word]['title'] = tf * idf
    else:
        tf_idf[word]['title'] = 0

    tf_idf[word]['full'] = 0.4 * tf_idf[word].get('abstract') + 0.6 * tf_idf[word].get('title')

with open('tf_idf.json', 'w') as f:
    json.dump(tf_idf, f, sort_keys=True, indent=4, ensure_ascii=False, cls=SetEncoder)

