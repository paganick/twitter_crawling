import tweepy

def authenticate():
    CONSUMER_KEY = 'zpYi7cVxYpQizxjHqElyO5Yhx'
    CONSUMER_SECRET = 'BTF8TQK6UnXs9e7QyXSCkbWywrXUIFFGKpaZrY3TXJ5F6jBCls'
    ACCESS_TOKEN = '1070010671918665728-55mOCtb3uxmRKh9dvYWWgthc79yGmj'
    ACCESS_TOKEN_SECRET = 'FLjTbGbGam9EJ7uilSuykQ5MdZ6Wg1e9EN8cC8zNnW7h0'
    
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
    return api
