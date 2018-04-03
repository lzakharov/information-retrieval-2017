import json
import string

import math

from boolean_search import BooleanSearch
from utils import SetEncoder


class TFIDF:
    def __init__(self, documents, words):
        self.documents = documents
        self.words = words

    def calculate(self):
        tf_idf = {}

        for word in self.words:
            tf_idf[word] = []
            documents = self.documents
            title_count = sum(1 for d in documents if word in d['title'])
            title_idf = math.log(len(documents) / title_count) if title_count else 0
            abstract_count = sum(1 for d in documents if word in d['abstract'])
            abstract_idf = math.log(len(documents) / abstract_count) if abstract_count else 0
            for i, document in enumerate(documents):
                title = document['title']
                abstract = document['abstract']
                if word in title or word in abstract:
                    tf_idf[word].append({
                        'document_id': i,
                        'title': (title.count(word) / len(title)) * title_idf,
                        'abstract': (abstract.count(word) / len(abstract)) * abstract_idf
                    })

                    tf_idf[word][-1]['full'] = (0.4 * tf_idf[word][-1].get('abstract') +
                                                0.6 * tf_idf[word][-1].get('title'))

        return tf_idf


def process(text):
    return text.replace(string.punctuation, ' ').replace('\xa0', ' ').split()


def score(query, result, tf_idf):
    for d in result:
        score = 0
        for word in query.split():
            try:
                score += [x['full']
                          for x in tf_idf[word]
                          if x['document_id'] == d][0]
            except IndexError:
                score += 0

        print(f'Документ {d}: {score}')


issue = json.load(open('issue.json'))
articles = issue['articles']
documents = [{'title': process(article['title_mystem']),
              'abstract': process(article['abstract_mystem'])}
             for article in articles]

inverted_index = json.load(open('inverted_index_abstract_mystem.json'))
abstract = set(json.load(open('inverted_index_abstract_mystem.json')).keys())
title = set(json.load(open('inverted_index_title_mystem.json')).keys())
words = sorted(abstract | title)

tf_idf = TFIDF(documents, words).calculate()
with open('tf_idf.json', 'w') as f:
    json.dump(tf_idf, f, sort_keys=True, indent=4, ensure_ascii=False, cls=SetEncoder)

query = input()
result = BooleanSearch(inverted_index, len(articles)).process(query)
score(query, result, tf_idf)
