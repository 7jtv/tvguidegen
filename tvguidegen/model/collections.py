# -*- coding: utf-8 -*-
from pymongo import MongoClient
try:
    from ..db.settings import MONGO_DATABASE,MONGO_URI
except:
    MONGO_URI = 'mongo001'
    MONGO_DATABASE = 'tvguide'

class Channels(object):

    channels = None
    def __init__(self,collection_name='channels'):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DATABASE]
        self.collection_name = collection_name


    def getCollection(self,criteria={}):
        if self.channels is None:
            self.channels = list(self.db[self.collection_name].find(criteria))
        return self.channels

    #def output(self):
    #    channels = self.getChannels()
    #    for channel in channels:
    #        print "Channel: %s" %  (channel['name'])
    #        for guide in channel['guide']:
    #            print "\t%s %s %s" % (guide['date'].encode('utf-8'), guide['datetime'].encode('utf-8'), guide['title'].encode('utf-8'))

class M3uChannels(object):

    m3uChannels = None

    def __init__(self, collection_name='m3uchannels'):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DATABASE]
        self.collection_name = collection_name


    def getCollection(self,criteria={}):
        if self.m3uChannels is None:
            self.m3uChannels = list(self.db[self.collection_name].find(criteria))
        return self.m3uChannels
