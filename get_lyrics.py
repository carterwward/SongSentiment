import lyricsgenius
from credentials import client_access_token

genius = lyricsgenius.Genius(client_access_token)
genius.verbose = False


def get_song_dict(title, artist, clean_ad_libs=False):
    song = genius.search_song(title, artist).to_dict()
    song_lyrics = song["lyrics"].encode().decode("utf-8").replace(u"\u2019", "'")
    chunks = song_lyrics.split("\n\n")
    chunked = {}
    for chunk in chunks:
        part = chunk[chunk.find("[")+1:chunk.find("]")]
        chunked[part] = chunk[len(part) + 2:]

    return chunked

title = "baby"
artist = "justin bieber"
print(get_song_dict(title, artist))