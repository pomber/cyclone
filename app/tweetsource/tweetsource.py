from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

class TweetSource(StreamListener):
  
    def __init__(self, listener, config): 
        super(TweetSource, self).__init__()

        consumer_key = config["twitter.consumer-key"]
        consumer_secret = config["twitter.consumer-secret"]
        access_token = config["twitter.access-token"]
        access_token_secret = config["twitter.access-token-secret"]
        keywords_to_track = config["twitter.keywords-to-track"]
        locations_to_track = config["twitter.locations-to-track"]

        self._listener = listener
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        stream = Stream(auth, self)
        stream.filter(track=keywords_to_track, locations=locations_to_track, async=True)

    def on_status(self, status):
        text = status.text.replace("\n","|")
        if not text.lower().startswith("rt"):
            self._listener.new_document(text)
        return True

    def on_error(self, status_code):
        print 'Encountered error with status code:', status_code
        return True
    
    def on_timeout(self):
        print 'Timeout...'
        return True