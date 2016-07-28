# -*- coding: utf-8 -*-

from lxml import etree

class Export(object):

    def __init__(self,channels,m3uChannels=None):
        self.channels = channels
        self.m3uChannels = m3uChannels

    def run(self,filename="data/xmltv/all.xml",output=False,prettyXml=False):
        # create XML
        tv = etree.Element('tv')
        tv.set("generator-info-name", "Kas-IPTV generator")

        channels = self.channels

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

        s = etree.tostring(tv,xml_declaration=True,encoding='UTf-8', doctype="<!DOCTYPE tv SYSTEM \"xmltv.dtd\">",pretty_print=prettyXml)

        if filename: self.write(s,filename=filename)
        if output: print s
        return s

    def write(self,s,filename='all.xml'):
        # pretty string
        f = open(filename, 'w')
        f.write(s)
        f.close()

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

        for ch in self.m3uChannels:
            if ch['name'] in variations:
                print "*********** M3u name FOUND on variations *********** ====> ++++ %s ++++" % (ch['name'].encode('UTF-8'))
                return [ch['name']] # Return only name found in m3u
            elif ch['name'].upper().replace(' ','') in [v.replace(' ','') for v in variations]:
                print "*********** M3u name FOUND on variations whitout spaces *********** ====> ++++ %s ++++" % (ch['name'].encode('UTF-8'))
                return [ch['name']]

        return variations
