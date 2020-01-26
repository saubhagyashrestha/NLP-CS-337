import json
from classes import *

#data = open('gg2020.json',encoding="utf8")
def tagger(tweet):
    tags = []
    #run tweet through imdb and find matches
    #with each match update the tags
    

    return(Tweet(tweet, tags))

def prune():
    TweetObjs = []
    with open('gg2020.json', encoding="utf8") as f:
        for line in f:
            message = json.loads(line)
            #get the text
            tweet = message["text"]
            #pass text through tagger
            tweetobj = tagger(tweet)
            TweetObjs.append(tweetobj)

    TweetObjs[0].printTweet()

prune()
