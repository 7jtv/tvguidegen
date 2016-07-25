# -*- coding: utf-8 -*-

import pymongo
from lxml import etree

class GenerateXmltv(object):

    collection_name = 'channels_fr'
    m3uChannels = None
    channels = None
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]


    def getChannels(self):
        if self.channels is None:
            #self.channels = self.db[self.collection_name].find({'name': {"$regex": '.*13EME.*'}})
            self.channels = self.db[self.collection_name].find()
        return self.channels

    def getM3uChannels(self):
        if self.m3uChannels is None:
            self.m3uChannels = list(self.db['channels_m3u'].find())
        return self.m3uChannels

    def output(self):
        channels = self.getChannels()
        for channel in channels:
            print "Channel: %s" %  (channel['name'])
            for guide in channel['guide']:
                print "\t%s %s %s" % (guide['date'].encode('utf-8'), guide['datetime'].encode('utf-8'), guide['title'].encode('utf-8'))

    def display_name_variations(self,channel,addOriginalName=False):

        original_name = channel['name']
        variations = []

        base_variations = [
            original_name.title(),# Capitalize all words
            original_name.lower(),# To lowercase
            original_name.upper(),# To uppercase
            original_name.lower().capitalize(),# To Capitalize first word
        ]
        tmp = []
        for bv in base_variations:

            #Replace "-" by space and nothing
            if '-' in bv:
                tmp.append(bv.replace('-',' '))
                tmp.append(bv.replace('-',''))
            #Upper case the first word, if they are more than 1 word
            if ' ' in bv:
                tmp.append(bv.replace(' ','')) # remove all spaces
                words = bv.split(' ')
                tmp.append(bv.replace(words[0],words[0].upper())) # Upper case for the first word

            # Add space between string and digit character
            bvSpaceDigit = ''
            for idx,s in enumerate(bv):
                if s.isdigit() and idx > 0 and bv[idx - 1] != ' ':
                    bvSpaceDigit += ' ' + s
                else:
                    bvSpaceDigit += s
            if len(bvSpaceDigit) != len(bv) : # check if are changes in length
                tmp.append(bvSpaceDigit)

            # abrev channel word for paramount
            tmp.append(bv.replace('channel', 'ch'))
            tmp.append(bv.replace('channel', 'Ch'))
            tmp.append(bv.replace('channel', 'CH'))
            tmp.append(bv.replace('channel', 'ch.'))
            tmp.append(bv.replace('channel', 'Ch.'))
            tmp.append(bv.replace('channel', 'CH.'))
            # change Specific to my m3u
            tmp.append(bv.replace('Premier', 'Premiere'))
            tmp.append(bv.replace('Nickelodeon','Nikolodeon'))
            tmp.append(bv.replace('Planete','Planet'))
            tmp.append(bv.replace('Planete+ A&E','Planet+ AE'))
            tmp.append(bv.replace('NATIONAL GEO','NAT GEO'))
            tmp.append(bv.replace('SCIENCE ET VIE TV','Sciences'))
            tmp.append(bv.replace('D8','Direct 8'))
            tmp.append(bv.replace("L'EQUIPE 21",'Equipe 21'))
            tmp.append(bv.replace("MANGAS",'MANGA'))
            tmp.append(bv.replace("FOOT+ 24/24",'Foot +'))
            tmp.append(bv.replace("GOLF+",'Golf Channel FR'))
            if len(bv.split()) == 1:
                tmp.append(bv.replace("EQUIDIA LIFE",'Equidia'))
                tmp.append(bv.replace("EUROSPORT 1",'EuroSport'))

        base_variations += tmp

        for bv in base_variations:
            variations.append(bv)

            variations.append(bv + " HD") # Add HD to string's end
            variations.append(bv + " " + channel['country'].upper()) # Add country upper case to string's end
            variations.append(bv + " " + channel['country'].lower()) # Add country upper case to string's end

            if original_name.find("+") > -1 :
                variations.append(bv.replace("+",""))
                variations.append(bv.replace(" +",""))
                variations.append(bv.replace("+"," plus"))
                variations.append(bv.replace("+"," Plus"))

            #variations.append(bv)

        if addOriginalName : variations.append(original_name)

        for ch in self.getM3uChannels():
            if ch['name'] in variations:
                print "*********** M3u name FOUND on variations *********** ====> ++++ %s ++++" % (ch['name'].encode('UTF-8'))
                return [ch['name']] # Return only name found in m3u
            elif ch['name'].upper().replace(' ','') in [v.replace(' ','') for v in variations]:
                print "*********** M3u name FOUND on variations whitout spaces *********** ====> ++++ %s ++++" % (ch['name'].encode('UTF-8'))
                return [ch['name']]

        return variations



    def generate(self):
        # create XML
        tv = etree.Element('tv')
        tv.set("generator-info-name", "Kas-IPTV generator")

        channels = self.getChannels()

        #for n in self.m3uNames:
        #    print "m3uName: %s" % (n['name'].encode('UTF-8'))
        for channel in channels:
            ch = etree.Element('channel')
            ch.set('id', channel['slug'])

            display_name_variations = self.display_name_variations(channel,True)
            for dnv in display_name_variations:
                display_name = etree.Element('display-name')
                display_name.text = dnv
                ch.append(display_name)


            icon = etree.Element('icon')
            icon.set('src',channel['logo'])
            ch.append(icon)

            tv.append(ch)

            l_prog = len(channel['guide'])
            for idx_prog, prog in enumerate(channel['guide']):

                stop = ''
                if idx_prog < (l_prog - 1):
                    stop =  channel['guide'][idx_prog + 1]['datetime']

                programme = etree.Element('programme')
                programme.set('start',prog['datetime'])
                programme.set('stop',stop)
                programme.set('channel',channel['slug'])

                title = etree.Element('title')
                title.text = prog['title']
                programme.append(title)

                country = etree.Element('country')
                country.text = channel['country']

                date = etree.Element('date')
                date.text = prog['date']
                programme.append(date)

                tv.append(programme)

        # pretty string
        s = etree.tostring(tv,xml_declaration=True,encoding='UTf-8', doctype="<!DOCTYPE tv SYSTEM \"xmltv.dtd\">",pretty_print=False)
        f = open('data/xmltv_canalsat.xml', 'w')
        f.write(s)
        f.close()

        #print s
try:
    from db_settings import MONGO_DATABASE,MONGO_URI
except:
    MONGO_URI = '127.0.0.1:27017'
    MONGO_DATABASE = 'tvguide'
g = GenerateXmltv(MONGO_URI,MONGO_DATABASE)
g.generate()
