import os
import sys
import time
import myutil
import httplib2
import config

from datetime import datetime
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

# Use later when there's a beginning date
def activities_list_for_channelid(service, **kwargs):
    results = service.activities().list(**kwargs).execute()

    #print results
    while True:
        for result in results['items']:
            if ( 'contentDetails' in result ):
                VIDEOS.append( result['contentDetails']['upload']['videoId'] )
        print ("Found %i videos!\n" % len( VIDEOS ))
        if ( 'nextPageToken' in results ):
            kwargs['pageToken'] = results['nextPageToken']
            results = service.activities().list(**kwargs).execute()
        else:
            break;
    #print('Got a result! ID: %s', results['items'][0]['contentDetails']['upload']['videoId'] )


def playlistitems_for_playlistid(service, **kwargs):
    results = service.playlistItems().list(**kwargs).execute()

    while True:
        for result in results['items']:
            if ( 'contentDetails' in result ):
                VIDEOS.append( result['contentDetails']['videoId'] )
        print ("Found %i videos!\n" % len( VIDEOS ))
        if ( 'nextPageToken' in results ):
            kwargs['pageToken'] = results['nextPageToken']
            results = service.playlistItems().list(**kwargs).execute()
        else:
            break;
    #print('Got a result! ID: %s', results['items'][0]['contentDetails']['upload']['videoId'] )


# Process data from channels.txt
def processChannels():
    print( "################# Processing Channels ##################" )
    if ( not os.path.isdir( "channel_data" ) ):
        os.makedirs( "channel_data" )
    for channel in CHANNELS:
        # Check to see if the channel data has been grabbed at some point already
        # If it has, use the time in the .time file in order to get only the activity since the full list was retrieved.
        if ( os.path.isfile( "channel_data/%s.time" % channel ) ):
            print("### Getting delta list of videos for %s\n" % channel)
            timeFile = open("channel_data/%s.time" % channel, "r")
            timestamp = timeFile.read()
            timeFile.close()
            activities_list_for_channelid(service, part='contentDetails', channelId=channel, maxResults=50, publishedAfter=timestamp + 'Z', fields="nextPageToken,items(contentDetails(upload(videoId)))")

            if ( len( VIDEOS ) > 0 ):
                if ( os.path.isfile( "channel_data/%s.items" % channel ) ):
                    out_file = open( "channel_data/%s.items" % channel , "a" )
                else:
                    out_file = open( "channel_data/%s.items" % channel, "w" )
                for video in VIDEOS:
                    out_file.write( video )
                    out_file.write('\n')
                out_file.close()
            time_file = open("channel_data/%s.time" % channel, "w")
            time_file.write(datetime.now().isoformat())
            del VIDEOS[:]
        else:
            print("### Getting full list of videos for %s\n" % channel)
            # Getting the 'playlist' for all user videos works best for grabbing all videos.
            playlistitems_for_playlistid(service, part='contentDetails', playlistId=channel.replace( 'UC', 'UU' ), maxResults=50, fields="nextPageToken,items(contentDetails(videoId))")
            out_file = open("channel_data/%s.items" % channel, "w")
            for video in VIDEOS:
                out_file.write( video )
                out_file.write( '\n' )
            out_file.close()
            time_file = open( "channel_data/%s.time" % channel, "w" )
            # Write the retrieval time to the .time file using the ISO8601 format that YouTube expects.
            time_file.write( datetime.now().isoformat() )
            # Clear out the list for the next call
            del VIDEOS[:]

# Process data from the playlists.txt
def processPlaylists():
    print( "################# Processing Playlists ##################" )
    if ( not os.path.isdir( "playlist_data" ) ):
        os.makedirs( "playlist_data" )
    for playlist in PLAYLISTS:
        tokens = playlist.split( "," )
        thePlaylist = tokens[0]

        # Default to 7 days cache time for playlists
        age_limit = 604800
        doGet = True

        if ( len( tokens ) > 1 ):
            age_limit = int( tokens[1] )

        if ( os.path.isfile( "playlist_data/%s.items" % thePlaylist ) ):
            if ( age_limit is -1 ):
                print( "Not getting playlist items for %s, its age limit is infinite (-1)" % thePlaylist )
                doGet = false
            elif ( os.path.isfile( "playlist_data/%s.time" % thePlaylist ) ):
                timeFile = open( "playlist_data/%s.time" % thePlaylist, "r" )
                timestamp = timeFile.read()
                timeFile.close()
                timestamp = int( timestamp.strip() )
                if ( ( int( time.time() ) - timestamp ) < age_limit ):
                    print( "Playlist %s isn't out of date yet. %i seconds to go before it's old. Age limit is: %i seconds" % ( thePlaylist, age_limit - ( int( time.time() ) - timestamp ), age_limit ) )
                    doGet = False
        if ( doGet ):
            print( "### Getting full list of videos for playlist %s\n" % thePlaylist )
            playlistitems_for_playlistid(service, part='contentDetails', playlistId=thePlaylist, maxResults=50, fields="nextPageToken,items(contentDetails(videoId))")
            out_file = open("playlist_data/%s.items" % thePlaylist, "w")
            for video in VIDEOS:
                out_file.write( video )
                out_file.write('\n')
            out_file.close()
            time_file = open("playlist_data/%s.time" % thePlaylist, "w")
            time_file.write( str( int( time.time() ) ) )
            del VIDEOS[:]

VIDEOS = []
CHANNELS = []

with open("channels.txt", "r") as ins:
    myutil.readInputFile( "channels.txt", CHANNELS )

PLAYLISTS = []
if ( os.path.isfile( "playlists.txt" ) ):
    myutil.readInputFile( "playlists.txt", PLAYLISTS )

if ( len( CHANNELS ) > 0 ):
    processChannels()
else:
    print( "No channels in channels.txt to process!\n" )

if ( len( PLAYLISTS ) > 0 ):
    processPlaylists()
else:
    print( "No playlists in playlists.txt to process!\n" )

