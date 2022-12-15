import os
import sys
import fileinput
import glob
import re
import winsound
import config

Freq = 1700 # Set Frequency To 2500 Hertz
Dur = 250 # Set Duration To 1000 ms == 1 second

def removeTextInline( theText, theFile ):
    with open( theFile ) as f:
        contents = f.read()
        if theText in contents:
            f.close()
            print( "Found " + theText + " in " + theFile )
            for line in fileinput.input(theFile, inplace = True):
                if not theText in line:
                    print (line)
            if ( config.videotato_config['PLAY_SOUND_ON_DELETE'] is True ):
                winsound.Beep(Freq,Dur)

if ( os.path.isfile( "result.txt" ) ):
    resultFile = open( "result.txt", "r" )
    resultText = resultFile.read().strip()
    resultFile.close()
    if resultText:
        for file in glob.glob( 'channel_data/*' ):
            removeTextInline( resultText, file )
        for file in glob.glob( 'playlist_data/*' ):
            removeTextInline( resultText, file )
        for file in glob.glob( 'music_data/*' ):
            removeTextInline( resultText, file )
        for file in glob.glob( 'full_url_site_data/*' ):
            removeTextInline( resultText, file )
    else:
        print( "Invalid result text: " + resultText )
else:
    print( "result.txt doesn't exist." )
