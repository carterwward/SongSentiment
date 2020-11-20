from firebase import read_song_dict, read_artist_dict
from process import lyric_tokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd

def tokenize_lyrics(lyrics_list):
    return [' '.join(lyric_tokenizer(doc)) for doc in lyrics_list]

def predict(artist_name, song_name):
    model = build_model()
    song_dict = read_song_dict(artist_name, song_name)
    song_pd = pd.DataFrame.from_dict(song_dict, orient='index').drop(["year", "album", "features"])
    lyr = song_pd.values[0]
    lyrics_list = tokenize_lyrics(lyr)
    model.predict(lyrics_list)


def build_model():
    # We will actually be getting all of the lyrics and valence scores for every discography, but for now we will use just one
    artist_name = "saba"
    data_dict = read_artist_dict(artist_name)
    lr_valence = [1 if song_dict['valence'] > 0.5 else 0 for song_dict in data_dict.values()]
    data_pd = pd.DataFrame.from_dict(data_dict, orient='index').drop(columns = ["year", "album", "features"])
    data_pd["lr_valence"] = lr_valence
    #print(data_pd)
    
    # Split data into train and test dfs
    train, test = train_test_split(data_pd, test_size=0.1, random_state=42)
    # use function to get train tokenized documents
    train_lyrics_list = tokenize_lyrics(train["lyrics"].values)
    #print(train_lyrics_list)
    # Create vectorizer object 
    train_vectorizer = TfidfVectorizer(analyzer='word', lowercase=True)
    # fit and transform tokenized lyrics
    X_train = train_vectorizer.fit_transform(train_lyrics_list).toarray()
    Y_train = train["lr_valence"].values
    train_vocab = train_vectorizer.get_feature_names()
    
    # calculating X_test, Y_test
    test_lyrics_list = tokenize_lyrics(test["lyrics"].values)
    test_vectorizer = TfidfVectorizer(analyzer='word', lowercase=True, vocabulary = train_vocab)
    X_test = test_vectorizer.fit_transform(test_lyrics_list).toarray()
    Y_test = test["lr_valence"].values
    
    #print(X_test)
    
    # get vector of trained lr_valences   

    #model = LogisticRegression(max_iter = 10000).fit(X_train, Y_train)
    #return model

#build_model() 
predict("dead kennedys", 'holiday in cambodia')