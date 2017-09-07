import random
import os
import myutil
import config

random.seed()

# Weight the channels higher, to play more videos from channels, versus playlists.
CHANNELS_WEIGHT = config.videotato_config['CHANNEL_WEIGHT']
PLAYLISTS_WEIGHT = config.videotato_config['PLAYLIST_WEIGHT']

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
    assert ( len( CHANNELS ) > 0 or len( PLAYLISTS ) > 0 )
    if ( len( CHANNELS ) is 0 ):
        return "PLAYLISTS"
    elif( len( PLAYLISTS ) is 0):
        return "CHANNELS"

    return weighted_choice( [ ( "CHANNELS", len(CHANNELS) * CHANNELS_WEIGHT ), ("PLAYLISTS", len(PLAYLISTS) * PLAYLISTS_WEIGHT ) ] )


WHICH = []
CHANNELS = []
PLAYLISTS = []

if ( os.path.isfile( os.path.dirname( os.path.realpath(__file__) ) + "/channels.txt" ) ):
    myutil.readInputFile( os.path.dirname( os.path.realpath(__file__) ) + "/channels.txt", CHANNELS )
else:
    print( "The file, %s, doesn't exist!" % os.path.dirname( os.path.realpath(__file__) ) + "/channels.txt" )

if ( os.path.isfile( os.path.dirname( os.path.realpath(__file__) ) + "/playlists.txt" ) ):
    myutil.readInputFile( os.path.dirname( os.path.realpath(__file__) ) + "/playlists.txt", PLAYLISTS )
else:
    print( "The file, %s, doesn't exist!" % os.path.dirname( os.path.realpath(__file__) ) + "/playlists.txt" )

if ( len( CHANNELS ) > 0 ):
    WHICH.append( "CHANNELS" )
else:
    print( "No channels in channels.txt to process!\n" )

if ( len( PLAYLISTS ) > 0 ):
    WHICH.append( "PLAYLISTS" )
else:
    print( "No playlists in playlists.txt to process!\n" )
if ( len( WHICH ) > 0 ):
    which = pickWhich()
    if ( which is "CHANNELS" ):
        print( "Picking a channel." )
        theChannel = random.choice( CHANNELS ).strip()
        vidFile = open( os.path.dirname( os.path.realpath(__file__) ) + "/channel_data/%s.items" % theChannel, "r ")
        theVideo = random_line( vidFile ).strip()
        vidFile.close()
    elif ( which is "PLAYLISTS" ):
        print( "Picking a playlist." )
        thePlaylist = random.choice( PLAYLISTS ).strip().split( "," )[0]
        vidFile = open( os.path.dirname( os.path.realpath(__file__) ) + "/playlist_data/%s.items" % thePlaylist, "r ")
        theVideo = random_line( vidFile ).strip()
        vidFile.close()

    print theVideo
    open( "result.txt", "w").write(theVideo)
else:
    print "Nothing to do!"