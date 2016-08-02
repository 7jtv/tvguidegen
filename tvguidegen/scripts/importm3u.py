#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo,sys
from m3u.tools import Exractor
class ImportM3uChannels(object):

    def __init__(self, mongo_uri, mongo_db,collection_name='channels_m3u'):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection_name = collection_name

    def importM3u(self,channels):
        #for ch in channels:
        self.db[self.collection_name].drop()
        self.db[self.collection_name].insert(channels)

if __name__ == '__main__':
    extractor = Exractor("data/m3u/list.m3u.sample")

    mongo_uri = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'
    mongo_db = sys.argv[2] if len(sys.argv) > 2 else 'tvguide'
    mongo_collection = sys.argv[3] if len(sys.argv) > 3 else 'channels_m3u'
    ImportM3uChannels(mongo_uri,mongo_db,mongo_collection).importM3u(extractor.extract())
