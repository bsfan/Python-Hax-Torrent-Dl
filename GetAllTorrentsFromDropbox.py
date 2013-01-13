# Relased under MIT License

#Copyright (c) 2013 Simon Ramsay

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy,modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#requires the Dropbox SDK 1.5.1
from dropbox import client, rest, session 
from datetime import datetime
import glob

# Get your app key and secret from the Dropbox developer website
APP_KEY = '____________'
APP_SECRET = '_____________'
# ACCESS_TYPE should be 'dropbox' or 'app_folder' as configured for your app
ACCESS_TYPE = '____________'
#where to get/set the auth token
TOKEN_FILE = "______________/token.txt"
#where to put new torrnets (note: use absolute path)
TORRENT_FOLDER = '___________'

class StoredSession(session.DropboxSession):
    """a wrapper around DropboxSession that stores a token to a file on disk"""

    def load_creds(self):
        try:
            stored_creds = open(TOKEN_FILE).read()
            self.set_token(*stored_creds.split('|'))
            print "[loaded access token]"
        except IOError: #program will continue if the file was not found
						pass

    def write_creds(self, token):
        f = open(TOKEN_FILE, 'w')
        f.write("|".join([token.key, token.secret]))
        f.close()

    def link(self):
        request_token = self.obtain_request_token()
        url = self.build_authorize_url(request_token)
        print "url:", url
        print "Please authorize in the browser."
        raw_input()

        self.obtain_access_token(request_token)
        self.write_creds(self.token)


existingTorrents = glob.glob('{0}*.torrent'.format(TORRENT_FOLDER))

sess = StoredSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
sess.load_creds()
if not sess.is_linked():
	sess.link()

client = client.DropboxClient(sess)
folder_metadata = client.metadata('/')
folder = folder_metadata['contents']

for item in folder:
	#only if the file is a .torrent and does not exist on the local machine
	if not item['is_dir'] and item['path'].endswith('.torrent') and existingTorrents.count('{0}{1}'.format(TORRENT_FOLDER,item['path'].replace('/',''))) == 0:
		f, metadata = client.get_file_and_metadata(item['path'])
		out = open('{0}{1}'.format(TORRENT_FOLDER,item['path'].replace('/','')), 'wb')
		out.write(f.read())
		out.close()

