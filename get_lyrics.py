import lyricsgenius
from genius_credentials import client_access_token
import en_core_web_sm
import re
import sys
import spacy
import json
import pandas as pd
import numpy as np

genius = lyricsgenius.Genius(client_access_token)
genius.verbose = False

# get_discography will use Genius API to pull all the song names, lyrics, and artists featured on the song
# how the API is formatted, it will start by extracting the most popular song on Genius.com, and next song
# is less popular, so on until it reaches the least popular song.  It will only pull songs where the artist
# is the primary artist, not a featured artist.
def get_discography(artist):
    print("...")
    disco = genius.search_artist(artist)

    discog = {}

    for song in disco.songs:
        song_dict = {}
        if song.lyrics == "Transcribing needed":
            continue

        features = ", ".join([item["name"] for item in song.featured_artists]).encode(
            'ascii', 'ignore').decode()

        song_dict['features'] = features
        song_dict['album_name'] = song.album
        song_dict['lyrics'] = song.lyrics
        #print(song)
        #song = str(song).split('"')[1:2]
        #seperator = ' '
        #song = seperator.join(song)
        discog[song.title] = song_dict
        
       
        #print(song)

    #df.to_csv("artists/" + artist.replace(" ", '_') + ".csv")
    print(discog)
    
    #print(song_dict)


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

# TODO: write try and except so that if program fails it restarts itself
artists = ['Boyscott'] 
# TODO: Write feature crawler to pull running discography of all the newly found featured artists

for artist in artists:
    print(artist + " running")
    get_discography(artist)
    print("done")
 