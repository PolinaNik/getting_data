from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['hh_vacancies']  # database
vacancies = db.vacancies  # collection


# test = vacancies.aggregate([
#     {"$group": {"_id": "$vacancy_link", "count": {"$sum": 1}}},
#     {"$match": {"_id": {"$ne": 'null'}, "count": {"$gt": 1}}},
#     {"$project": {"name": "$_id", "_id": 0}}
# ])


test = vacancies.find({"salary": {"$elemMatch": {"$gt": 400000}}})

for doc in list(test):
    pprint(doc)

"""output

{'_id': ObjectId('620d9613fcd3e289fc560a99'),
 'salary': [None, 450000, 'руб'],
 'vacancy_link': 'https://khabarovsk.hh.ru/vacancy/51004272?from=vacancy_search_list&hhtmFrom=vacancy_search_list&query=python',
 'vacancy_name': 'Python разработчик (AWS)',
 'web_link': 'https://hh.ru'}
 
"""
