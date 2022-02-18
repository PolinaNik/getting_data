from pymongo import MongoClient
from pprint import pprint


client = MongoClient('localhost', 27017)
db = client['hh_vacancies']    # database
vacancies = db.vacancies        # collection


item_details = vacancies.find()

for item in item_details:
    print(item)


# test = vacancies.aggregate([
#     {"$group": {"_id": "$vacancy_link", "count": {"$sum": 1}}},
#     {"$match": {"_id": {"$ne": 'null'}, "count": {"$gt": 1}}},
#     {"$project": {"name": "$_id", "_id": 0}}
# ])


