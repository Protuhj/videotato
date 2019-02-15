import json
import sys
import urllib
import os
import myutil



def goGetJSON(fullAPIURL, output_file):
    output_dir = os.path.dirname( os.path.realpath(__file__) ) + "/full_url_site_data"
    fullURLWithPageArg = fullAPIURL + "&order=asc&per_page=100&page={0}"
    max_pages = 1
    cur_page = 1
    lastRunVidID = None

    newOutFileName = "{0}/{1}.items".format(output_dir, output_file)
    newOutFileLastIDName = "{0}/{1}.last".format(output_dir, output_file)
    if ( os.path.isfile( newOutFileName ) ):
        outputFP = open( newOutFileName , "a" )
    else:
        outputFP = open( newOutFileName, "w" )

    if ( os.path.isfile( newOutFileLastIDName ) ):
        with open( newOutFileLastIDName, "r" ) as ins:
            inCtr = 0
            for line in ins:
                if ( inCtr == 0 ):
                    cur_page = int(line.strip())
                    max_pages = cur_page
                else:
                    lastRunVidID = line.strip()
                    break
                inCtr = inCtr + 1

    try:
        vidID = None
        while (cur_page <= max_pages):
            print("Loading page {0} out of {1}".format(cur_page, max_pages))
            url = urllib.urlopen(fullURLWithPageArg.format(cur_page))
            filecontents = json.loads(url.read())

            # Update max pages arg
            if (int(filecontents["total_pages"]) != max_pages):
                print("Updating max_pages to {0} from {1}".format(filecontents["total_pages"], max_pages))
                max_pages = int(filecontents["total_pages"])
            cur_page = int(filecontents["page"])

            # Now parse JSON
            for element in filecontents["data"]:
                vidID = element["_id"]
                if (lastRunVidID):
                    if ( lastRunVidID != element["_id"] ):
                        print ("Skipping {0}".format( "URL: https://roosterteeth.com%s" % element["canonical_links"]["self"] ))
                    else:
                        print ("Matched {0}".format( "URL: https://roosterteeth.com%s" % element["canonical_links"]["self"] ))
                        lastRunVidID = None
                else:
                    outputFP.write( "https://roosterteeth.com%s\n" % element["canonical_links"]["self"] )

            # Close URL object
            url.close()
            cur_page = cur_page + 1
        if ( vidID ):
            with open( newOutFileLastIDName, "w" ) as outs:
                outs.write( str( cur_page - 1 ) )
                outs.write('\n')
                outs.write( str( vidID ) )
                outs.write('\n')
    except Exception as e:
        print ("uh oh, error:")
        print (e)
    finally:
        outputFP.close()

RT_VIDS = []
myutil.readInputFile( os.path.dirname( os.path.realpath(__file__) ) + "/rt_entries.txt", RT_VIDS )
if ( len( RT_VIDS ) > 0 ):
    for line in RT_VIDS:
        tokens = line.split( "," )
        url = tokens[0].strip()
        media_token = tokens[1].strip()
        goGetJSON( url, media_token )
else:
    print( "No sites in rt_entries.txt to process!\n" )
