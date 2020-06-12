import lyricsgenius
from credentials import client_access_token
import re
import sys
import json

genius = lyricsgenius.Genius(client_access_token)
genius.verbose = False


def get_song_dict(title, artist, clean_ad_libs=False):
    song_lyrics = genius.search_song(title, artist).to_text().replace("'", "QUOTE")
    chunks = song_lyrics.split("\n\n")
    chunked = {}
    for chunk in chunks:
        part = chunk[chunk.find("[")+1:chunk.find("]")]
        chunk_lyrics = chunk[len(part) + 2:].split("\n")
        cleaned_lyrics = []
        for line in chunk_lyrics:
            cleaned_line = ("" + line.encode("utf-8").decode(sys.stdout.encoding))
            cleaned_lyrics.append(str(cleaned_line))
        chunked[part] = cleaned_lyrics[1:]

    return chunked

title = "doomsday"
artist = "mf doom"
print(get_song_dict(title, artist))