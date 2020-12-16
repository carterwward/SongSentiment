from firebase import read_song_dict
from process import lyric_tokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import numpy as np
import pandas as pd

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
