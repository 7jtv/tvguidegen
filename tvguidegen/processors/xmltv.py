# -*- coding: utf-8 -*-

from lxml import etree
from pytz import timezone
from pytz import utc
from slugify import slugify

class Export(object):

    totals = {'channels':0,'progs':0,'exact_match': 0,'variations_match':0,'total_match':0}

    def __init__(self,channels,m3uChannels=None,verbose=False):
        self.channels = channels
        self.m3uChannels = m3uChannels
        self.verbose = verbose

    def run(self,filename="data/xmltv/all.xml",outputXml=False,prettyXml=False):
        # create XML
        tv = etree.Element('tv')
        tv.set("generator-info-name", "Kas-IPTV generator")

        channels = self.channels

        for channel in channels:

            if self.verbose:
                print '**********************************************************************************************'
                print "Process tv guide for %s" % (channel['name'])

            tz = timezone(channel['timezone'])
            ch = etree.Element('channel')
            ch.set('id', channel['slug'])

            # Try exact match
            exactMatched = False

            for idx,ex in enumerate([slugify(c['name'],separator="") == slugify(channel['name'],separator="").encode('utf-8') for c in self.m3uChannels]):
                if ex:
                    if self.verbose: print "M3U channel %s name found. METHOD: Exact matching" % (self.m3uChannels[idx]['name'].encode('UTF-8'))
                    display_name_variations = [self.m3uChannels[idx]['name']]
                    exactMatched = True
                    self.totals['exact_match'] += 1
                    self.totals['total_match'] += 1
                    break

            if not exactMatched:
                display_name_variations = self.get_variations(channel,True)

            if self.verbose and len(display_name_variations) > 1 and self.m3uChannels:
                print "Not m3u matching for %s" % (channel['name'])

            for dnv in display_name_variations:
                display_name = etree.Element('display-name')
                display_name.text = dnv
                ch.append(display_name)


            icon = etree.Element('icon')
            icon.set('src',channel['logo'])
            ch.append(icon)

            tv.append(ch)

            l_prog = len(channel['guide'])
            if self.verbose: print '%d programmation(s) found.' % (l_prog)
            for idx_prog, prog in enumerate(channel['guide']):

                stop = ''
                if idx_prog < (l_prog - 1):
                    stop =  utc.localize(channel['guide'][idx_prog + 1]['datetime']).astimezone(tz).strftime('%Y%m%d%H%M%S %z')

                programme = etree.Element('programme')
                programme.set('start',utc.localize(prog['datetime']).astimezone(tz).strftime('%Y%m%d%H%M%S %z'))
                programme.set('stop',stop)
                programme.set('channel',channel['slug'])

                title = etree.Element('title')
                title.text = prog['title']
                programme.append(title)

                country = etree.Element('country')
                country.text = channel['country']

                date = etree.Element('date')
                date.text = prog['datetime'].strftime('%Y%m%d')
                programme.append(date)

                tv.append(programme)
                self.totals['progs'] += 1

            self.totals['channels'] += 1
            if self.verbose: print '**********************************************************************************************'

        if self.verbose:
            print "{channels} channels, {progs} programmations, {total_match} m3u channels matched (exact match: {exact_match}, variations match: {variations_match})".format(**self.totals)

        s = etree.tostring(tv,xml_declaration=True,encoding='UTf-8', doctype="<!DOCTYPE tv SYSTEM \"xmltv.dtd\">",pretty_print=prettyXml)

        if filename: self.write(s,filename=filename)
        if outputXml: print s
        return s

    def write(self,s,filename='all.xml'):
        # pretty string
        f = open(filename, 'w')
        f.write(s)
        f.close()

    def add_replace_variation(self,s,search,replace,variations):
        if search in s:
            variations.append(s.replace(search,replace))

    def get_variations(self,channel,addOriginalName=False):
        original_name = channel['name']
        #name_no_spaces = original_name.replace(' ','')
        slug = slugify(original_name,separator="")
        variations = []
        base_variations = [
            slug,
            slug + "hd",
            slug + channel['country'].lower(),
        ]

        if original_name.find("+") > -1 :
            base_variations.append(slugify(original_name.replace("+","plus"),separator=""))
            base_variations.append(slugify(original_name.replace("+",""),separator=""))

        for bv in base_variations:
            variations.append(bv)
            self.add_replace_variation(bv,'channel', 'ch',variations)
            self.add_replace_variation(bv,'premier', 'premiere',variations)
            self.add_replace_variation(bv,'nickelodeon', 'nikolodeon',variations)
            self.add_replace_variation(bv,'planete','planet',variations)
            self.add_replace_variation(bv,'mangas','manga',variations)
            self.add_replace_variation(bv,'nationalgeo','natgeo',variations)
            self.add_replace_variation(bv,'scienceetvietv','sciences',variations)
            self.add_replace_variation(bv,'d8','direct8',variations)
            self.add_replace_variation(bv,"lequipe21",'equipe21',variations)
            self.add_replace_variation(bv,'foot2424','footplus',variations)
            self.add_replace_variation(bv,"golf",'golfchannelfr',variations)
            self.add_replace_variation(bv,"equidialife",'equidia',variations)
            self.add_replace_variation(bv,"eurosport1",'eurosport',variations)


        if addOriginalName : variations.append(original_name)
        if self.verbose: print '%d variations generated.' % (len(variations))

        for ch in self.m3uChannels:
            if slugify(ch['name'],separator="") in [v.encode('utf-8') for v in variations]:
                if self.verbose: print "M3U channel %s name found. METHOD: Variations matching" % (ch['name'].encode('UTF-8'))
                self.totals['variations_match'] += 1
                self.totals['total_match'] += 1
                return [ch['name']] # Return only name found in m3u



        return variations
