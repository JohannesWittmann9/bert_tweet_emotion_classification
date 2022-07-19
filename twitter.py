# Necessary imports
import csv
import os
import sys
import random
import pandas as pd
import tweepy
from configparser import ConfigParser

# Load twitter developer keys and tokens through a local config file
config = ConfigParser()
config.read('./keys.cfg')

consumer_key = config.get('twitter', 'consumer_key')
consumer_secret = config.get('twitter', 'consumer_secret')
access_token = config.get('twitter', 'access_token')
access_token_secret = config.get('twitter', 'access_token_secret')
bearer_token = config.get('twitter', 'bearer_token')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Initialize tweepy api
api = tweepy.API(auth, wait_on_rate_limit=True) #, wait_on_rate_limit_notify=True

# Set total number of retrieved tweets
numOfTotalTweets = 100

# Twitter Dataset must be in the same directory as the script
dirs = next(os.walk("RussoUkrainianWar_Dataset-main"))[1] 
print(dirs)

numOfTweetsPerFolder = int(numOfTotalTweets/len(dirs))

print(numOfTweetsPerFolder)

# Create random indices for choosing tweets per day
def getRandomIndices(amount, length):
    inxAmount = amount
    if amount > length:
        inxAmount = length
    indices = []
    for i in range(0, inxAmount):
        randInt = random.randint(0, inxAmount-1)
        while randInt in indices:
            randInt = random.randint(0, inxAmount-1)
        indices.append(randInt)
    return indices

# Storing tweet ids by date
tweet_ids = {}

# Load and choose tweets
for folder in dirs:
    files = next(os.walk(f"RussoUkrainianWar_Dataset-main/{folder}"))[2]
    numFiles = len(files)
    tweetsPerFile = int(numOfTweetsPerFolder/numFiles)
    print(tweetsPerFile*numFiles)
    for file in files:
        if not file.startswith("."):
            with open(f"./RussoUkrainianWar_Dataset-main/{folder}/{file}", "r") as f:
                arr = []
                if folder in tweet_ids.keys():
                    arr = tweet_ids[folder]
                newIds = f.read().split("\n")
                rndmIndices = getRandomIndices(tweetsPerFile, len(newIds))
                for idx in rndmIndices:
                    arr.append(newIds[idx])
                tweet_ids[folder] = arr


# Write files with chosen ids per month
for month in tweet_ids.keys():
    if not os.path.exists('output'):
        os.mkdir('output')
    with open(f'./output/{month}-ids.txt', 'w') as f: 
        for i in range(0, len(tweet_ids[month])):
            tweet = tweet_ids[month][i]
            if i < len(tweet_ids[month])-1:
                f.writelines(tweet+"\n")
            else:
                f.writelines(tweet)


tweets = {}
counter = 0
# Crawl Tweets and Userdata
for date in tweet_ids:
    arr = []
    if date in tweets.keys():
        arr = tweets[date]
    for tweet_id in tweet_ids[date]:
        tweet_obj = {}
        counter = counter + 1
        print("Trying to fetch data for tweet No."+str(counter))
        try:
            tweet = api.get_status(tweet_id)
        except tweepy.errors.NotFound:
            print("Not Found")
            continue
        except tweepy.errors.Forbidden:
            print("user account suspended")
            print("skipping tweet with id:"+tweet_id)
            continue
        except:
            print("other error occured")
            print("skipping id:"+ tweet_id)
            continue
        tweet_obj["tweet"] = tweet    
        user = api.get_user(user_id = tweet.user.id) 
        tweet_obj["user"] = user
        arr.append(tweet_obj)
    tweets[date] = arr

# Write Tweetcontents and User location data to csv
with open("tweets.csv", "w", encoding="utf8", newline="") as csvFile:
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(["id", "created_at", "text", "lang", "user_id", "location", "profile_location", "utc_offset", "user_lang", "tweet_place_id"])
    for date in tweets.keys():
        for tweet in tweets[date]:
            user = tweet["user"]
            twet = tweet["tweet"]
            location = user.location
            if location == "":
                location = "NaN"
            profile_location = user.profile_location
            if profile_location == "" or profile_location == None:
                profile_location = "NaN"
            user_lang = user.lang
            if user_lang == "" or user_lang == None:
                user_lang = "NaN"
            place_id = twet.geo
            if place_id != None:
                place_id = tweet.geo["place_id"]
            if place_id == None:
                place_id = "NaN"
            utc_offset = user.utc_offset
            if utc_offset == "" or utc_offset == None:
                utc_offset = "NaN"
            csvWriter.writerow([twet.id, twet.created_at, twet.text, twet.lang, user.id, location, profile_location, utc_offset, user_lang, place_id])




#Sources:
#https://www.loginradius.com/blog/engineering/beginners-guide-to-tweepy/
#https://stackoverflow.com/questions/44948628/how-to-take-all-tweets-in-a-hashtag-with-tweepy?answertab=scoredesc#tab-top
#https://stackoverflow.com/questions/28384588/twitter-api-get-tweets-with-specific-id#28384699
#https://medium.com/analytics-vidhya/fetch-tweets-using-their-ids-with-tweepy-twitter-api-and-python-ee7a22dcb845
#https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/user
#https://stackoverflow.com/questions/65429943/python-dictionary-with-arrays-to-csv-file
#https://www.geeksforgeeks.org/python-tweepy-getting-the-location-of-a-user/
#https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet
#https://stackoverflow.com/questions/7781545/how-to-get-all-folder-only-in-a-given-path-in-python
#https://developer.twitter.com/en/docs/twitter-api/rate-limits -> 1 tweet per sec