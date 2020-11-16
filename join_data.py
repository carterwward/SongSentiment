from get_valence import get_valence
from get_lyrics import get_discography

def join_spotify_genius(artist):
    spotify_dict = get_valence(artist)
    genius_dict = get_discography(artist)
    common_keys = set(genius_dict.keys()) & set(spotify_dict.keys())
    # print("in spot not genius Keys:", set(spotify_dict.keys()) - set(genius_dict.keys()), '\n')
    # print("in genius not spot Keys:", set(genius_dict.keys()) - set(spotify_dict.keys()), '\n')
    # print("Common Keys:", common_keys)
    print("len of discog", len(common_keys))
    full_dict = {}
    for key in common_keys:
        song_dict = {}
        # print(spotify_dict.keys())
        song_dict['valence'] = spotify_dict[key]['valence']
        song_dict['album'] = spotify_dict[key]['album']
        song_dict['lyrics'] = genius_dict[key]['lyrics']
        song_dict['year'] = genius_dict[key]['year']
        song_dict['features'] = genius_dict[key]['features']
        full_dict[key] = song_dict
    return full_dict
    