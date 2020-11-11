from firebase import read_song_dict, read_artist_dict
from process import lyric_tokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def calculate_tf_idf():
    print('h')

tfidf_vectorizer = TfidfVectorizer(tokenizer =lyric_tokenizer)

artist_name = "joy division"
corpus = [song_dict['lyrics'] for song_dict in read_artist_dict(artist_name).values()]
lyrics = read_song_dict(artist_name, 'isolation')['lyrics']
tfidf_values = tfidf_vectorizer.fit_transform(corpus)
response = tfidf_vectorizer.transform([lyrics])

feature_array = np.array(tfidf_vectorizer.get_feature_names())
tfidf_sorting = np.argsort(response.toarray()).flatten()[::-1]

n = 3

top_n = feature_array[tfidf_sorting]

print(top_n)
