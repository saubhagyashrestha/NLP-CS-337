import json
from classes import *
from fuzzywuzzy import fuzz
import string


def contains_key_words(text):
    #this list of words needs to be added to
    key_words = ["wins", "win", "won", "winner", "nominate", "nomimated", "nominee", "lost", "award", "awarded", "awards", "present", "presenter", "presents", "presented", "host",
    "hosts", "hosted","best", "goes to", "gave", "announce", "announced", "introduce", "introduced", "monologue"]
    #prior list of key words: "win", "wins", "winner","won","nominee", "nominated", "congrat", "best", "award", "goes to", "present", "host", "monologue"
    text = text.split()
    for i in key_words:
        if i in text:
            return True
    return False

def tagger(tweet):
    return(Tweet(tweet,[]))

def prune(file_name):
    TweetObjs = []
    with open(file_name,encoding="utf8") as f:
        for line in f:
            message = json.loads(line)
            #get the text
            tweet = message["text"]
            text = tweet.lower().translate(str.maketrans('', '', string.punctuation))
            #pass text through tagger
            tweetobj = tagger(text)
            #if len(tweetobj.tweet_tags) != [] and contains_key_words(tweetobj.tweet_text):
            if contains_key_words(tweetobj.tweet_text):
                TweetObjs.append(tweetobj)
    return(TweetObjs)

def get_awards(relevant_tweets_obj):
    award_words = ["motion","picture","movie","tv","television","series","performance","director","actor","actress","drama","comedy","animated","foreign","original","score",
    "song","cecil","demille","musical","role","supporting","limited","carol","burnett","best","language","award"]

    award_names = {}
    award_tweets = []

    for i in relevant_tweets_obj:
        tweet = i.tweet_text
        #print(tweet)
        #print(set(tweet.split()))
        #print(set(award_words))
        if len(set(tweet.split()).intersection(set(award_words))) > 3:
            award_tweets.append(tweet)
    for text in award_tweets:
        start = float('inf')
        end = float('-inf')
        for key_word in award_words:
            try:
                point = text.index(key_word)
                point2 = point + len(key_word)
                if point2 > end:
                    end = point2
                if point < start:
                    start = point
            except:
                pass
        if start != float('inf') and end != float('-inf'):
            name = text[start: end]
            if name not in award_names:
                award_names[name] = 1
            else:
                award_names[name] += 1
    return(award_names)

def run_this():
    potential_names = get_awards(prune('gg2020.json'))

    #this will print the potential names that have the word cecil in it
    print("********POTENTIAL AWARDS THAT HAVE THE WORD CECIL IN IT*******\n")
    for name, count in potential_names.items():
        if "cecil" in name:
            print("Count: " , count, "   Tweet: ", name, "\n")

    #when running, this right now will print the names of awards and they are mostly right
    print("\n\n\n*******AWARD NAMES**********\n")
    num = 0
    for name, count in potential_names.items():
        if count > 9:
            num += 1
            print("Name of award: ", name, "\n")
    print("Total awards: ", num)
run_this()
