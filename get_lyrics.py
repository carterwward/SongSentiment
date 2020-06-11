import lyricsgenius
from credentials import client_access_token
import re

genius = lyricsgenius.Genius(client_access_token)
genius.verbose = False


def get_song_dict(title, artist, clean_ad_libs=False):
    song = genius.search_song(title, artist).to_dict()
    song_lyrics = song["lyrics"].encode("utf-8").decode().replace(u"\u2019", "'")
    # for i in range(len(song_lyrics)):
    #     if song_lyrics[i] == "'"and song_lyrics[i-1 "\\"
    chunks = song_lyrics.split("\n\n")
    chunked = {}
    for chunk in chunks:
        part = chunk[chunk.find("[")+1:chunk.find("]")]
        chunk_lyrics = chunk[len(part) + 2:].split("\n")
        cleaned_lyrics = []
        for line in chunk_lyrics:
            cleaned_line = line.replace("\\", "")
            cleaned_lyrics.append(str(cleaned_line))
        chunked[part] = cleaned_lyrics[1:]

    return chunked

title = "doomsday"
artist = "mf doom"
print(get_song_dict(title, artist))