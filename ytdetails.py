# Sample Python code for user authorization

import httplib2
import os
import sys
import time
import myutil
import config

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

### BEGIN YOUTUBE BOILERPLATE CODE

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = config.videotato_config['client_secret_filename']
STORAGE_FILE = config.videotato_config['storage_filename']

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = "WARNING: Please configure OAuth 2.0"

# Authorize the request and store authorization credentials.
def get_authenticated_service(args):
    flow = flow_from_clientsecrets( CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SSL_SCOPE, message = MISSING_CLIENT_SECRETS_MESSAGE )
    storage = Storage( STORAGE_FILE )
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, args)

    # Trusted testers can download this discovery document from the developers page
    # and it should be in the same directory with the code.
    return build(API_SERVICE_NAME, API_VERSION, http=credentials.authorize(httplib2.Http()))

args = argparser.parse_args()
service = get_authenticated_service(args)

### END YOUTUBE BOILERPLATE CODE

def videoDetails(outFile, service, **kwargs):
    results = service.videos().list(**kwargs).execute()

    for result in results['items']:
        if ( 'contentDetails' in result ):
            try:
                outString = result['id']
                outString += ','
                outString += result['contentDetails']['duration']
                outString += ','
                outString += result['snippet']['publishedAt']
                outString += ','
                outString += result['snippet']['title'].encode('ascii', 'ignore').replace(",", "" )
                outString += '\n'
                outFile.write( outString )
            except:
                print( "Failed on video: %s" % result['snippet']['title'] )
    #print('Got a result! ID: %s', results['items'][0]['contentDetails']['upload']['videoId'] )

def doWork(whichList, whichFolder):
    for channel in whichList:
        print("### Getting full list of videos for %s\n" % channel)
        if ( os.path.isfile( "{0}/{1}.items".format(whichFolder, channel) ) ):
            out_file = open( "{0}/{1}.details".format(whichFolder, channel), "a")
            with open( "{0}/{1}.items".format(whichFolder, channel), "r") as ins:
                counter = 0
                batchString = ''
                for line in ins:
                    batchString += line
                    batchString += ','
                    counter += 1
                    if (counter >= 49):
                        videoDetails(out_file, service, part='snippet,contentDetails', id=batchString, fields='items(contentDetails/duration,id,snippet/publishedAt,snippet/title)')
                        counter = 0
                        batchString = ''
            if ( counter > 0 ):
                videoDetails(out_file, service, part='snippet,contentDetails', id=batchString, fields='items(contentDetails/duration,id,snippet/publishedAt,snippet/title)')
            out_file.close()
        else:
            print( "No items file for item %s\n" % channel )

CHANNELS = []
myutil.readInputFile( "channels.txt", CHANNELS )
PLAYLISTS = []
myutil.readInputFile( "playlists.txt", PLAYLISTS )
print ("--------------Doing channels--------------")
doWork(CHANNELS, "channel_data")
print ("--------------Doing playlists--------------")
doWork(PLAYLISTS, "playlist_data")