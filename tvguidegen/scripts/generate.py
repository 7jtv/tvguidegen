#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Script XMLTV generator """

if __name__ == "__main__":

  from tvguidegen.model import collections
  from tvguidegen.processors import xmltv

  channels = collections.Channels('channels_fr').getCollection()
  m3uChannels = collections.M3uChannels('channels_m3u').getCollection()

  xmltv.Export(channels,m3uChannels).run()
