# TV GUIDE Generator

Python script used to generate tv guide in many formats


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
