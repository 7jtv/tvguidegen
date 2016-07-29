# -*- coding: utf-8 -*-
from pymongo import MongoClient

class Channels(object):

    channels = None
    def __init__(self,collection_name,mongodb_uri,mongodb_db):
        self.client = MongoClient(mongodb_uri)
        self.db = self.client[mongodb_db]
        self.collection_name = collection_name


    def getCollection(self,criteria={}):
        if self.channels is None:
            self.channels = self.db[self.collection_name].find(criteria)
        return self.channels

    def aggregate(self,criteria):
        return list(self.db[self.collection_name].aggregate(criteria))
    #def output(self):
    #    channels = self.getChannels()
    #    for channel in channels:
    #        print "Channel: %s" %  (channel['name'])
    #        for guide in channel['guide']:
    #            print "\t%s %s %s" % (guide['date'].encode('utf-8'), guide['datetime'].encode('utf-8'), guide['title'].encode('utf-8'))

class M3uChannels(object):

    m3uChannels = None

    def __init__(self, collection_name,mongodb_uri,mongodb_db):
        self.client = MongoClient(mongodb_uri)
        self.db = self.client[mongodb_db]
        self.collection_name = collection_name


    def getCollection(self,criteria={}):
        if self.m3uChannels is None:
            self.m3uChannels = self.db[self.collection_name].find(criteria)
        return self.m3uChannels
