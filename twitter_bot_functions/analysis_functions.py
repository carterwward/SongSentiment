from firebase_functions import read_song_dict, read_artist_dict, read_all_discogs
from process import lyric_tokenizer
from model_functions import predict, tokenize_lyrics
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import plot_confusion_matrix
from sklearn import metrics
import re

def read_test_data():
    test = pd.read_csv("tokenized_test_data.csv").dropna()
    model = pickle.load(open('more_feature_model.sav', 'rb'))
    vectorizer = pickle.load(open('larger_vectorizer.pk', 'rb')) 
    vocab = vectorizer.get_feature_names()
    lyrics_list = test["tokenized_lyrics"].values
    predict_vectorizer = TfidfVectorizer(analyzer='word', lowercase=True, vocabulary= vocab)
    X_vals = predict_vectorizer.fit_transform(lyrics_list).toarray()
    Y_vals = test["lr_valence"]
    return model, vocab, X_vals, Y_vals

def read_train_data():
    train = pd.read_csv("tokenized_train_data.csv").dropna()
    model = pickle.load(open('more_feature_model.sav', 'rb'))
    vectorizer = pickle.load(open('larger_vectorizer.pk', 'rb')) 
    vocab = vectorizer.get_feature_names()
    lyrics_list = train["tokenized_lyrics"].values
    predict_vectorizer = TfidfVectorizer(analyzer='word', lowercase=True, vocabulary= vocab)
    X_train = predict_vectorizer.fit_transform(lyrics_list).toarray()
    Y_train = train["lr_valence"]
    return model, X_train, Y_train


def confusion_matrix(model, X_vals, Y_vals):
    fig, ax = plt.subplots(figsize=(8, 8))
    return plot_confusion_matrix(model, X_vals, Y_vals, ax=ax, values_format = '.5g')

#test data accuracy 0.5751724137931035
def test_accuracy(model, X_vals, Y_vals):
    return model.score(X_vals, Y_vals)


#graph 10 most positive and 10 most negative features
def feature_analysis(model, vocab):
    model_coef = ((model.coef_).transpose())
    df = pd.DataFrame(model_coef, columns=["Coefficient"])
    feature = pd.DataFrame(vocab, columns = ["Feature"])
    feature = pd.concat([feature, df], axis=1)
    top_10_neg = feature.sort_values(["Coefficient"])["Feature"].head(10)
    top_10_pos = feature.sort_values(["Coefficient"])["Feature"].tail(10)
    df = pd.concat([feature.sort_values(["Coefficient"]).head(10), feature.sort_values(["Coefficient"]).tail(10)])
    fig, ax = plt.subplots(figsize=(8, 8))
    return sns.barplot(x = "Coefficient", y = "Feature", data=df, ax=ax)

#create ROC curve
def ROC_curve(model, X_train, Y_train):
    return metrics.plot_roc_curve(model, X_train, Y_train)

def compare_auc():
    model, vocab, X_vals, Y_vals = read_test_data()
    model, X_train, Y_train = read_train_data()

    return ROC_curve(model, X_train, Y_train), ROC_curve(model, X_vals, Y_vals)


def get_accuracy(model, X_val, Y_val):
    return model.score(X_val, Y_val)

def get_test_predictions(test_csv):
    test = pd.read_csv(test_csv)
    model = pickle.load(open('model.sav', 'rb'))
    vectorizer = pickle.load(open('vectorizer.pk', 'rb')) 
    vocab = vectorizer.get_feature_names()
    lyrics_list = tokenize_lyrics(test["lyrics"].values)
    predict_vectorizer = TfidfVectorizer(analyzer='word', lowercase=True, vocabulary= vocab)
    predict_vector = predict_vectorizer.fit_transform(lyrics_list).toarray()
    return model.predict(predict_vector)

def most_important_words(artist_name, song_name):
    song_dict = read_song_dict(artist_name, song_name)
    tf_idf_df = get_song_tf_idf(song_dict, 20)

    words = list(tf_idf_df.index)
    tf_idf_scores = list(tf_idf_df['tfidf'])
    sns.barplot(x = tf_idf_scores, y = words)
    plt.title('TF-IDF Scores by Features for ' + song_name + ' by ' + artist_name)
    plt.xlabel('TF-IDF Scores')
    plt.ylabel('Features')
    plt.show()

def calculate_and_graph_tf(feature_list, tokenized_lyrics):
    feature_props = []
    for word in feature_list:
        term_count = 0
        for tokens in tokenized_lyrics:
            doc_count = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(word), tokens))
            if doc_count != 0:
                term_count +=1
        feature_props.append(term_count/len(tokenized_lyrics))
    return sns.distplot(feature_props)

def cross_validation(penalty):
    #read in train and test data
    model, X, y = read_train_data()
    model, vocab, X_vals, Y_vals = read_test_data()
    #train model with penalty
    clf = LogisticRegressionCV(penalty=penalty, solver='liblinear', max_iter = 10000).fit(X, y)
    #print model accuracy
    print(clf.score(X_vals,Y_vals))
    #get model parameters
    print(clf.get_params())
