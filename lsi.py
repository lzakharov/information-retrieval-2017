import json

from lsi import LSI, TFIDFModel
from utils import process

issue = json.load(open('issue.json'))
articles = issue['articles']
documents = [process(article['abstract_mystem'])
             for article in articles]

query = 'в работа получать'
lsi = LSI(documents, query, model=TFIDFModel)
print(f'{query}: {" ".join(map(str, lsi.process()))}')

query1 = 'условие решение'
lsi1 = LSI(documents, query1, model=TFIDFModel)
print(f'{query1}: {" ".join(map(str, lsi1.process()))}')

query2 = 'линейный уравнение'
lsi2 = LSI(documents, query2, model=TFIDFModel)
print(f'{query2}: {" ".join(map(str, lsi2.process()))}')


