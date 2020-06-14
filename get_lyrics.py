import lyricsgenius
from credentials import client_access_token
import re
import sys
import json

genius = lyricsgenius.Genius(client_access_token)
genius.verbose = False


def get_song_dict(title, artist, clean_ad_libs=False):
    # Some songs in genius library contain empty sections
    song_lyrics = genius.search_song(title, artist).to_text()
    chunks = song_lyrics.split("\n\n")
    chunked = {}
    for chunk in chunks:
        part = chunk[chunk.find("[")+1:chunk.find("]")]
        chunk_lyrics = chunk[len(part) + 2:].split("\n")
        cleaned_lyrics = []
        for line in chunk_lyrics:
            line = re.sub(r'\s*\([^)]*\)\s*', '', line)
            if line != "":
                cleaned_lyrics.append(r"{}".format(str(line)))
        chunked[part] = cleaned_lyrics[1:]

    return chunked

title = "sicko mode"
artist = "travis scott"

print(get_song_dict(title, artist))
