# TV GUIDE Generator

Python script used to generate tv guide in many formats

## Requirement
+ Python 2.7
+ pip ans setuptools
+ lxml

## Installation

The installation steps assume that you have the following things installed:
+ Python 2.7
+ pip and setuptools Python packages. Nowadays pip requires and installs setuptools if not installed. Python 2.7.9 and later include pip by default, so you may have it already.
+ lxml. Most Linux distributions ships prepackaged versions of lxml. Otherwise refer to http://lxml.de/installation.html

You can install Tvguidegen using pip (which is the canonical way to install Python packages). To install using pip run:

`pip install tvguidegen`

## Supported Formats
+ [XMLTV](http://wiki.xmltv.org/index.php/XMLTVProject) format. see [DTD](http://xmltv.cvs.sourceforge.net/viewvc/xmltv/xmltv/xmltv.dtd).


## Typical usage

+ With JSON file source:

  `~# tvguidegen -o <outputfile> -c /data/tvguide.json --m3uchannels=/data/mym3uchannels.json`

+ With mongodb collection source:

  `~# tvguidegen -o <outputfile> -c channels_collection --m3uchannels=m3uCahnnels_collection --mongodb-uri=localhost --mongodb-db=tvguide --limit=50`

### Command Line Arguments
```
-o, --output      Output filename

-c, --channels    Filename path with Channels and TV programing content in JSON format
                  or a Mongodb collection name.

--m3uchannels     Filename path with your channels names (Eg. From m3u playlist) in JSON format
                  or a Mongodb collection name.(Optionnal)

--mongodb-uri     Mongodb HOST URI.(Optionnal)
                  If is set,--channels and --m3u-channels are selected from Mongodb\s collections
                  Default: 127.0.0.1

--mongodb-db      Mongodb DATABASE Name. (Optionnal)
                  Default: tvguide

-l, --limit       Limit channels to generate. (Optionnal)

-v                Verbose script execution. (Optionnal)
```

### LICENCE

The MIT License (MIT)
