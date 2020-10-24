import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotify_credentials import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET))

def get_valence(artist_name):
    results = sp.search(q = "artist:" + artist_name, type = "artist")
    print(results['artists']['items'])

    # initialize uri variable as empty string
    # iterate over list of artist dictionaries results['artists']['items']
        # check to see if all lower case version of artist_name and name in each dict are equivalent
            # read uri into variable and break from loop

get_valence('kendrick lamar')