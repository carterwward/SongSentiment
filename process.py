import en_core_web_sm
import re
import sys
import spacy
import json
import pandas as pd
import numpy as np
# from firebase_write import read_artist_dict

try:
    nlp = spacy.load("en_core_web_sm")
except:
    nlp = en_core_web_sm.load()

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
    doc = [token for token in doc if token.is_stop != True and token.is_punct !=
           True and token.is_digit != True and token.is_space != True]
    return doc


def lyric_tokenizer(doc):
    nlp = spacy.load('en_core_web_sm')
    stops = ["yeah", '\n', 'intro', 'hook', 'verse', 'yes', 'oh', 'chorus', 'like', 'hey', 'okay',
    'uh', 'blah', 'ooooooh', 'woah', 'la', 'aight', 'whoa', 'til', 'o', 'huh']
    nlp.Defaults.stop_words.update(stops)
    nlp.add_pipe(lemmatizer, name="lemmatizer", after="ner")
    nlp.add_pipe(remove_stopwords, name="stopwords", last=True)
    return nlp(doc)


# if __name__ == "__main__":
#     #gets an artist's full dictionary
#     discog = read_artist_dict("99 neighbors")
#     for song in discog.values():
#         lyrics = song["lyrics"]
#         lyrics = lyrics.lower()
#         doc = tokenizer(lyrics)
#         print(doc,"\n\n")
#     #gets just an artist's song
#     # song = read_song_dict()
#     # lyrics = song['lyrics']
#     # doc = tokenizer(lyrics)
#     # print(doc)

