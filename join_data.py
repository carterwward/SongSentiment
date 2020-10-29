from get_valence import get_valence
from get_lyrics import get_discography

def join_spotify_genius(artist):
    genius_dict = get_discography(artist)
    spotify_dict = get_valence(artist)
    common_keys = set(genius_dict.keys()) & set(spotify_dict.keys())
    print("in spot not genius Keys:", set(spotify_dict.keys()) - set(genius_dict.keys()))
    print("in genius not spot Keys:", set(genius_dict.keys()) - set(spotify_dict.keys()))
    print("Common Keys:", common_keys)
    full_dict = {}
    for key in common_keys:
        song_dict = {}
        song_dict['valence'] = spotify_dict['valence']
        song_dict['album'] = spotify_dict['album']
        song_dict['lyrics'] = genius_dict['lyrics']
        song_dict['year'] = genius_dict['year']
        song_dict['features'] = genius_dict['features']
        full_dict[key] = song_dict

    return full_dict

    
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
join_spotify_genius('thundercat')