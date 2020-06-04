
import tweepy

def authenticate():
    CONSUMER_KEY = 'gZaCT9FHyYaxucFQnE9pVvzxa'
    CONSUMER_SECRET = '9Sk3veYThrQawinJhFGq9taewVDtqCX6jwBp84FdYaLQNgwHO6'
    ACCESS_TOKEN = '1070010671918665728-smESXV5NypkHDnXQggAgH7okAgXedd'
    ACCESS_TOKEN_SECRET = 'BEYi2lrZ8ptRoRTWOF5XN2opRzu3D2SIx7Ywn9UnxPOpA'
    
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
    return api
