# Reads one of the input files (channels.txt, playlists.txt, etc.) and appends the valid entries to the given list.
# Lines that start with '#' are comments, and are ignored.
def readInputFile( filename, listToAppendTo ):
    with open( filename, "r" ) as ins:
        for line in ins:
            stripped = line.strip()
            # Ignore comments and empty lines
            if ( not stripped.startswith( "#" ) and stripped ):
                listToAppendTo.append( stripped )