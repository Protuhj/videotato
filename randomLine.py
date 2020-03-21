import random
import os
import myutil
import config
import winsound
import traceback

random.seed()

# Weight the channels higher, to play more videos from channels, versus playlists.
CHANNELS_WEIGHT = config.videotato_config['CHANNEL_WEIGHT']
PLAYLISTS_WEIGHT = config.videotato_config['PLAYLIST_WEIGHT']
MUSIC_WEIGHT = config.videotato_config['MUSIC_WEIGHT']
FULL_URL_WEIGHT = config.videotato_config['FULL_URL_WEIGHT']

def random_line(afile):
    line = next(afile)
    for num, aline in enumerate(afile):
        if random.randrange(num + 2): continue
        line = aline
    return line


def weighted_choice(choices):
   total = sum(w for c, w in choices)
   r = random.uniform(0, total)
   upto = 0
   for c, w in choices:
      if upto + w >= r:
         return c
      upto += w
   assert False, "Shouldn't get here"


def pickWhich():
    assert ( len( CHANNELS ) > 0 or len( PLAYLISTS ) > 0 or len( MUSIC ) > 0 or len( FULL_URL ) > 0)
    chanLen = len( CHANNELS )
    playlistLen = len ( PLAYLISTS )
    musicLen = len( MUSIC )
    fullURLLen = len ( FULL_URL )
    if ( chanLen is 0 and musicLen is 0 and fullURLLen is 0 ):
        return "PLAYLISTS"
    elif( chanLen is 0 and playlistLen is 0 and fullURLLen is 0 ):
        return "MUSIC"
    elif( playlistLen is 0 and musicLen is 0 and fullURLLen is 0 ):
        return "CHANNELS"
    elif ( chanLen is 0 and playlistLen is 0 and musicLen is 0 ):
        return "FULL_URL"

    chanWeight = len(CHANNELS) * CHANNELS_WEIGHT
    playlistWeight = len(PLAYLISTS) * PLAYLISTS_WEIGHT
    musicWeight = len(MUSIC) * MUSIC_WEIGHT
    fullWeight = len(FULL_URL) * FULL_URL_WEIGHT
    print ("Chan: {0} play: {1} music: {2} full: {3}".format(chanWeight, playlistWeight, musicWeight, fullWeight))
    return weighted_choice( [ ( "CHANNELS", chanWeight ), ("PLAYLISTS", playlistWeight ), ("MUSIC", musicWeight ), ("FULL_URL", fullWeight ) ] )


WHICH = []
CHANNELS = []
PLAYLISTS = []
MUSIC = []
FULL_URL = []

if ( os.path.isfile( os.path.dirname( os.path.realpath(__file__) ) + "/channels.txt" ) ):
    myutil.readInputFile( os.path.dirname( os.path.realpath(__file__) ) + "/channels.txt", CHANNELS )
else:
    print( "The file, %s, doesn't exist!" % os.path.dirname( os.path.realpath(__file__) ) + "/channels.txt" )

if ( os.path.isfile( os.path.dirname( os.path.realpath(__file__) ) + "/playlists.txt" ) ):
    myutil.readInputFile( os.path.dirname( os.path.realpath(__file__) ) + "/playlists.txt", PLAYLISTS )
else:
    print( "The file, %s, doesn't exist!" % os.path.dirname( os.path.realpath(__file__) ) + "/playlists.txt" )

if ( os.path.isfile( os.path.dirname( os.path.realpath(__file__) ) + "/music.txt" ) ):
    myutil.readInputFile( os.path.dirname( os.path.realpath(__file__) ) + "/music.txt", MUSIC )
else:
    print( "The file, %s, doesn't exist!" % os.path.dirname( os.path.realpath(__file__) ) + "/music.txt" )

if ( os.path.isfile( os.path.dirname( os.path.realpath(__file__) ) + "/full_url_sites.txt" ) ):
    myutil.readInputFile( os.path.dirname( os.path.realpath(__file__) ) + "/full_url_sites.txt", FULL_URL )
else:
    print( "The file, %s, doesn't exist!" % os.path.dirname( os.path.realpath(__file__) ) + "/full_url_sites.txt" )

if ( len( CHANNELS ) > 0 ):
    WHICH.append( "CHANNELS" )
else:
    print( "No channels in channels.txt to process!\n" )

if ( len( PLAYLISTS ) > 0 ):
    WHICH.append( "PLAYLISTS" )
else:
    print( "No playlists in playlists.txt to process!\n" )

if ( len( MUSIC ) > 0 ):
    WHICH.append( "MUSIC" )
else:
    print( "No music in music.txt to process!\n" )

if ( len( FULL_URL ) > 0 ):
    WHICH.append( "FULL_URL" )
else:
    print( "No sites in full_url_sites.txt to process!\n" )

if ( len( WHICH ) > 0 ):
    which = pickWhich()
    try:
        if ( which is "CHANNELS" ):
            print( "Picking a channel." )
            theChannel = random.choice( CHANNELS ).strip()
            try:
                vidFile = open( os.path.dirname( os.path.realpath(__file__) ) + "/channel_data/%s.details" % theChannel, "r ")
            except:
                pass
                vidFile = open( os.path.dirname( os.path.realpath(__file__) ) + "/channel_data/%s.items" % theChannel, "r ")
            theVideo = random_line( vidFile ).split( ",")[0].strip()
            vidFile.close()
        elif ( which is "PLAYLISTS" ):
            print( "Picking a playlist." )
            thePlaylist = random.choice( PLAYLISTS ).strip().split( "," )[0]
            try:
                vidFile = open( os.path.dirname( os.path.realpath(__file__) ) + "/playlist_data/%s.details" % thePlaylist, "r ")
            except:
                pass
                vidFile = open( os.path.dirname( os.path.realpath(__file__) ) + "/playlist_data/%s.items" % thePlaylist, "r ")
            theVideo = random_line( vidFile ).split( ",")[0].strip()
            vidFile.close()
        elif ( which is "MUSIC" ):
            print( "Picking a music playlist." )
            thePlaylist = random.choice( MUSIC ).strip().split( "," )[0]
            try:
                vidFile = open( os.path.dirname( os.path.realpath(__file__) ) + "/music_data/%s.details" % thePlaylist, "r ")
            except:
                pass
                vidFile = open( os.path.dirname( os.path.realpath(__file__) ) + "/music_data/%s.items" % thePlaylist, "r ")
            theVideo = random_line( vidFile ).split( ",")[0].strip()
            vidFile.close()
        elif ( which is "FULL_URL" ):
            print( "Picking a full url entry." )
            theSite = random.choice( FULL_URL ).strip().split( ", " )[0]
            vidFile = open( os.path.dirname( os.path.realpath(__file__) ) + "/full_url_site_data/%s.items" % theSite, "r ")
            theVideo = random_line( vidFile ).strip()
            vidFile.close()
        else:
            assert False, "Invalid WHICH"

        #inFile = open( "result.txt", "r")
        #curResult = inFile.readline()
        #inFile.close()
        #f (curResult == theVideo):
        #    print ("Prev: {0} new: {1}".format(curResult, theVideo))
        print ("new: {0}".format(theVideo))

        outFile = open( "result.txt", "w")
        outFile.write(theVideo)
        outFile.close()
    except Exception as e:
        with open('randomlineError.txt', 'w') as f:
            f.write(str(e))
            f.write(traceback.format_exc())
        for i in range(10, 5, -1): winsound.Beep(i * 100, 30)

else:
    print "Nothing to do!"