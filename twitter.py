# Necessary imports
import csv
import os
import sys
import random
import pandas as pd
import tweepy
from configparser import ConfigParser

# Demo Info to test script
sample = {
    "data": [
        {
            "id": "1212092628029698048",
            "text": "We believe the best future version of our API will come from 'building' it with YOU. Here’s to another great year with everyone, who builds on the Twitter platform. We can’t wait to continue working with you in the new year. https://t.co/yvxdK6aOo2",
            "possibly_sensitive": "false",
            "referenced_tweets": [
                {
                    "type": "replied_to",
                    "id": "1212092627178287104"
                }
            ],
            "entities": {
                "urls": [
                    {
                        "start": 222,
                        "end": 245,
                        "url": "https://t.co/yvxdK6aOo2",
                        "expanded_url": "https://twitter.com/LovesNandos/status/1211797914437259264/photo/1",
                        "display_url": "pic.twitter.com/yvxdK6aOo2"
                    }
                ],
                "annotations": [
                    {
                        "start": 144,
                        "end": 150,
                        "probability": 0.626,
                        "type": "Product",
                        "normalized_text": "Twitter"
                    }
                ]
            },
            "author_id": "2244994945",
            "public_metrics": {
                "retweet_count": 8,
                "reply_count": 2,
                "like_count": 40,
                "quote_count": 1
            },
            "lang": "en",
            "created_at": "2019-12-31T19:26:16.000Z",
            "source": "Twitter Web App",
            "in_reply_to_user_id": "2244994945",
            "attachments": {
                "media_keys": [
                    "16_1211797899316740096"
                ]
            },
            "context_annotations": [
                {
                    "domain": {
                        "id": "119",
                        "name": "Holiday",
                        "description": "Holidays like Christmas or Halloween"
                    },
                    "entity": {
                        "id": "1186637514896920576",
                        "name": " New Years Eve"
                    }
                },
                {
                    "domain": {
                        "id": "119",
                        "name": "Holiday",
                        "description": "Holidays like Christmas or Halloween"
                    },
                    "entity": {
                        "id": "1206982436287963136",
                        "name": "Happy New Year: It’s finally 2020 everywhere!",
                        "description": "Catch fireworks and other celebrations as people across the globe enter the new year.\nPhoto via @GettyImages "
                    }
                },
                {
                    "domain": {
                        "id": "46",
                        "name": "Brand Category",
                        "description": "Categories within Brand Verticals that narrow down the scope of Brands"
                    },
                    "entity": {
                        "id": "781974596752842752",
                        "name": "Services"
                    }
                },
                {
                    "domain": {
                        "id": "47",
                        "name": "Brand",
                        "description": "Brands and Companies"
                    },
                    "entity": {
                        "id": "10045225402",
                        "name": "Twitter"
                    }
                },
                {
                    "domain": {
                        "id": "119",
                        "name": "Holiday",
                        "description": "Holidays like Christmas or Halloween"
                    },
                    "entity": {
                        "id": "1206982436287963136",
                        "name": "Happy New Year: It’s finally 2020 everywhere!",
                        "description": "Catch fireworks and other celebrations as people across the globe enter the new year.\nPhoto via @GettyImages "
                    }
                }
            ]
        }
    ],
    "includes": {
        "tweets": [
            {
                "possibly_sensitive": "false",
                "referenced_tweets": [
                    {
                        "type": "replied_to",
                        "id": "1212092626247110657"
                    }
                ],
                "text": "These launches would not be possible without the feedback you provided along the way, so THANK YOU to everyone who has contributed your time and ideas. Have more feedback? Let us know ⬇️ https://t.co/Vxp4UKnuJ9",
                "entities": {
                    "urls": [
                        {
                            "start": 187,
                            "end": 210,
                            "url": "https://t.co/Vxp4UKnuJ9",
                            "expanded_url": "https://twitterdevfeedback.uservoice.com/forums/921790-twitter-developer-labs",
                            "display_url": "twitterdevfeedback.uservoice.com/forums/921790-…",
                            "images": [
                                {
                                    "url": "https://pbs.twimg.com/news_img/1261301555787108354/9yR4UVsa?format=png&name=orig",
                                    "width": 100,
                                    "height": 100
                                },
                                {
                                    "url": "https://pbs.twimg.com/news_img/1261301555787108354/9yR4UVsa?format=png&name=150x150",
                                    "width": 100,
                                    "height": 100
                                }
                            ],
                            "status": 200,
                            "title": "Twitter Developer Feedback",
                            "description": "Share your feedback for the Twitter developer platform",
                            "unwound_url": "https://twitterdevfeedback.uservoice.com/forums/921790-twitter-developer-labs"
                        }
                    ]
                },
                "author_id": "2244994945",
                "public_metrics": {
                    "retweet_count": 3,
                    "reply_count": 1,
                    "like_count": 17,
                    "quote_count": 0
                },
                "lang": "en",
                "created_at": "2019-12-31T19:26:16.000Z",
                "source": "Twitter Web App",
                "in_reply_to_user_id": "2244994945",
                "id": "1212092627178287104"
            }
        ]
    }
}

demo_user = {
    "data": [
        {
            "id": "2244994945",
            "name": "Twitter Dev",
            "username": "TwitterDev",
            "location": "127.0.0.1",
            "entities": {
                "url": {
                    "urls": [
                        {
                            "start": 0,
                            "end": 23,
                            "url": "https://t.co/3ZX3TNiZCY",
                            "expanded_url": "/content/developer-twitter/en/community",
                            "display_url": "developer.twitter.com/en/community"
                        }
                    ]
                },
                "description": {
                    "hashtags": [
                        {
                            "start": 23,
                            "end": 30,
                            "tag": "DevRel"
                        },
                        {
                            "start": 113,
                            "end": 130,
                            "tag": "BlackLivesMatter"
                        }
                    ]
                }
            },
            "verified": "true",
            "description": "The voice of Twitter's #DevRel team, and your official source for updates, news, & events about Twitter's API. \n\n#BlackLivesMatter",
            "url": "https://t.co/3ZX3TNiZCY",
            "profile_image_url": "https://pbs.twimg.com/profile_images/1267175364003901441/tBZNFAgA_normal.jpg",
            "protected": "false",
            "pinned_tweet_id": "1255542774432063488",
            "created_at": "2013-12-14T04:35:55.000Z"
        }
    ],
    "includes": {
        "tweets": [
            {
                "id": "1255542774432063488",
                "text": "During these unprecedented times, what’s happening on Twitter can help the world better understand &amp; respond to the pandemic. \n\nWe're launching a free COVID-19 stream endpoint so qualified devs &amp; researchers can study the public conversation in real-time. https://t.co/BPqMcQzhId"
            }
        ]
    }
}

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
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Set total number of retrieved tweets
numOfTotalTweets = 1000

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
# Crawl Tweets and Userdata
for date in tweet_ids:
    arr = []
    if date in tweets.keys():
        arr = tweets[date]
    for tweet_id in tweet_ids[date]:
        tweet = api.get_status(tweet_id)
        #tweet = sample
        #user = demo_user
        user = api.get_user(id) 
        location = user["data"][0]["location"]
        if location == "":
            location = "NaN"
        tweet["location"] = location
        arr.append(tweet)
    tweets[date] = arr

# Write Tweetcontents and User location data to csv
with open("tweets.csv", "w", encoding="utf8", newline="") as csvFile:
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(["id","created_at","text","lang","user_id","location"])
    for date in tweets.keys():
        for tweet in tweets[date]:
            csvWriter.writerow([tweet["data"][0]["id"], tweet["data"][0]["created_at"], tweet["data"][0]["text"], tweet["data"][0]["lang"], tweet["data"][0]["author_id"], tweet["location"]])




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