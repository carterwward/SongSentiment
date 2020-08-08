import en_core_web_sm
import re
import sys
import spacy
import json
import pandas as pd
import numpy as np

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


def tokenizer(doc):
    stops = ["yeah", '\n']
    nlp.Defaults.stop_words.update(stops)
    nlp.add_pipe(lemmatizer, name="lemmatizer", after="ner")
    nlp.add_pipe(remove_stopwords, name="stopwords", last=True)
    return nlp(doc)

if __name__ == "__main__":
    nlp = spacy.load('en_core_web_sm')
    discog_df = pd.read_csv('artists/saba.csv')
    lyrics = discog_df.iloc[0][3]
    # print(lyrics)
    doc = tokenizer(lyrics)
    print(doc)
