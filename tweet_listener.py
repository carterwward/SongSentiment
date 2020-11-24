import tweepy
from twitter_cred import consumer_key, secret_key, access_key, access_secret
import time
from firebase import read_song_dict
from datetime import datetime, timedelta

def check_mentions(api, since_id, time_now):
    new_since_id = since_id

    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():

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
        print(song_dict['lyrics'])

        # TODO: retrieve top 4 words for song

        # TODO: retrieve positive vs. negative prediction from predict function

        # TODO: create response string

        user_handle = tweet.user.screen_name

        # api.update_status(+
        #     status= "@" + user_handle + " hello friend",
        #     in_reply_to_status_id=tweet.id
        # )
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
        time.sleep(15)

if __name__ == "__main__":
    main()
