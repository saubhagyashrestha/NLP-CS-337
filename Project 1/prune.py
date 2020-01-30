import json
from classes import *
import string


def contains_key_words(text):
    #this list of words needs to be added to
    key_words = ["wins", "win", "won", "winner", "nominate", "nomimated", "nominee", "lost", "award", "awarded", "awards", "present", "presenter", "presents", "presented", "host",
    "hosts", "hosted","best", "goes to", "gave", "announce", "announced", "introduce", "introduced", "monologue", "carol", "brunett","cecil","demille"]
    #prior list of key words: "win", "wins", "winner","won","nominee", "nominated", "congrat", "best", "award", "goes to", "present", "host", "monologue"
    text = text.split()
    for i in key_words:
        if i in text:
            return True
    return False

def tag_wrapper(tweet):
    tags = tagger(tweet)
    return(Tweet(tweet,tags))

def prune(file_name):
    TweetObjs = []
    with open(file_name,encoding="utf8") as f:
        for line in f:
            message = json.loads(line)
            #get the text
            tweet = message["text"]
            text = tweet.lower().translate(str.maketrans('', '', string.punctuation.replace("-", "")))
            #pass text through tagger
            tweetobj = tagger(text)
            #if len(tweetobj.tweet_tags) != [] and contains_key_words(tweetobj.tweet_text):
            if contains_key_words(tweetobj.tweet_text):
                TweetObjs.append(tweetobj)
    return(TweetObjs)
