import json
from string import punctuation

issue = json.load(open('issue.json'))
ii_abstract_mystem = dict()
ii_abstract_porter = dict()
ii_title_mystem = dict()
ii_title_porter = dict()


for i, article in enumerate(issue['articles']):
    words = filter(lambda w: w != '–', map(lambda w: w.strip(punctuation), article['abstract_mystem'].split()))
    for word in words:
        if word in ii_abstract_mystem:
            ii_abstract_mystem[word]['documents'].add(i)
            ii_abstract_mystem[word]['count'] += 1
        else:
            ii_abstract_mystem[word] = dict()
            ii_abstract_mystem[word]['documents'] = {i}
            ii_abstract_mystem[word]['count'] = 1

    words = filter(lambda w: w != '–', map(lambda w: w.strip(punctuation), article['abstract_porter'].split()))
    for word in words:
        if word in ii_abstract_porter:
            ii_abstract_porter[word]['documents'].add(i)
            ii_abstract_porter[word]['count'] += 1
        else:
            ii_abstract_porter[word] = dict()
            ii_abstract_porter[word]['documents'] = {i}
            ii_abstract_porter[word]['count'] = 1

    words = filter(lambda w: w != '–', map(lambda w: w.strip(punctuation), article['title_mystem'].split()))
    for word in words:
        if word in ii_title_mystem:
            ii_title_mystem[word]['documents'].add(i)
            ii_title_mystem[word]['count'] += 1
        else:
            ii_title_mystem[word] = dict()
            ii_title_mystem[word]['documents'] = {i}
            ii_title_mystem[word]['count'] = 1

    words = filter(lambda w: w != '–', map(lambda w: w.strip(punctuation), article['title_porter'].split()))
    for word in words:
        if word in ii_title_porter:
            ii_title_porter[word]['documents'].add(i)
            ii_title_porter[word]['count'] += 1
        else:
            ii_title_porter[word] = dict()
            ii_title_porter[word]['documents'] = {i}
            ii_title_porter[word]['count'] = 1


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return sorted(list(obj))
        return json.JSONEncoder.default(self, obj)


with open('inverted_index_abstract_mystem.json', 'w') as f:
    json.dump(ii_abstract_mystem, f, sort_keys=True, indent=4, ensure_ascii=False, cls=SetEncoder)

with open('inverted_index_abstract_porter.json', 'w') as f:
    json.dump(ii_abstract_porter, f, sort_keys=True, indent=4, ensure_ascii=False, cls=SetEncoder)

with open('inverted_index_title_mystem.json', 'w') as f:
    json.dump(ii_title_mystem, f, sort_keys=True, indent=4, ensure_ascii=False, cls=SetEncoder)

with open('inverted_index_title_porter.json', 'w') as f:
    json.dump(ii_title_porter, f, sort_keys=True, indent=4, ensure_ascii=False, cls=SetEncoder)


