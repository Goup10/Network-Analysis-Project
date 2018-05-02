#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from time import sleep
import time

#Variables that contains the user credentials to access Twitter API
access_token = "980431212350238720-7SwVvcqmFZBBt7NYMRCEicgQ50rcFw9"
access_token_secret = "8us1aIfKzlcJ5vDmq7XKWqy7fijKB5Jx8N9UzXslrQshF"
consumer_key = "UpKh3aM48Xm0SbZZaz7CoAxtP"
consumer_secret = "PS7boO4EOSLz7aUlUWluMSyNWDJ3EVEyLaS7xBXemq5NY2Y3gi"


class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        try:
            print(data)
            saveFile = open('newtweets.csv', 'a')
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
