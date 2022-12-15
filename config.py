videotato_config = dict(
    client_secret_filename = "client_secret.json",
    storage_filename = "videotato-oauth2.json",
    # Multiplicative weight for choosing channels when getting a random video.
    # I prefer playing random videos from channels at this point.
    CHANNEL_WEIGHT = 35,
    # Multiplicative weight for choosing playlists when getting a random video.
    PLAYLIST_WEIGHT = 15,
    # Multiplicative weight for choosing music when getting a random video.
    MUSIC_WEIGHT = 0,
    # Multiplicative weight for choosing a full URL when getting a random video.
    FULL_URL_WEIGHT = 0,
    # Option to play a little tone when deleting items from the local data
    # Default to False so people aren't confused by this when it happens.
    PLAY_SOUND_ON_DELETE = True,
)