from firebase_functions import read_song_dict, read_artist_dict, read_all_discogs
from process import lyric_tokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd
import pickle

def tokenize_lyrics(lyrics_list):
    return [' '.join(lyric_tokenizer(doc)) for doc in lyrics_list]

def predict(song_dict):
    model = pickle.load(open('data_and_models/model.sav', 'rb'))
    vectorizer = pickle.load(open('data_and_models/vectorizer.pk', 'rb')) 
    vocab = vectorizer.get_feature_names()

    lyr = [song_dict['lyrics']]

    lyrics_list = tokenize_lyrics(lyr)

    predict_vectorizer = TfidfVectorizer(analyzer='word', lowercase=True, vocabulary= vocab)
    predict_vector = predict_vectorizer.fit_transform(lyrics_list).toarray()

    return model.predict(predict_vector)

def get_song_tf_idf(data_dict, num_features):
    # TODO: Use spacies entity attribute to sort tf_idf values based on entities
    # TODO: then create an actual summary sentence from the top words using the different parts of speech
    vectorizer = pickle.load(open('data_and_models/vectorizer.pk', 'rb')) 
    vocab = vectorizer.get_feature_names()
    tfidf_vectorizer = TfidfVectorizer(analyzer='word', lowercase=True, vocabulary= vocab)

    doc =  [' '.join([lyric for lyric in lyric_tokenizer(data_dict['lyrics']) if 'igg' not in lyric])]

    tfidf_vectorizer_vectors=tfidf_vectorizer.fit_transform(doc)

    song_vector = tfidf_vectorizer_vectors[0]

    df = pd.DataFrame(song_vector.T.todense(), index=tfidf_vectorizer.get_feature_names(), columns=["tfidf"]) 
    df = df.sort_values(by=["tfidf"],ascending=False)
    return df.head(num_features)

