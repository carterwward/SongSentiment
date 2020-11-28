from firebase import read_song_dict, read_artist_dict, read_all_discogs
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
    model = pickle.load(open('model.sav', 'rb'))
    vectorizer = pickle.load(open('vectorizer.pk', 'rb')) 
    vocab = vectorizer.get_feature_names()
    # song_dict = read_song_dict(artist_name, song_name)

    lyr = [song_dict['lyrics']]

    lyrics_list = tokenize_lyrics(lyr)

    predict_vectorizer = TfidfVectorizer(analyzer='word', lowercase=True, vocabulary= vocab)
    predict_vector = predict_vectorizer.fit_transform(lyrics_list).toarray()

    return model.predict(predict_vector)[0]

def build_model():
    print('start')
    # We will actually be getting all of the lyrics and valence scores for every discography, but for now we will use just one
    # artist_name = "saba"
    print('reading entire database')
    data_dict = read_all_discogs()
    lr_valence = [1 if song_dict['valence'] > 0.5 else 0 for song_dict in data_dict.values()]
    data_pd = pd.DataFrame.from_dict(data_dict, orient='index').drop(columns = ["year", "album", "features"])
    data_pd["lr_valence"] = lr_valence

    
    # Split data into train and test dfs
    train, test = train_test_split(data_pd, test_size=0.25, random_state=42)
    train.to_csv('train_data.csv')
    test.to_csv('test_data.csv')
    # use function to get train tokenized documents
    print('begin tokenization')
    train_lyrics_list = tokenize_lyrics(train["lyrics"].values)
    #print(train_lyrics_list)
    # Create vectorizer object 
    train_vectorizer = TfidfVectorizer(analyzer='word', lowercase=True, max_df = 0.95, min_df=0.05)
    # fit and transform tokenized lyrics
    X_train = train_vectorizer.fit_transform(train_lyrics_list).toarray()
    # save vectorizer
    print('save vectorizer')
    with open('vectorizer.pk', 'wb') as fin:
        pickle.dump(train_vectorizer, fin)

    Y_train = train["lr_valence"].values
    train_vocab = train_vectorizer.get_feature_names()
    
    # calculating X_test, Y_test
    # test_lyrics_list = tokenize_lyrics(test["lyrics"].values)
    # test_vectorizer = TfidfVectorizer(analyzer='word', lowercase=True, vocabulary = train_vocab)
    # X_test = test_vectorizer.fit_transform(test_lyrics_list).toarray()
    # Y_test = test["lr_valence"].values
    
    
    # get vector of trained lr_valences   
    print('save model')
    model = LogisticRegression(max_iter = 10000).fit(X_train, Y_train)
    pickle.dump(model, open('model.sav', 'wb'))


