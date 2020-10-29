from get_valence import get_valence
from get_lyrics import get_discography

def join_spotify_genius(artist):
    print('hi')
    
# TODO: implement getting the full disocgraphy for all features artist in a given artists full disography
# I realized for this to work we also have to be calling the spotify API, so maybe we should put this function in a different file
def get_featured_artist_discography(artist):
# set is underordered and has unique elements
    artist_set = set()
    print("...")
    primary_artist_discography = get_discography(artist)
    for c in primary_artist_discography:
        artist_set.add(primary_artist_discography[c]["features"])


    print(artist_set)