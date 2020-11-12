from firebase import read_song_dict, read_artist_dict
from process import lyric_tokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd

def calculate_tf_idf():
    print('h')

# Get list of lyrics for discography
artist_name = "joy division"
corpus = [song_dict['lyrics'] for song_dict in read_artist_dict(artist_name).values()]

# Tokenize before hand using spacy
tokenized_docs = [' '.join(lyric_tokenizer(doc)) for doc in corpus]

# Create vectorizer object
tfidf_vectorizer=TfidfVectorizer(analyzer='word', lowercase=True) 
# fit and transform tokenized lyrics
tfidf_vectorizer_vectors=tfidf_vectorizer.fit_transform(tokenized_docs)

# print features in discography
print(tfidf_vectorizer.get_feature_names())
# retrieve first vector(tf-idf values for song at index 0)
first_vector=tfidf_vectorizer_vectors[0]
# put tf-idf values for first vector in df to get a glance
df = pd.DataFrame(first_vector.T.todense(), index=tfidf_vectorizer.get_feature_names(), columns=["tfidf"]) 
df = df.sort_values(by=["tfidf"],ascending=False)
print(df)
