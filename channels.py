# Comment lines start with the # character
# If you only have a username, go to: https://developers.google.com/apis-explorer/#p/youtube/v3/youtube.channels.list?part=snippet&fields=items/id
# put the username in the 'forUsername' field
# and then hit 'Execute without OAuth'
# If a channel is found, it will be the only entry in the Response at the bottom of the page for 'id'
##
# View source on the channel's About page and search for "browse_id", the channel ID should be near it
##


# You can optionally set the "noupdate" field to True if you don't want to retrieve any new updates for a given channel
CHANNELS = [
    { "id": "UCsB0LwkHPWyjfZ-JwvtwEXw", "weight": 10, "name": "Achievement Hunter", "noupdate": True},
    { "id": "UCZYTClx2T1of7BRZ86-8fow", "weight": 2, "name": "SciShow"},
    { "id": "UCrMePiHCWG4Vwqv3t7W9EFg", "weight": 2, "name": "SciShow Space"},
]
