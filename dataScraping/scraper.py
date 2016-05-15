#!/usr/bin/env python
import time
import os
from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener


consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
oauth_token = os.getenv('OAUTH_TOKEN')
oauth_token_secret = os.getenv('OAUTH_TOKEN_SECRET')


class listener(StreamListener):

    def on_data(self, raw_data):
        try:
            with open('twitterDB.txt', 'a') as fh:
                fh.write(raw_data)
            return True
        except BaseException as e:
            print 'Failed ondata {0}'.format(str(e))
            time.sleep(60)

    def on_error(self, status_code):
        print(status_code)

if __name__ == '__main__':
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(oauth_token, oauth_token_secret)
    twitterStreamn = Stream(auth, listener())
    twitterStreamn.filter(track=['syria' or 'refugee' or
                                 'syrian' or 'migrant crisis'])
