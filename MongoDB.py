import pymongo
from pymongo import MongoClient

client = MongoClient()
db = client.test
users = db.users



user = raw_input("What is your name: ")
pin = raw_input("Enter a pin code: ")
post = users.insert_one({
    "name": user,
    "pincode": pin

})


for doc in users.find_one({"name": "Youssef"},{"_id":0}):
    print doc




