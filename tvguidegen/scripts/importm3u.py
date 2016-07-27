# -*- coding: utf-8 -*-

import pymongo
from m3u.tools import Exractor
class ImportM3uChannels(object):

    collection_name = 'channels_m3u'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def importM3u(self,channels):
        #for ch in channels:
        self.db[self.collection_name].drop()
        self.db[self.collection_name].insert(channels)

extractor = Exractor("data/m3u/list.m3u.sample")
#for ch in extractor.extract():
#    print ch
try:
    from db_settings import MONGO_DATABASE,MONGO_URI
except:
    MONGO_URI = '127.0.0.1:27017'
    MONGO_DATABASE = 'tvguide'
ImportM3uChannels(MONGO_URI,MONGO_DATABASE).importM3u(extractor.extract())
