#File to test MongoDB
import pymongo
from pymongo import MongoClient
import json
from pprint import pprint


client = MongoClient()
db = client.test
users = db.users
passwords = db.passwords







print "Passwords Collection:"
for w in passwords.find():
    pprint(w)
    print "\n"
print "Users collections"
for u in users.find():
    pprint(u)
    print "\n"


