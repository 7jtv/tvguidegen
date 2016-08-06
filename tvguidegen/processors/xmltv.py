# -*- coding: utf-8 -*-

from lxml import etree
from pytz import timezone
from pytz import utc
from slugify import slugify
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from collections import Counter

class Export(object):

    totals = {
        'channels':0,
        'progs':0,
        'exact_match': 0,
        'variations_match':0,
        'total_match':0,
        'simple_ratio_match':0,
        'partial_ratio_match':0,
        'token_sort_ratio_match':0,
        'token_set_ratio_match':0,
        'process_ratio_match':0,
        'result_frequency_ratio_match':0
    }

    def __init__(self,channels,m3uChannels=None,verbose=False):
        self.channels = channels
        self.m3uChannels = m3uChannels
        self.verbose = verbose

    def run(self,filename="data/xmltv/all.xml",outputXml=False,prettyXml=False,m3u_only=False):
        # create XML
        tv = etree.Element('tv')
        tv.set("generator-info-name", "Kas-IPTV generator")

        channels = self.channels

        for channel in channels:

            if len(slugify(channel['name'])) == 1: continue  # Special case like "E!" channel

            #if channel['name'] != 'BEIN SPORTS 1':
            #    continue

            if self.verbose:
                print '**********************************************************************************************'
                print "Process tv guide for %s" % (channel['name'])

            tz = timezone(channel['timezone'])
            group = 'all'
            groups = channel['groups']
            ch = etree.Element('channel')
            ch.set('id', channel['slug'])

            simple_ratio_res = []
            partial_ratio_res = []
            sort_ratio_res = []
            set_ratio_res = []
            process_ratio_res = []
            variations = self.get_variations(channel,True)

            for group,chGroups in self.m3uChannels.iteritems():

                (groupFound,ratio) = process.extractOne(group, groups)
                if ratio < 92:
                    continue
                if self.verbose: "Process group {}".format(group)
                for c in chGroups:
                    for variation in variations:
                        """
                            Simple ratio
                            This is an approach of exact match.
                            Result is dirty if channel name must have more than 3 words and less than 10 words
                        """
                        ratio = fuzz.ratio(variation,c)
                        simple_ratio_res.append((c,ratio))
                        """
                            Partial ratio
                            Search for substring
                        """
                        ratio = fuzz.partial_ratio(variation,c)
                        partial_ratio_res.append((c,ratio))
                        """
                            Token Sort ratio
                            The token sort approach involves tokenizing the string in question,
                            sorting the tokens alphabetically, and then joining them back into a string.
                        """
                        ratio = fuzz.token_sort_ratio(variation,c)
                        sort_ratio_res.append((c,ratio))
                        """
                            Token Set Ratio
                            The token set approach is similar of token sort, but a little bit more flexible.
                            Here, we tokenize both strings, but instead of immediately sorting and comparing,
                            we split the tokens into two groups: intersection and remainder.
                            We use those sets to build up a comparison string.
                        """
                        ratio = fuzz.token_set_ratio(variation,c)
                        set_ratio_res.append((c,ratio))
                        """
                            Process Ratio
                        """
                        ratio = fuzz.token_set_ratio(variation,c)
                        set_ratio_res.append((c,ratio))


                for variation in variations:
                    tupRes = process.extractOne(variation, self.m3uChannels[group])
                    process_ratio_res.append(tupRes)


            best_simple_ratio = sorted(simple_ratio_res,key=lambda tup: tup[1],reverse=True)[0]
            best_partial_ratio = sorted(partial_ratio_res,key=lambda tup: tup[1],reverse=True)[0]
            best_sort_ratio = sorted(sort_ratio_res,key=lambda tup: tup[1],reverse=True)[0]
            best_set_ratio = sorted(set_ratio_res,key=lambda tup: tup[1],reverse=True)[0]
            best_process_ratio = sorted(process_ratio_res,key=lambda tup: tup[1],reverse=True)[0]

            all_best_ratio = [
                {
                    "type": 'simple_ratio',
                    "name": best_simple_ratio[0],
                    "ratio":best_simple_ratio[1]
                },
                {
                    "type": 'partial_ratio',
                    "name": best_partial_ratio[0],
                    "ratio":best_partial_ratio[1]
                },
                {
                    "type": 'token_sort_ratio',
                    "name": best_sort_ratio[0],
                    "ratio":best_sort_ratio[1]
                },
                {
                    "type": 'token_set_ratio',
                    "name": best_set_ratio[0],
                    "ratio":best_set_ratio[1]
                },
                {
                    "type": 'process_ratio',
                    "name": best_process_ratio[0],
                    "ratio":best_process_ratio[1]
                },

            ]

            display_name = channel['name']

            matched_ratio = 0
            best_last_chance_ratio = None
            matched_names_freq = Counter([n['name'] for n in all_best_ratio])
            for m in matched_names_freq:
                if matched_names_freq[m] >= 3:
                    for n in all_best_ratio:
                        if n['name'] == m:
                            matched_ratio += int(n['ratio'])
                    best_last_chance_ratio = (m,matched_ratio)
                break # break on first elmt


            if best_simple_ratio[1] > 85:
                if self.verbose: print "===== MATCH WITH SIMPLE RATIO ({}) =====".format(best_simple_ratio[1])
                self.append_matched_name(ch,best_simple_ratio,'simple_ratio')
            elif best_partial_ratio[1] > 85 and len(best_partial_ratio[0].split()) == 1: # check if it have one word
                if self.verbose: print "===== MATCH WITH PARTIAL RATIO ONE WORD ({}) =====".format(best_partial_ratio[1])
                self.append_matched_name(ch,best_partial_ratio,'partial_ratio')
            elif best_partial_ratio[1] > 80:
                if self.verbose: print "===== MATCH WITH PARTIAL RATIO ({}) =====".format(best_partial_ratio[1])
                self.append_matched_name(ch,best_partial_ratio,'partial_ratio')
            elif best_process_ratio[1] >= 88:
                if self.verbose: print "===== MATCH WITH FUZZY PROCESSOR ({}) =====".format(best_process_ratio[1])
                self.append_matched_name(ch,best_process_ratio,'process_ratio')
            elif best_sort_ratio[1] > 80:
                if self.verbose: print "===== MATCH WITH SORT RATIO({}) =====".format(best_sort_ratio[1])
                self.append_matched_name(ch,best_sort_ratio,'token_sort_ratio')
            elif best_set_ratio[1] >= 87:
                if self.verbose: print "===== MATCH WITH SET RATIO ({}) =====".format(best_set_ratio[1])
                self.append_matched_name(ch,best_set_ratio,'token_set_ratio')
            elif not best_last_chance_ratio is None and best_last_chance_ratio[1] >  150:  # Last chance
                if self.verbose: print "===== MATCH WITH Result frequency (Last Chance) ({}) =====".format(best_last_chance_ratio[1])
                self.append_matched_name(ch,best_last_chance_ratio,'result_frequency_ratio')
            else:
                if self.verbose: print "Not m3u matching for %s" % (display_name)
                if self.m3uChannels and m3u_only:
                    print 'M3U only option enabled. Channel skipped.'
                    continue;

                self.append_display_name(ch,display_name)

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

                desc = etree.Element('desc')
                desc.text = prog.get('desc','') # Use dict.get to pass default value if key not exist
                programme.append(desc)

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
            print "Simple match: {simple_ratio_match}, Partial match: {partial_ratio_match}, Token Sort Match: {token_sort_ratio_match}, Token Set Match: {token_set_ratio_match}, Process Match: {process_ratio_match},Result Freq: {result_frequency_ratio_match}".format(**self.totals)

        s = etree.tostring(tv,xml_declaration=True,encoding='UTf-8', doctype="<!DOCTYPE tv SYSTEM \"xmltv.dtd\">",pretty_print=prettyXml)

        if filename: self.write(s,filename=filename)
        if outputXml: print s
        return s

    def write(self,s,filename='all.xml'):
        # pretty string
        f = open(filename, 'w')
        f.write(s)
        f.close()

    def append_matched_name(self,node_to_append,tup_ratio,method_name):
        display_name = tup_ratio[0]
        if self.verbose: print "M3U channel {0} name found. METHOD: {1} Value: {2}".format(display_name,method_name,tup_ratio[1])
        if 'simple_ratio' == method_name:
            self.totals['exact_match'] += 1
        else:
            self.totals['variations_match'] += 1
        self.totals['total_match'] += 1
        self.totals[method_name + '_match'] += 1

        self.append_display_name(node_to_append,display_name)

    def append_display_name(self,node_to_append,display_name):
        child = etree.Element('display-name')
        child.text = display_name
        node_to_append.append(child)

    def add_replace_variation(self,s,search,replace,variations):
        if search in s:
            variations.append(s.replace(search,replace))

    # Return alpha-2 code with ISO 3166-1 for variations
    # Can return wrong code too
    def getAlpha2CountryCode(self,countrycode):
        mapping = {
            'gb':['uk'],
            'pl':['cy'],
            'es':['sp']
            }
        if countrycode in mapping:
            return mapping[countrycode]

        return countrycode

    def get_variations(self,channel,addOriginalName=False):
        original_name = channel['name']
        country = channel['country'].lower()
        variations = []

        if not country in original_name.lower():
            variations.append(original_name + country)

        for a2 in self.getAlpha2CountryCode(country):
            if not a2 in original_name.lower():
                variations.append(original_name + a2)

        if original_name.lower().find("HD") == -1 :
            variations.append(original_name + 'HD')
        else:
            variations.append(original_name.replace('HD',''))

        if original_name.find("+") > -1 : # TODO test if it is still necessary
            variations.append(slugify(original_name.replace("+","plus"),separator=""))
            variations.append(slugify(original_name.replace("+",""),separator=""))

        if original_name.find(" ") > -1 :
            variations.append(original_name.replace(' ', ''))

        # TODO create a dictionnary file for variations
        if original_name.lower().find("channel") > -1 :
            variations.append(original_name.lower().replace('channel', 'ch'))

        numbers = {'one':'1','two':'2','three':'3','four':'4','five':'5'}
        for l,n in numbers.iteritems():
            if l in original_name.lower():
                variations.append(original_name.lower().replace(l, n))

        if addOriginalName : variations.append(original_name)
        if self.verbose: print '%d variations generated.' % (len(variations))

        return variations
