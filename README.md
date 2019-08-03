# plex-channel-mapper.py

This creates unique channel mappings from a xmltv file.

This script takes three arguments:

`./plex-channel-mapper.py input.xml output.xml map.xml`

Run:

```
#!/bin/sh
/root/mc2xml -T $SCHEDULESDIRECT_CREDS -U
./plex-channel-mapper.py xmltv.xml xmltv-parsed.xml map.xml
```
