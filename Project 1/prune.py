import json
from tagger import tagger
from classes import *
import string


def contains_key_words(text):
    #this list of words needs to be added to
    key_words = ["wins", "win", "won", "winner", "nominate", "nomimated", "nominee", "lost", "award", "awarded", "awards", "present", "presenter", "presents", "presented", "host",
    "hosts", "hosted","best", "goes to", "gave", "announce", "announced", "introduce", "introduced", "monologue", "carol", "brunett","cecil","demille"]
    #prior list of key words: "win", "wins", "winner","won","nominee", "nominated", "congrat", "best", "award", "goes to", "present", "host", "monologue"

    award_words = ["motion","picture","screenplay, ""movie","tv","television","series","performance","director","actor","actress","drama","comedy","animated","foreign","original","score",
    "song","cecil","demille","musical","role","supporting","limited","carol","burnett","best","language","award"]

    text = text.split()
    for i in key_words:
        if i in text and len(set(text).intersection(set(award_words))) > 3:
            return True
    return False

def tag_wrapper(tweet):
    tags = tagger(tweet)
    return(tags)

def prune(file_name):
    pruned_tweets = []
    with open(file_name,encoding="utf8") as infile:
        for line in infile:
            message = json.loads(line)
            #get the text
            text = message["text"]
            text = text.lower().translate(str.maketrans('', '', string.punctuation.replace("-", "")))
            #pass text through tagger
            #if len(tweetobj.tweet_tags) != [] and contains_key_words(tweetobj.tweet_text):
            if contains_key_words(text):
                tags = tag_wrapper(text)
                tweet_dic = {}
                tweet_dic['text'] = text
                tweet_dic['tags'] = tags
                pruned_tweets.append(tweet_dic)
    infile.close()

    with open('pruned_tweets.json','w') as outfile:
        for tweet in pruned_tweets:
            json.dump(tweet, outfile)
            outfile.write('\n')
    outfile.close()

prune('gg2020.json')
