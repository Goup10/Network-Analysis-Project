#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from time import sleep
import time

#Variables that contain the user credentials to access Twitter API
#All following tokens have been removed as a protection of my privacy
#You can create your own tokens at: https://apps.twitter.com/ 
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""


class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        try:
            print(data)
            saveFile = open('newtweets.txt', 'a')
            saveFile.write(data)
            saveFile.close()
            return True
        except BaseException:
            print ('failed ondata')
            time.sleep(5)

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    auth.secure = True

    stream.filter(locations=[-0.351468,51.38494,0.148271,51.672343])
