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
genius.remove_section_headers = True # Remove section headers (e.g. [Chorus]) from lyrics when searching
#genius.skip_non_songs = False # Include hits thought to be non-songs (e.g. track lists)
genius.excluded_terms = ["(Remix)", "(Live)"] # Exclude songs with these words in their title

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
        song_dict['year'] = song.year
        discog[song.title] = song_dict

    return discog
    




# TODO: write try and except so that if program fails it restarts itself
artists = ['JPEGMAFIA'] 
# TODO: Write feature crawler to pull running discography of all the newly found featured artists

for artist in artists:
    print(artist + " running")
    #get_discography(artist)
    get_featured_artist_discography(artist)
    print("done")
 