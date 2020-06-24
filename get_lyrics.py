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
try:
    nlp = spacy.load("en_core_web_sm")
except:
    nlp = en_core_web_sm.load()


def get_discography(artist):
    disco = genius.search_artist(artist, max_songs=3)

    data = np.empty((0,7))

    for song in disco.songs:
        # features = ", ".join([item["name"] for item in song.featured_artists])
        # try:
        #     print(features.encode('ascii', 'ignore').decode())
        # except IndexError:
        #     print(features)
        data = np.vstack((data, np.asarray([song.title, song.artist, song.lyrics, song.album, song.year, 
                         ", ".join([item["name"] for item in song.featured_artists]).encode('ascii', 'ignore').decode(), 
                         song.producer_artists],object)))
    df = pd.DataFrame(data, columns=["title", "artist", "lyrics", "album", "year", "featured_artists", "producers"])
    df.to_csv("artists/" + artist +".csv")


# TODO: Write function to correct capitalization according to entities and add to pipeline.

def lemmatizer(doc):
    # This takes in a doc of tokens from the NER and lemmatizes them.
    # Pronouns (like "I" and "you" get lemmatized to '-PRON-', so I'm removing those.
    # TODO: change logic to try to map pronoun to last identified proper noun and replace.
    doc = [token.lemma_ for token in doc if token.lemma_ != "-PRON-"]
    doc = u" ".join(doc)
    return nlp.make_doc(doc)

def remove_stopwords(doc):
    # TODO: add words for sections of songs,
    doc = [token for token in doc if token.is_stop != True and token.is_punct != True and token.is_digit != True and token.is_space != True]
    return doc

def tokenizer(doc):
    stops = ["yeah", '\n']
    nlp.Defaults.stop_words.update(stops)
    nlp.add_pipe(lemmatizer, name="lemmatizer",after="ner")
    nlp.add_pipe(remove_stopwords, name="stopwords", last=True)
    return nlp(doc)


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
# # custom = spacy.load('en_core_web_sm')

# title = "sicko mode"
# artist = "travis scott"

# lyrics = genius.search_song(title, artist).to_text()
# # document = custom(lyrics)
# # for token in document:
# #     print(token,token.ent_type_)
# tokens = tokenizer(lyrics)
# print(tokens)

get_discography("saba")
