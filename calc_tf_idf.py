from firebase import read_song_dict, read_artist_dict
from process import lyric_tokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd

def get_song_tf_idf(artist_name, song_name):
    tfidf_vectorizer=TfidfVectorizer(analyzer='word', lowercase=True)
    song_name = song_name.lower()
    # TODO: add same cleaning as song names from genius and spotify

    data_dict = read_artist_dict(artist_name)
    corpus = [' '.join(lyric_tokenizer(song_dict['lyrics'])) for song_dict in data_dict.values()]
    tfidf_vectorizer_vectors=tfidf_vectorizer.fit_transform(corpus)

    song_index = list(data_dict.keys()).index(song_name)
    song_vector = tfidf_vectorizer_vectors[song_index].toarray()
    return song_vector
    df = pd.DataFrame(song_vector.T.todense(), index=tfidf_vectorizer.get_feature_names(), columns=["tfidf"]) 
    df = df.sort_values(by=["tfidf"],ascending=False)
    print(df.head(20))
    # print(song_vector.toarray())


get_song_tf_idf('saba', "gps")

# TODO: Turn this into a function that takes an artist name and song name and returns the top 3 tf-idf scores for that song
# retrieve first vector(tf-idf values for song at index 0)
# first_vector=tfidf_vectorizer_vectors[0]
# put tf-idf values for first vector in df to get a glance at TF-IDF values per song
# df = pd.DataFrame(first_vector.T.todense(), index=tfidf_vectorizer.get_feature_names(), columns=["tfidf"]) 
# df = df.sort_values(by=["tfidf"],ascending=False)
# print(df)

# build_model()