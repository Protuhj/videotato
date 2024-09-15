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


# Returns a random choice from an array of objects
# The objects just need a "weight" key
def weighted_choice_object(objectsWithWeights):
    random.shuffle(objectsWithWeights)
    total = 0
    for obj in objectsWithWeights:
        if obj['weight'] > 0:
            total += obj['weight']
    r = random.uniform(0, total)
    upto = 0
    for obj in objectsWithWeights:
        if obj['weight'] <= 0:
            continue
        if upto + obj['weight'] >= r:
            return obj
        upto += obj['weight']
    assert False, "Shouldn't get here"

def pickWhich():
    assert ( len( CHANNELS ) > 0 or len( PLAYLISTS ) > 0 or len( MUSIC ) > 0 or len( FULL_URL ) > 0)
    chanLen = len( CHANNELS )
    playlistLen = len ( PLAYLISTS )
    musicLen = len( MUSIC )
    fullURLLen = len ( FULL_URL )
    if ( chanLen == 0 and musicLen == 0 and fullURLLen == 0 ):
        return "PLAYLISTS"
    elif( chanLen == 0 and playlistLen == 0 and fullURLLen == 0 ):
        return "MUSIC"
    elif( playlistLen == 0 and musicLen == 0 and fullURLLen == 0 ):
        return "CHANNELS"
    elif ( chanLen == 0 and playlistLen == 0 and musicLen == 0 ):
        return "FULL_URL"

    chanWeight = getNonZeroWeightCount(CHANNELS) * CHANNELS_WEIGHT
    playlistWeight = getNonZeroWeightCount(PLAYLISTS) * PLAYLISTS_WEIGHT
    musicWeight = getNonZeroWeightCount(MUSIC) * MUSIC_WEIGHT
    fullWeight = getNonZeroWeightCount(FULL_URL) * FULL_URL_WEIGHT
    print ("Chan: {0} play: {1} music: {2} full: {3}".format(chanWeight, playlistWeight, musicWeight, fullWeight))
    return weighted_choice( [ ( "CHANNELS", chanWeight ), ("PLAYLISTS", playlistWeight ), ("MUSIC", musicWeight ), ("FULL_URL", fullWeight ) ] )


# Count how many elements in the array have a weight > 0
def getNonZeroWeightCount(objectsWithWeights):
    total = 0
    for obj in objectsWithWeights:
        if obj['weight'] > 0:
            total += 1
    return total


WHICH = []
PLAYLISTS = []
MUSIC = []
FULL_URL = []
CHANNELS = []


# ---- Channels ----- 
try:
    if ( os.path.isfile( os.path.dirname( os.path.realpath(__file__) ) + "/channels.py" ) ):
        exec(open("./channels.py").read())
    else:
        print( "The file, %s, doesn't exist!" % os.path.dirname( os.path.realpath(__file__) ) + "/channels.py" )
except NameError as e:
    print("CHANNELS not found, NameError exception: " + str(e))


# If there was no data in channels.py, then try filling it with data from channels.txt
if ( len(CHANNELS) == 0 ):
    if ( os.path.isfile( os.path.dirname( os.path.realpath(__file__) ) + "/channels.txt" ) ):
        myutil.readInputFile( os.path.dirname( os.path.realpath(__file__) ) + "/channels.txt", CHANNELS )
    else:
        print( "The file, %s, doesn't exist!" % os.path.dirname( os.path.realpath(__file__) ) + "/channels.txt" )
    # converting from old format to new object format
    CHANNELS_COPY = []
    for channel in CHANNELS:
        CHANNELS_COPY.append({"id": channel, "weight": 1, "channel": "unknown"})
    CHANNELS = CHANNELS_COPY

print ("CHANNELS has {0} elements".format(len(CHANNELS)))

# ---- Playlists ----
try:
    if ( os.path.isfile( os.path.dirname( os.path.realpath(__file__) ) + "/playlists.py" ) ):
        exec(open("./playlists.py").read())
    else:
        print( "The file, %s, doesn't exist!" % os.path.dirname( os.path.realpath(__file__) ) + "/playlists.py" )
except NameError as e:
    print("PLAYLISTS not found, NameError exception: " + str(e))
    
# If there was no data in playlists.py, then try filling it with data from playlists.txt
if ( len(PLAYLISTS) == 0 ):
    if ( os.path.isfile( os.path.dirname( os.path.realpath(__file__) ) + "/playlists.txt" ) ):
        myutil.readInputFile( os.path.dirname( os.path.realpath(__file__) ) + "/playlists.txt", PLAYLISTS )
    else:
        print( "The file, %s, doesn't exist!" % os.path.dirname( os.path.realpath(__file__) ) + "/playlists.txt" )
    # converting from old format to new object format
    PLAYLISTS_COPY = []
    for playlist in PLAYLISTS_COPY:
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

# ---- Music ----
try:
    if ( os.path.isfile( os.path.dirname( os.path.realpath(__file__) ) + "/music.py" ) ):
        exec(open("./music.py").read())
    else:
        print( "The file, %s, doesn't exist!" % os.path.dirname( os.path.realpath(__file__) ) + "/music.py" )
except NameError as e:
    print("MUSIC not found, NameError exception: " + str(e))

# If there was no data in music.py, then try filling it with data from music.txt
if ( len(MUSIC) == 0 ):
    if ( os.path.isfile( os.path.dirname( os.path.realpath(__file__) ) + "/music.txt" ) ):
        myutil.readInputFile( os.path.dirname( os.path.realpath(__file__) ) + "/music.txt", MUSIC )
    else:
        print( "The file, %s, doesn't exist!" % os.path.dirname( os.path.realpath(__file__) ) + "/music.txt" )
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

# ---- Full URLs ----

try:
    if ( os.path.isfile( os.path.dirname( os.path.realpath(__file__) ) + "/full_url_sites.py" ) ):
        exec(open("./full_url_sites.py").read())
    else:
        print( "The file, %s, doesn't exist!" % os.path.dirname( os.path.realpath(__file__) ) + "/full_url_sites.py" )
except NameError as e:
    print("FULL_URL not found, NameError exception: " + str(e))

# If there was no data in full_url_sites.py, then try filling it with data from full_url_sites.txt
if ( len(FULL_URL) == 0 ):
    if ( os.path.isfile( os.path.dirname( os.path.realpath(__file__) ) + "/full_url_sites.txt" ) ):
        myutil.readInputFile( os.path.dirname( os.path.realpath(__file__) ) + "/full_url_sites.txt", FULL_URL )
    else:
        print( "The file, %s, doesn't exist!" % os.path.dirname( os.path.realpath(__file__) ) + "/full_url_sites.txt" )
    # converting from old format to new object format
    FULL_URL_COPY = []
    for playlist in FULL_URL_COPY:
        FULL_URL_COPY.append({"id": channel, "weight": 1, "name": "unknown"})
    FULL_URL = FULL_URL_COPY

if ( len( CHANNELS ) > 0 ):
    WHICH.append( "CHANNELS" )
else:
    print( "No channels in channels.py to process!\n" )

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
    theSource = "unknown"
    try:
        if ( which == "CHANNELS" ):
            print( "Picking a channel." )
            theChannel = weighted_choice_object(CHANNELS)
            theSource = theChannel['name']
            print( "Chose channel: " + repr(theChannel) )
            vidFile = open( os.path.dirname( os.path.realpath(__file__) ) + "/channel_data/%s.items" % theChannel['id'], "r")
            theVideo = random_line( vidFile ).split( ",")[0].strip()
            vidFile.close()
            if ( theVideo == "" ):
                raise Exception("channel resulted in empty video: " + theChannel)
        elif ( which == "PLAYLISTS" ):
            print( "Picking a playlist." )
            thePlaylist = weighted_choice_object(PLAYLISTS)
            theSource = thePlaylist['name']
            print( "Chose playlist: " + repr(thePlaylist) )
            vidFile = open( os.path.dirname( os.path.realpath(__file__) ) + "/playlist_data/%s.items" % thePlaylist['id'], "r")
            theVideo = random_line( vidFile ).split( ",")[0].strip()
            vidFile.close()
            if ( theVideo == "" ):
                raise Exception("playlist resulted in empty video: " + thePlaylist)
        elif ( which == "MUSIC" ):
            print( "Picking a music playlist." )
            thePlaylist = weighted_choice_object(MUSIC)
            theSource = thePlaylist['name']
            print( "Chose music playlist: " + repr(thePlaylist) )
            vidFile = open( os.path.dirname( os.path.realpath(__file__) ) + "/music_data/%s.items" % thePlaylist['id'], "r")
            theVideo = random_line( vidFile ).split( ",")[0].strip()
            vidFile.close()
            if ( theVideo == "" ):
                raise Exception("music playlist resulted in empty video: " + thePlaylist)
        elif ( which == "FULL_URL" ):
            print( "Picking a full url entry." )
            theSite = weighted_choice_object(FULL_URL)
            theSource = theSite['name']
            print( "Chose site: " + repr(theSite) )
            vidFile = open( os.path.dirname( os.path.realpath(__file__) ) + "/full_url_site_data/%s.items" % theSite['id'], "r")
            theVideo = random_line( vidFile ).strip()
            vidFile.close()
            if ( theVideo == "" ):
                raise Exception("full url site resulted in empty video: " + theSite)
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
        outSource = open( "result_source.txt", "w")
        outSource.write(theSource)
        outSource.close()
    except Exception as e:
        with open('randomlineError.txt', 'w') as f:
            f.write(str(e))
            f.write(traceback.format_exc())
        for i in range(10, 5, -1): winsound.Beep(i * 100, 30)

else:
    print ("Nothing to do!")