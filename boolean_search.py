import json


def intersect(a, b):
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


def subtract(a, b):
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


issue = json.load(open('issue.json'))
articles = issue['articles']
inverted_index = json.load(open('inverted_index_abstract_mystem.json'))
query = input()

result = list(range(len(articles)))

for word in query.split():
    negation = word[0] == '-'
    documents = inverted_index[word[1:] if negation else word]['documents']
    if negation:
        documents = subtract(list(range(len(articles))), documents)

    result = intersect(result, documents)

for i in result:
    article = articles[i]
    print('{}, {}'.format(article['title_normal'], article['href']))
