import lyricsgenius
from credentials import client_access_token
import re
import sys
import spacy
import json

genius = lyricsgenius.Genius(client_access_token)
genius.verbose = False
nlp = spacy.load("en_core_web_sm")

def get_discography(artist):
    return


def lemmatizer(doc):
    # This takes in a doc of tokens from the NER and lemmatizes them.
    # Pronouns (like "I" and "you" get lemmatized to '-PRON-', so I'm removing those.
    doc = [token.lemma_ for token in doc if token.lemma_ != "-PRON-"]
    doc = u"".join(doc)
    return nlp.make_doc(doc)

def remove_stopwords(doc):
    doc = [token.text for token in doc if token.is_stop != True and token.is_punct != True and token.is_digit != True and token.is_space != True]
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

title = "sicko mode"
artist = "travis scott"

lyrics = genius.search_song(title, artist).to_text()
tokens = tokenizer(lyrics)
print(tokens)
