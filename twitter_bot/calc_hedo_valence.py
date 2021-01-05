"""Program will leverage hedonometer scores from computational story lab at UVM to calculate a valence
score for lyrics of song based on the average valence score of the tokens that appear in the 
hedonometer dataset"""

import firebase
from process import lyric_tokenizer
import pandas as pd
import os

def calc_hedo_valence(tok_lyrics, hedo_df, word_valence_dict):
    available_set = set(tok_lyrics) & set(hedo_df['Word'].values)
    available_lyrics = [word for word in tok_lyrics if word in available_set]
    valence_scores = [word_valence_dict[word] for word in available_lyrics]
    return sum(valence_scores) / len(valence_scores)

# TODO: write function to pull all firebase songs, calculate valence, and update fb

# TODO: write function to calculate valence for artist

# TODO: write function to calculate valence for album

# TODO: FOR ANALYSIS: scatter plot of hedo word happiness scores and associations scores from model

# TODO: FOR ANALYSIS: scatter plot of song valence scores from spotify and hedo calculated song valence scores

# TODO: Train new model on hedonometer valence scores

if __name__ == '__main__':
    lyrics = firebase.read_song_dict('99 neighbors', '19')['lyrics']
    tok_lyrics = lyric_tokenizer(lyrics)
    hedonometer = pd.read_csv("data_and_models/Hedonometer.csv")
    word_valence_dict = {row['Word']: row['Happiness Score'] for index, row in hedonometer.iterrows()}
    print(calc_hedo_valence(tok_lyrics, hedonometer, word_valence_dict))

