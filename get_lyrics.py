import lyricsgenius
from credentials import client_access_token

genius = lyricsgenius.Genius(client_access_token)
genius.verbose = False

def get_song(title, artist):
    print(genius.search_song(title, artist).lyrics)
    return genius.search_song(title, artist).lyrics

get_song("prom king", "saba")
