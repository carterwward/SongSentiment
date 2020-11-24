from firebase import read_song_dict
from process import lyric_tokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import numpy as np
import pandas as pd

def get_song_tf_idf(artist_name, song_name, num_features):
    vectorizer = pickle.load(open('vectorizer.pk', 'rb')) 
    vocab = vectorizer.get_feature_names()
    tfidf_vectorizer = TfidfVectorizer(analyzer='word', lowercase=True, vocabulary= vocab)

    data_dict = read_song_dict(artist_name, song_name)
    doc =  [' '.join([lyric for lyric in lyric_tokenizer(data_dict['lyrics']) if 'igg' not in lyric])]

    tfidf_vectorizer_vectors=tfidf_vectorizer.fit_transform(doc)

    # song_index = list(data_dict.keys()).index(song_name)
    song_vector = tfidf_vectorizer_vectors[0]
    # return song_vector
    df = pd.DataFrame(song_vector.T.todense(), index=tfidf_vectorizer.get_feature_names(), columns=["tfidf"]) 
    df = df.sort_values(by=["tfidf"],ascending=False)
    return df.head(num_features)


print(get_song_tf_idf('saba', "westside bound 3", 5))
