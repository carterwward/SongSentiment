import tweepy
from twitter_cred import consumer_key, secret_key, access_key, access_secret
from calc_tf_idf import get_song_tf_idf
import time
from firebase import read_song_dict
from datetime import datetime, timedelta
from model import predict

def check_mentions(api, since_id, time_now):
    new_since_id = since_id
    print('new check')

    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        user_handle = tweet.user.screen_name


        new_since_id = max(tweet.id, new_since_id)

        if time_now > tweet.created_at:
            continue

        print('new tweet since id', new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue

        if not tweet.user.following:
            tweet.user.follow()
        
        # Parse user input
        tweet_input = tweet.text.replace('@musicpsychic2', '')
        separator = tweet_input.find(',')
        song_name = tweet_input[:separator].strip()
        artist_name = tweet_input[separator+1:].strip()

        print(artist_name)
        print(song_name)

        # Retrieve song dictionary
        song_dict = read_song_dict(artist_name, song_name)
        # print(song_dict['valence'])
        
        if song_dict == {}:
            api.update_status(
            status= "@" + user_handle + " I can't find the song " + song_name + " or the artist " + artist_name + " please check your spelling and the list of artists I have data on in my pinned tweet.",
            in_reply_to_status_id=tweet.id
            )
            continue


        # retrieve top 5 words for song
        rank_df = get_song_tf_idf(song_dict, 5)
        # retrieve positive vs. negative prediction from predict function
        song_pred = predict(song_dict)

        # create response string
        # Change response to say: artist talks about blank, blank, ... and blank to convey generally ___ emotions
        response = ' ' + artist_name + ' uses words like'
        for word in rank_df.index:
            response += ' ' + word + ',' 
        response += ' to convey '

        if song_pred == 1:
            response += "generally positive emotions in " + song_name + '.'
        else:
            response += "generally negative emotions in " + song_name + '.'

        api.update_status(
            status= "@" + user_handle + response,
            in_reply_to_status_id=tweet.id
        )
    return new_since_id

def main():
    auth = tweepy.OAuthHandler(consumer_key, secret_key)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    time_now = datetime.now() + timedelta(hours=5)

    since_id = 1
    print('current time', time_now)

    while True:
        since_id = check_mentions(api, since_id, time_now)
        time.sleep(10)

if __name__ == "__main__":
    main()
