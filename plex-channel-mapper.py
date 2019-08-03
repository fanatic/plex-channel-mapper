#!/usr/local/bin/python
import xml.etree.cElementTree as ET
import sys

if len(sys.argv) != 4:
    print "./plex-channel-mapper.py input.xml output.xml map.xml"
    sys.exit()

inputXml = sys.argv[1]
outputXml = sys.argv[2]
mapXml = sys.argv[3]

# 1. Parse mapping xml into memory

# <map>
#   <mapitem callsign="WHYYDT2" newchannel="12.2" />
#   <mapitem callsign="WHYYDT3" newchannel="11.2" />
#   <mapitem callsign="OWN" newchannel="19.2" />
# </map>
mapping = {}
tree = ET.parse(mapXml)
for mapitem in tree.getroot().findall('mapitem'):
    callsign = mapitem.get('callsign')
    newchannel = mapitem.get('newchannel')
    mapping[callsign] = newchannel

# print(mapping)
# {'OWN': '19.2', 'WHYYDT2': '12.2', 'WHYYDT3': '11.2'}


# 2. Parse input xml, modifying channel as we go

# https://github.com/XMLTV/xmltv/blob/master/xmltv.dtd
tree = ET.parse(inputXml)
for channel in tree.getroot().findall('channel'):
    # Each channel shows one or more display-names
    if len(channel) > 3:
        channelNumber, callsign = channel[1], channel[2]
        # print(channelNumber.text, callsign.text)
        # For example:
        # ('29', '42 WTXFDT3 fcc')
        # ('29', '42 WTXFDT2 fcc')
        # ('29', '42 WTXFDT fcc')
        if callsign.text in mapping:
            channelNumber.text = mapping[callsign.text]


# 3. Write out modified input as output.xml

tree.write(outputXml,encoding="UTF-8",xml_declaration=True)

# Have to hack to add doctype back just in case it matters
with open(outputXml, 'r+') as fd:
    contents = fd.readlines()
    contents.insert(1, "<!DOCTYPE tv SYSTEM \"xmltv.dtd\">\n\n".encode('utf8'))
    fd.seek(0)  # readlines consumes the iterator, so we need to start over
    fd.writelines(contents)  # No need to truncate as we are increasing filesize
