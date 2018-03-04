import json

issue = json.load(open('issue.json'))
ii_mystem = dict()
ii_porter = dict()

for i, article in enumerate(issue['articles']):
    for word in article['abstract_mystem'].split():
        if word in ii_mystem:
            ii_mystem[word]['documents'].add(i)
            ii_mystem[word]['count'] += 1
        else:
            ii_mystem[word] = dict()
            ii_mystem[word]['documents'] = {i}
            ii_mystem[word]['count'] = 1

    for word in article['abstract_porter'].split():
        if word in ii_porter:
            ii_porter[word]['documents'].add(i)
            ii_porter[word]['count'] += 1
        else:
            ii_porter[word] = dict()
            ii_porter[word]['documents'] = {i}
            ii_porter[word]['count'] = 1


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


with open('inverted_index_abstract_mystem.json', 'w') as f:
    json.dump(ii_mystem, f, indent=4, ensure_ascii=False, cls=SetEncoder)

with open('inverted_index_abstract_porter.json', 'w') as f:
    json.dump(ii_porter, f, indent=4, ensure_ascii=False, cls=SetEncoder)
