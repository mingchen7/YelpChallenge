from pymongo import MongoClient
from datetime import datetime

client = MongoClient()
db = client.test

# INSERT
result = db.restaurants.insert_one(
    {
        "address": {
            "street": "2 Avenue",
            "zipcode": "10075",
            "building": "1480",
            "coord": [-73.9557413, 40.7720266]
        },
        "borough": "Manhattan",
        "cuisine": "Italian",
        "grades": [
            {
                "date": datetime.strptime("2014-10-01", "%Y-%m-%d"),
                "grade": "A",
                "score": 11
            },
            {
                "date": datetime.strptime("2014-01-16", "%Y-%m-%d"),
                "grade": "B",
                "score": 17
            }
        ],
        "name": "Vella",
        "restaurant_id": "41704620"
    }
)

# QUERY
# one condition
cursor = db.restaurants.find({"address.zipcode": "10075"})
# filtering
cursor = db.restaurants.find({"grades.grade": "B"})
# greater than and less than
cursor = db.restaurants.find({"grades.score": {"$gt": 30}})
cursor = db.restaurants.find({"grades.score": {"$lt": 10}})
# combined condition
cursor = db.restaurants.find({"cuisine": "Italian", "address.zipcode": "10075"})
# sort by combined conditions
cursor = db.restaurants.find().sort([
    ("borough", pymongo.ASCENDING),
    ("address.zipcode", pymongo.DESCENDING)
])

for document in cursor:
	print document

