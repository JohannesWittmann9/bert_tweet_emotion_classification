import csv
import os
import sys
import random
import pandas as pd
import tweepy

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


#https://www.loginradius.com/blog/engineering/beginners-guide-to-tweepy/
#https://stackoverflow.com/questions/44948628/how-to-take-all-tweets-in-a-hashtag-with-tweepy?answertab=scoredesc#tab-top
#https://stackoverflow.com/questions/28384588/twitter-api-get-tweets-with-specific-id#28384699
#https://medium.com/analytics-vidhya/fetch-tweets-using-their-ids-with-tweepy-twitter-api-and-python-ee7a22dcb845

# TODO: Insert API Keys below
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)# https://developer.twitter.com/en/docs/twitter-api/rate-limits -> 1 tweet per sec


numOfTotalTweets = 10000

dirs = next(os.walk("RussoUkrainianWar_Dataset-main"))[1] #https://stackoverflow.com/questions/7781545/how-to-get-all-folder-only-in-a-given-path-in-python
print(dirs)

numOfTweetsPerFolder = int(numOfTotalTweets/len(dirs))

print(numOfTweetsPerFolder)


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


tweet_ids = {}

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

#print(tweet_ids)
#Write ids to csv

#https://stackoverflow.com/questions/65429943/python-dictionary-with-arrays-to-csv-file

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

for date in tweet_ids:
    arr = []
    if date in tweets.keys():
        arr = tweets[date]
    for tweet_id in tweet_ids[date]:
        tweet = api.get_status(tweet_id)
        #tweet = sample
        arr.append(tweet)
    tweets[date] = arr

#print(tweets)

#https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet
with open("tweets.csv", "w", encoding="utf8", newline="") as csvFile:
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(["id","created_at","text","lang"])
    for date in tweets.keys():
        for tweet in tweets[date]:
            csvWriter.writerow([tweet["data"][0]["id"], tweet["data"][0]["created_at"], tweet["data"][0]["text"], tweet["data"][0]["lang"]])



# with open('tweets.csv', newline='', encoding="utf8") as csvfile:
#      spamreader = csv.reader(csvfile)
#      for row in spamreader:
#          print(', '.join(row))
