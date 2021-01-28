"""Program will leverage hedonometer scores from computational story lab at UVM to calculate a valence
score for lyrics of song based on the average valence score of the tokens that appear in the 
hedonometer dataset"""

from process import lyric_tokenizer
import firebase
import pandas as pd
import os

def calc_hedo_valence(tok_lyrics, hedo_df, word_valence_dict):
    available_set = set(tok_lyrics) & set(hedo_df['Word'].values)
    # print(tok_lyrics)
    available_lyrics = [word for word in tok_lyrics if word in available_set]
    valence_scores = [word_valence_dict[word] for word in available_lyrics]
    return sum(valence_scores) / len(valence_scores)


# TODO: write function to pull all firebase songs, calculate valence, and update fb
# def calc_hedo_valence_update_fb():
#     print('start')
#     print('reading entire database')
#     data_dict = firebase.read_all_discogs()
#     for song in data_dict:
#         lyrics = song['lyrics']
#         tok_lyrics = lyric_tokenizer(lyrics)


def calc_artist_hedo_valence(artist, hedo_df, word_valence_dict):
    artist_dict = firebase.read_artist_dict(artist)
    sum_valence = 0
    len_valence = 0
    for key in artist_dict.keys():
        print(key)
        if artist_dict[key]['lyrics'] == '':
            continue
        tok_lyrics = lyric_tokenizer(artist_dict[key]['lyrics'])
        valence = (calc_hedo_valence(tok_lyrics, hedo_df, word_valence_dict))
        # print(valence)
        sum_valence += valence
        len_valence += 1
    # print(sum_valence)
    return(sum_valence/len_valence)

# TODO: write function to calculate valence for album

# TODO: Train new model on hedonometer valence scores

if __name__ == '__main__':
    lyrics = firebase.read_song_dict('frank ocean', 'self control')['lyrics']
    tok_lyrics = lyric_tokenizer(lyrics)
    hedonometer = pd.read_csv("data_and_models/Hedonometer.csv")
    word_valence_dict = {row['Word']: row['Happiness Score'] for index, row in hedonometer.iterrows()}
    print(calc_hedo_valence(tok_lyrics, hedonometer, word_valence_dict))
    # print(calc_artist_hedo_valence('99 neighbors', hedonometer, word_valence_dict))

