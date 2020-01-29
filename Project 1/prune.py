import json
from classes import *
from fuzzywuzzy import fuzz
import string


def contains_key_words(text):
    #this list of words needs to be added to
    key_words = ["best", "award", "goes to", "present", "host", "monologue"]
    #prior list of key words: "win", "wins", "winner","won","nominee", "nominated", "congrat", "best", "award", "goes to", "present", "host", "monologue"
    text1 = text.lower().translate(str.maketrans('', '', string.punctuation)).split()
    for i in key_words:
        if i in text1:
            print("Found Relevant: " + i + " \n" + "Tweet: " + text + "\n\n")
            return True
    return False

def tagger(tweet):
    return(Tweet(tweet,[]))

def prune():
    TweetObjs = []
    with open('test.json', encoding="utf8") as f:
        for line in f:
            message = json.loads(line)
            #get the text
            tweet = message["text"]
            #pass text through tagger
            tweetobj = tagger(tweet)
            if len(tweetobj.tweet_tags) != [] and contains_key_words(tweetobj.tweet_text):
                TweetObjs.append(tweetobj)
    return(TweetObjs)
