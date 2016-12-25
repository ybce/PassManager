import tweepy
import json

consumer_key = "rsv3Zl11ZblMg7JCyQ5IAvP0c"
consumer_secret = "PFbdNriK0IhroXGZzFyt7I0ZehnTfUWdIi59U6n7M1Q2ynOtTQ"
access_token = "803042454568103937-zhviYoiS4SYmwBD0uA7jvSBkYoBgdGP"
access_token_secret = "56MZd3yGZXXa67DVCMJQ9DvtT0yiyrISWQpanGcdiIHnJ"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


#override tweepy.StreamListener to add logic to on_status

class MyStreamListener(tweepy.StreamListener):
    #def on_status(self, status):
    #    with open('twitter_stream.txt', 'a') as f:
    #        f.seek(0)
    #        f.write(status)
    #    return True

    def on_data(self, data):
        all_data = json.loads(data)

        tweet = all_data["text"].encode('utf-8')
        username = all_data["user"]["screen_name"]
        print((username,tweet))

        #Open, write and close your file.
        savefile = open('nirvana.txt', 'ab')
        savefile.write(tweet)
        savefile.close()

        return True


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

myStream.filter(track=['Nirvana'], languages=['en'])
