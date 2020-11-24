from firebase import read_song_dict, read_artist_dict, read_all_discogs
from process import lyric_tokenizer
from model import predict, tokenize_lyrics
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import plot_confusion_matrix
from sklearn import metrics

def read_test_data():
    test = pd.read_csv("test_data.csv").dropna()
    model = pickle.load(open('model.sav', 'rb'))
    vectorizer = pickle.load(open('vectorizer.pk', 'rb')) 
    vocab = vectorizer.get_feature_names()
    lyrics_list = tokenize_lyrics(test["lyrics"].dropna().values)
    predict_vectorizer = TfidfVectorizer(analyzer='word', lowercase=True, vocabulary= vocab)
    X_vals = predict_vectorizer.fit_transform(lyrics_list).toarray()
    Y_vals = test["lr_valence"]
    return model, vocab, X_vals, Y_vals

def read_train_data():
    train = pd.read_csv("train_data.csv").dropna()
    model = pickle.load(open('model.sav', 'rb'))
    vectorizer = pickle.load(open('vectorizer.pk', 'rb')) 
    vocab = vectorizer.get_feature_names()
    lyrics_list = tokenize_lyrics(train["lyrics"].values)
    predict_vectorizer = TfidfVectorizer(analyzer='word', lowercase=True, vocabulary= vocab)
    X_train = predict_vectorizer.fit_transform(lyrics_list).toarray()
    Y_train = train["lr_valence"]
    return model, X_train, Y_train


def confusion_matrix(model, X_vals, Y_vals):
    fig, ax = plt.subplots(figsize=(8, 8))
    plot_confusion_matrix(model, X_vals, Y_vals, ax=ax, values_format = '.5g')

#test data accuracy 0.5696551724137932
def test_accuracy(model, X_vals, Y_vals):
    val_accuracy = model.score(X_vals, Y_vals)
    print("Validation Accuracy: ", val_accuracy)


#graph 10 most positive and 10 most negative features
def feature_analysis(model, vocab):
    model_coef = ((model.coef_).transpose())
    df = pd.DataFrame(model_coef, columns=["Coefficient"])
    feature = pd.DataFrame(vocab, columns = ["Feature"])
    feature = pd.concat([feature, df], axis=1)
    top_10_neg = feature.sort_values(["Coefficient"])["Feature"].head(10)
    top_10_pos = feature.sort_values(["Coefficient"])["Feature"].tail(10)
    df = pd.concat([feature.sort_values(["Coefficient"]).head(10), feature.sort_values(["Coefficient"]).tail(10)])
    print(type(df))
    print("Words most negatively associated:",top_10_neg)
    print("Words most positively associated:",top_10_pos)
    fig, ax = plt.subplots(figsize=(8, 8))
    plot = sns.barplot(x = "Coefficient", y = "Feature", data=df, ax=ax)

#create ROC curve
def ROC_curve(model, X_train, Y_train):
    metrics.plot_roc_curve(model, X_train, Y_train)

#train data accuracy 0.6972350230414747
def train_accuracy(model, X_train, Y_train):
    val_accuracy = model.score(X_train, Y_train)
    print("Validation Accuracy: ", val_accuracy)

def get_test_predictions(test_csv):
    test = pd.read_csv(test_csv)
    model = pickle.load(open('model.sav', 'rb'))
    vectorizer = pickle.load(open('vectorizer.pk', 'rb')) 
    vocab = vectorizer.get_feature_names()
    lyrics_list = tokenize_lyrics(test["lyrics"].values)
    predict_vectorizer = TfidfVectorizer(analyzer='word', lowercase=True, vocabulary= vocab)
    predict_vector = predict_vectorizer.fit_transform(lyrics_list).toarray()
    return model.predict(predict_vector)



