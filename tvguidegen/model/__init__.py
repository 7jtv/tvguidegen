# -*- coding: utf-8 -*-
from pymongo import MongoClient
try:
    from db.settings import MONGO_DATABASE,MONGO_URI
except:
    MONGO_URI = '127.0.0.1:27017'
    MONGO_DATABASE = 'tvguide'
