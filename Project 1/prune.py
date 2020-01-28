import json
from classes import *

from fuzzywuzzy import fuzz


str1 = "Priyanka Chopra and Nick Jonas at the 77th Annual Golden Globe Awards presented the award for Best TV series for a musical or comedy"
#str2 = "the best tv series award was presented by nick jonas and his wife"
str3 = "Priyanka Chopra and Nick Jonas at the 77th Annual Golden Globe Awards won the award for Best TV series for a musical or comedy"


def contains_key_words(text):
    #this list of words needs to be added to
    key_words = ["win", "nominee", "nominated", "congrat", "best", "award", "goes to", "present", "host"]
    text = text.split()
    for i in key_words:
        for j in text:
            if fuzz.patial_ratio(i, j.lower()) > 55:
                return True
    return False

def prune():
    TweetObjs = []
    with open('gg2020.json', encoding="utf8") as f:
        for line in f:
            message = json.loads(line)
            #get the text
            tweet = message["text"]
            #pass text through tagger
            tweetobj = tagger(tweet)


            if len(tweetobj.tweet_tags) != [] and contains_key_words(tweetobj.tweet_text):
                TweetObjs.append(tweetobj)
