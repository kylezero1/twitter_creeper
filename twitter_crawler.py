from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import os

import twitter_credentials

class TwitterStreamer():

    def __init__(self):
        pass
    def stream_tweets(self, fetched_tweets_filename):
        listener = StdOutListener(fetched_tweets_filename)

        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

        stream = Stream(auth, listener)
        
        stream.filter(locations=[-125.0011, 24.9493, -66.9326, 49.5904]) #bounding box for the United States
        #stream.sample()

class StdOutListener(StreamListener):

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename
        self.count = 0

    def on_data(self, data):
        try:           
            if self.count >= 500:
                return False

            self.fetched_tweets_filename = "tweets" + str(self.count) + ".json"                        

            b = os.stat(self.fetched_tweets_filename)
            #1048576 = roughly 1MB in bytes
            #10485760 = roughly 10MB in bytes
            if b.st_size < 10485760:
                with open(self.fetched_tweets_filename, 'a') as tf:
                    print(data)
                    tf.write(data)
                    tf.write(',')
                    tf.close()
                return True
            else: #if file surpasses file size                
                with open(self.fetched_tweets_filename, 'rb+') as filehandle: #to remove the last tweet's ','
                        filehandle.seek(-1, os.SEEK_END)
                        filehandle.truncate()
                        filehandle.close()
                with open(self.fetched_tweets_filename, 'a') as tf: #adds bracket at the end of the document                    
                    tf.write(']')
                    tf.close()

                self.count += 1
                if self.count >= 500:
                    return False

                self.fetched_tweets_filename = "tweets" + str(self.count) + ".json" #creates next file                        
                f = open(self.fetched_tweets_filename, "w+")
                f.close()   
                with open(self.fetched_tweets_filename, 'a') as tf:
                    tf.write('[')
                    tf.close()       
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
    
    def on_error(self, status):
        print(status)

if __name__ == '__main__':

    fetched_tweets_filename = "tweets"

    f = open("tweets0.json", "w+")
    f.write('[')
    f.close()

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename)   