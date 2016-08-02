# -*- coding: utf-8 -*-
import re
from collections import defaultdict
class Extractor(object):

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
        channel_name = {}
        group = 'all';
        for line in self.lines:
            if line.find(",") > -1 :
                res = re.search('group-title="(.+?)"',line)
                if res:
                    group = res.group(1).lower()

                if not group in channel_name: channel_name[group] = []

                channel_name[group].append(line.split(",")[-1].strip())

        return channel_name
