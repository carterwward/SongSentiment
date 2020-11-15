from firebase import read_song_dict, read_artist_dict
from process import lyric_tokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd

def build_model():
    # We will actually be getting all of the lyrics and valence scores for every discography, but for now we will use just one
    artist_name = "joy division"
    data_dict = read_artist_dict(artist_name)
    corpus = [song_dict['lyrics'] for song_dict in data_dict.values()]
    #Categorize valence and read into list
    lr_valence = [1 if song_dict['valence'] > 0.5 else 0 for song_dict in data_dict.values()]

    #read song names into list
    song_names = [song_name for song_name in data_dict.keys()]
    print(song_names)
    print(lr_valence)
    # print(corpus[2])
    # print(corpus[0])
    # Tokenize before hand using spacy
    tokenized_docs = [' '.join(lyric_tokenizer(doc)) for doc in corpus]

    # Create vectorizer object
    tfidf_vectorizer=TfidfVectorizer(analyzer='word', lowercase=True)
    # fit and transform tokenized lyrics
    tfidf_vectorizer_vectors=tfidf_vectorizer.fit_transform(tokenized_docs)

    # get tokens
    lyric_features = tfidf_vectorizer.get_feature_names()
    # Create
    tfidf_vectorizer_matrix = tfidf_vectorizer_vectors.toarray()
    print(tfidf_vectorizer_matrix)


# TODO: Turn this into a function that takes an artist name and song name and returns the top 3 tf-idf scores for that song
# retrieve first vector(tf-idf values for song at index 0)
# first_vector=tfidf_vectorizer_vectors[0]
# put tf-idf values for first vector in df to get a glance at TF-IDF values per song
# df = pd.DataFrame(first_vector.T.todense(), index=tfidf_vectorizer.get_feature_names(), columns=["tfidf"]) 
# df = df.sort_values(by=["tfidf"],ascending=False)
# print(df)

build_model()