# -*- coding: utf-8 -*-

class ExractorM3uChannels(object):

    lines = []

    def __init__(self,filename=None,url=None,str=None):
        if not filename is None:
            with open (filename, "r") as m3u:
                self.lines=m3u.readlines()
        elif not url is None:
            import urllib2
            r = urllib2.urlopen(url)
            if r.getcode() == 200:
                self.lines = r.read().split('\n')
            else:
                raise Exception('Response HTTP returned CODE: %s' % (r.status_code))
        elif not str is None:
            self.lines = str.split('\n')
        else:
            raise Exception("Need one argument at least: file,url or str")

        if len(self.lines) < 1:
            raise Exception("No m3u content found")


    def extract(self):
        for line in self.lines:
            if line.find(",") > -1 :
                channel_name = {'name':line.split(",")[-1].strip()}
                yield channel_name

import pymongo
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

extractor = ExractorM3uChannels("m3u/list.m3u.sample")
#for ch in extractor.extract():
#    print ch
try:
    from db_settings import MONGO_DATABASE,MONGO_URI
except:
    MONGO_URI = '127.0.0.1:27017'
    MONGO_DATABASE = 'tvguide'
ImportM3uChannels(MONGO_URI,MONGO_DATABASE).importM3u(extractor.extract())
