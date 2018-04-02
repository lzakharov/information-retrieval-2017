import json
from typing import List, Dict


class BooleanSearch:
    def __init__(self, inverted_index: Dict, docs_num: int):
        self.inverted_index = inverted_index
        self.docs_num = docs_num

    @staticmethod
    def _intersect(a: List[int], b: List[int]):
        result = []
        i = j = 0

        while i < len(a) and j < len(b):
            if b[j] > a[i]:
                i += 1
            elif b[j] < a[i]:
                j += 1
            else:
                result.append(a[i])
                i += 1
                j += 1

        return result

    @staticmethod
    def _subtract(a: List[int], b: List[int]):
        result = []
        i = j = 0

        while i < len(a) and j < len(b):
            if b[j] > a[i]:
                result.append(a[i])
                i += 1
            elif b[j] < a[i]:
                j += 1
            else:
                i += 1
                j += 1

        return result + a[i:]

    def process(self, query: str):
        result = list(range(len(articles)))

        for word in query.split():
            negation = word[0] == '-'
            docs = self.inverted_index[word[1:] if negation else word]['documents']

            if negation:
                docs = self._subtract(list(range(len(articles))), docs)

            result = self._intersect(result, docs)

        return result


issue = json.load(open('issue.json'))
articles = issue['articles']
inverted_index = json.load(open('inverted_index_abstract_mystem.json'))
query = input()

result = BooleanSearch(inverted_index, len(articles)).process(query)

for i in result:
    article = articles[i]
    print('{}, {}'.format(article['title_normal'], article['href']))
