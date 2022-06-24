import tweepy
import sys
import csv

#https://www.loginradius.com/blog/engineering/beginners-guide-to-tweepy/
#https://stackoverflow.com/questions/44948628/how-to-take-all-tweets-in-a-hashtag-with-tweepy?answertab=scoredesc#tab-top

query = sys.argv[1]


# TODO: Insert API Keys below
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


tweets = {}
for tweet in tweepy.Cursor(api.search, q=query, rpp=100).items():
    tweets[query].append(tweet)
    print(tweet)

with open("tweets.csv", "w") as csvFile:
    csvWriter = csv.DictWriter(csvFile)
    csvWriter.writeheader()
    csvWriter.writerows(tweets)