import lyricsgenius
from credentials import client_access_token
import en_core_web_sm
import re
import sys
import spacy
import json
import pandas as pd
import numpy as np

genius = lyricsgenius.Genius(client_access_token)
genius.verbose = False


def get_discography(artist):
    disco = genius.search_artist(artist)

    data = np.empty((0, 7))

    for song in disco.songs:
        if song.lyrics == "Transcribing needed":
            continue

        features = ", ".join([item["name"] for item in song.featured_artists]).encode(
            'ascii', 'ignore').decode()
        producers = ", ".join([item["name"] for item in song.producer_artists]).encode(
            'ascii', 'ignore').decode()
        art_name = song.artist.encode(
            'ascii', 'ignore').decode().replace("*", '')

        data = np.vstack((data, np.asarray([song.title, art_name, song.lyrics, song.album, song.year,
                                            features if features != "" else pd.NA,
                                            producers if producers != "" else pd.NA], object)))

    df = pd.DataFrame(data, columns=[
                      "title", "artist", "lyrics", "album", "year", "featured_artists", "producers"])
    df.to_csv("artists/" + artist.replace(" ", '_') + ".csv")


def get_song_dict(title, artist, clean_ad_libs=False):
    # Some songs in genius library contain empty sections
    song_lyrics = genius.search_song(title, artist).to_text()
    chunks = song_lyrics.split("\n\n")
    chunked = {}
    exprs = r"\s*\([^)]*\)\s*"
    for chunk in chunks:
        part = chunk[chunk.find('[')+1:chunk.find(']')]

        chunk_lyrics = chunk[len(part) + 2:].split('\n')
        cleaned_lyrics = []

        for line in chunk_lyrics:
            line = re.sub(exprs, '', line)

            if line != "":
                cleaned_lyrics.append(r"{}".format(str(line)))

        chunked[part] = cleaned_lyrics[1:]

    return chunked


get_discography("kanye west")
