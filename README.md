Python-Hax-Torrent-Dl
=====================
This is a small Python script to download all new .torrent files from the app root directory of a user's Dropbox account. It is intended to be run as a cron and have the files saved to a directory being activily watched by a torrent
client (http://nexus-rage-quit.blogspot.com/2013/01/turn-arm-linux-headless-server-into.html).


Why
---
Currently there is no direct Dropbox support for ARM Linux, so a small hack was needed.


Required
--------
python 2.7
Dropbox Python SDK 1.5.1 (https://www.dropbox.com/developers_beta/reference/sdk)
setuptools 0.6c11 (http://pypi.python.org/pypi/setuptools/0.6c11)
Registered development app key + secret key from Dropbox


