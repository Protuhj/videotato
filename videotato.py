import os
import sys
import time
import myutil
import httplib2
import config
import random
from pprint import pprint

from datetime import datetime, timezone,timedelta
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow


# From https://stackoverflow.com/a/3096934/16423400
UNITS = {"s":"seconds", "m":"minutes", "h":"hours", "d":"days", "w":"weeks"}

def convert_to_seconds(s):
    try:
        sec_val = int(s)
        return sec_val
    except:
        count = int(s[:-1])
        unit = UNITS[ s[-1] ]
        td = timedelta(**{unit: count})
        return td.seconds + 60 * 60 * 24 * td.days

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
            if ( 'contentDetails' in result and 'upload' in result['contentDetails'] ):
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
    for chanObj in CHANNELS:
        channel = chanObj['id']
        # 'noupdate' doesn't have to be set, so use the .get(key, default) form
        if chanObj.get("noupdate", False):
            print(f"Not updating channel {chanObj['name']} due to 'noupdate' being True.")
            continue
        elif (chanObj['weight'] <= 0):
            print(f"Skipping channel {chanObj['name']} due to weight being <= 0")
            continue

        # Check to see if the channel data has been grabbed at some point already
        # If it has, use the time in the .time file in order to get only the activity since the full list was retrieved.
        if ( os.path.isfile( "channel_data/%s.time" % channel ) ):
            print("### Getting delta list of videos for {1} (id: {0})".format(channel, chanObj['name']))
            timeFile = open("channel_data/%s.time" % channel, "r")
            timestamp = timeFile.read().strip()
            timeFile.close()
            if ( timestamp.find("+") == -1 ):
                timestamp += "Z"
            activities_list_for_channelid(service, part='contentDetails', channelId=channel, maxResults=50, publishedAfter=timestamp, fields="nextPageToken,items(contentDetails(upload(videoId)))")

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
            time_file.write(datetime.now(timezone.utc).isoformat())
            # Clear out the list for the next call
            del VIDEOS[:]
        else:
            print("### Getting full list of videos for {1} (id: {0})".format(channel, chanObj['name']))
            try:
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
            except:
                print( "####### Failed to query playlist: %s\n" %thePlaylist )


# Process data from the MUSIC or PLAYLISTS array
# Music is just a specialization of the PLAYLIST type, to allow for different weightings
# Sometimes I just want music, ya know?
def processPlaylist(isMusic = False):
    if isMusic:
        print( "################# Processing Music ##################" )
        data_dir = "music_data"
        which_array = MUSIC
        info_string_token = "music playlist"
    else:
        print( "################# Processing Playlists ##################" )
        data_dir = "playlist_data"
        which_array = PLAYLISTS
        info_string_token = "playlist"

    if ( not os.path.isdir( data_dir ) ):
        os.makedirs( data_dir )
    for array_obj in which_array:
        thePlaylistID = array_obj['id']
        # 'noupdate' doesn't have to be set, so use the .get(key, default) form
        if array_obj.get("noupdate", False):
            print(f"Not updating playlist {array_obj['name']} due to 'noupdate' being True.")
            continue
        doGet = True
        age_limit = convert_to_seconds( array_obj.get("age", "7d") )
        if ( os.path.isfile( f"{data_dir}/{thePlaylistID}.items" ) ):
            if ( age_limit <= 0 ):
                print( f"Not getting {info_string_token} items for {array_obj['name']}, its age limit is <= 0" )
                doGet = False
            elif ( os.path.isfile( f"{data_dir}/{thePlaylistID}.time" ) ):
                timeFile = open( f"{data_dir}/{thePlaylistID}.time", "r" )
                timestamp = timeFile.read()
                timeFile.close()
                timestamp = int( timestamp.strip() )
                if ( ( int( time.time() ) - timestamp ) < age_limit ):
                    print( f"The {info_string_token} {array_obj['name']} isn't out of date yet. {age_limit - ( int( time.time() ) - timestamp )} seconds to go before it's old. Age limit is: {age_limit} seconds" )
                    doGet = False
        if ( doGet ):
            print( f"### Getting full list of videos for {info_string_token} {array_obj['name']}\n" )
            try:
                playlistitems_for_playlistid(service, part='contentDetails', playlistId=thePlaylistID, maxResults=50, fields="nextPageToken,items(contentDetails(videoId))")
                out_file = open(f"{data_dir}/{thePlaylistID}.items", "w")
                for video in VIDEOS:
                    out_file.write( video )
                    out_file.write('\n')
                out_file.close()
                time_file = open(f"{data_dir}/{thePlaylistID}.time", "w")
                time_file.write( str( int( time.time() ) ) )
                # Clear out the list for the next call
                del VIDEOS[:]
            except:
                print( f"####### Failed to query {info_string_token}: {array_obj['name']}\n")

VIDEOS = []

#-- Channels --#
try:
    exec(open("./channels.py").read())
except Error as e:
    print("CHANNELS not found, loading from channels.txt: " + str(e))
    CHANNELS = []
    if ( os.path.isfile( "channels.txt" ) ):
        myutil.readInputFile( "channels.txt", CHANNELS )
        # converting from old format to new object format
        CHANNELS_COPY = []
        for channel in CHANNELS:
            CHANNELS_COPY.append({"id": channel, "weight": 1, "channel": "unknown"})
        CHANNELS = CHANNELS_COPY
    else:
        print("channels.txt doesn't exist!")


if ( len( CHANNELS ) > 0 ):
    processChannels()
else:
    print( "No channels to process!\n" )

#-----------#

#-- PLAYLISTS --#
try:
    exec(open("./playlists.py").read())
except Error as e:
    print("PLAYLISTS not found, loading from playlists.txt: " + str(e))
    PLAYLISTS = []
    if ( os.path.isfile( "playlists.txt" ) ):
        myutil.readInputFile( "playlists.txt", PLAYLISTS )
        # converting from old format to new object format
        PLAYLISTS_COPY = []
        for playlist in PLAYLISTS:
            tokens = playlist.split( "," )
            thePlaylist = tokens[0]

            # Default to 7 days cache time
            age_limit = "7d"

            if ( len( tokens ) > 1 ):
                age_limit = int( tokens[1] )
                if age_limit > 0:
                    age_limit = tokens + "s"
                else:
                    age_limit = "0"
            PLAYLISTS_COPY.append({"id": thePlaylist,  "age" : age_limit, "weight": 1, "name": "unknown"})
        PLAYLISTS = PLAYLISTS_COPY
    else:
        print("playlists.txt doesn't exist!")

if ( len( PLAYLISTS ) > 0):
    processPlaylist(False)
else:
    print( "No playlists to process!\n" )

#-------------#

#-- MUSIC --#
try:
    exec(open("./music.py").read())
except Error as e:
    print("MUSIC not found, loading from music.txt: " + str(e))
    MUSIC = []
    if ( os.path.isfile( "music.txt" ) ):
        myutil.readInputFile( "music.txt", MUSIC )
        # converting from old format to new object format
        MUSIC_COPY = []
        for music_playlist in MUSIC:
            tokens = music_playlist.split( "," )
            thePlaylist = tokens[0]

            # Default to 7 days cache time for music
            age_limit = "7d"

            if ( len( tokens ) > 1 ):
                age_limit = int( tokens[1] )
                if age_limit > 0:
                    age_limit = tokens + "s"
                else:
                    age_limit = "0"
            MUSIC_COPY.append({"id": thePlaylist,  "age" : age_limit, "weight": 1, "name": "unknown"})
        MUSIC = MUSIC_COPY
    else:
        print("music.txt doesn't exist!")

if ( len( MUSIC ) > 0 ):
    processPlaylist(True)
else:
    print( "No music to process!\n" )

if ( not os.path.isdir( "full_url_site_data" ) ):
    os.makedirs( "full_url_site_data" )

#-----------#