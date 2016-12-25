import tweepy
import sys
import itertools
import time
import emoji

reload(sys)
sys.setdefaultencoding('utf-8')

consumer_key = "rsv3Zl11ZblMg7JCyQ5IAvP0c"
consumer_secret = "PFbdNriK0IhroXGZzFyt7I0ZehnTfUWdIi59U6n7M1Q2ynOtTQ"
access_token = "803042454568103937-zhviYoiS4SYmwBD0uA7jvSBkYoBgdGP"
access_token_secret = "56MZd3yGZXXa67DVCMJQ9DvtT0yiyrISWQpanGcdiIHnJ"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

suits = ['H', 'C', 'S', 'D']
numbers = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
emojis = {'H': '\u2665', 'C': '\u2663', 'S': '\u2660',
          'D': '\u2666'}  # Dictionairy to hold unicode representation of the suits
deck = list(itertools.product(numbers, suits))  # creating deck of cards
combs = itertools.combinations(deck, 13)  # creating all possible 13 card hands in a deck

hand = combs.next()  # fetching next combination from the generator

handList = ""  # Converting the tuple returned from the generator into a string

for i in range(0, 13):
    handList += hand[i][0] + hand[i][1]

hands = list(handList)  # Converting string into a list so I can replace characters

for i in range(0, len(hands)):  # Replacing letters for emojis from the dictionary

    if hands[i] == 'C':
        hands[i] = emojis['C']
    elif hands[i] == 'H':
        hands[i] = emojis['H']
    elif hands[i] == 'D':
        hands[i] = emojis['D']
    elif hands[i] == 'S':
        hands[i] = emojis['S']

tweet = unicode("")
for i in range(0, len(hands), 2):
    tweet += u'%s %s ' % (hands[i], hands[i + 1])

print tweet
tweet2 = u'4 \u2660' + u' 4 \u2663'
print tweet2

api.update_status(tweet2)

user = api.user_timeline('Hand_Generator')
i = 1
for tweets in user:
    print "Tweet %d: " % (i) + tweets.text.encode('utf-8')
    i = i + 1

results = api.search(q="Ronaldo")
for result in results:
    if result.lang == "en":
        print "Tweet %d: " % (i) + result.text.encode('utf-8')
    i = i + 1

# api.update_status(tweet2)




