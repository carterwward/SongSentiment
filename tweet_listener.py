import tweepy
from twitter_cred import consumer_key, secret_key, access_key, access_secret
import time

def check_mentions(api, since_id):
    # logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        
        if tweet.in_reply_to_status_id is not None:
            continue
        
        # logger.info(f"Answering to {tweet.user.name}")

        if not tweet.user.following:
            tweet.user.follow()
        

        user_handle = tweet.user.screen_name
        print(user_handle)
        api.update_status(
            status= "@" + user_handle + " hello friend",
            in_reply_to_status_id=tweet.id
        )
    return new_since_id

def main():
    auth = tweepy.OAuthHandler(consumer_key, secret_key)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    since_id = 1
    while True:
        since_id = check_mentions(api, since_id)
        # logger.info("Waiting...")
        time.sleep(10)

if __name__ == "__main__":
    main()
    