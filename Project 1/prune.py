import json
from classes import *
import string


def contains_key_words(text):
    #this list of words needs to be added to
    key_words = ["wins", "win", "won", "winner", "nominate", "nomimated", "nominee", "lost", "award", "awarded", "awards", "present", "presenter", "presents", "presented", "host",
    "hosts", "hosted","best", "goes to", "gave", "announce", "announced", "introduce", "introduced"]
    key_words_red_carpet = ["best", "worst", "dressed"]

    text = text.split()
    for i in key_words:
        if i in text: # and len(set(text).intersection(set(award_words))) > 3:
            return True
    return False

def contains_key_words_red_carpet(text):
    key_words_red_carpet = ["best", "worst", "dressed"]
    text = text.split()
    for i in key_words_red_carpet:
        if i in text: # and len(set(text).intersection(set(award_words))) > 3:
            return True
    return False

def prune(year):
    year = str(year)
    pruned_tweets = []
    pruned_tweets_best = []
    pruned_tweets_red_carpet = []
    file_name = 'gg' + year + '.json'
    with open(file_name,encoding="utf8") as infile:
        dic = {}
        for line in infile:
            dic = json.loads(line)
            #get the text
        for message in dic:
            #message = json.loads(line)
            #get the text
            text = message["text"]
            text1 = text.lower().translate(str.maketrans('', '', string.punctuation.replace("-", "")))
            #pass text through tagger
            #if len(tweetobj.tweet_tags) != [] and contains_key_words(tweetobj.tweet_text):
            if contains_key_words(text1):
                tweet_dic = {}
                tweet_dic['text'] = text
                pruned_tweets.append(tweet_dic)
            if 'best' in text1.split():
                tweet_dic = {}
                tweet_dic['text'] = text
                pruned_tweets_best.append(tweet_dic)
            if contains_key_words_red_carpet(text1):
                tweet_dic = {}
                tweet_dic['text'] = text1
                pruned_tweets_red_carpet.append(tweet_dic)
    infile.close()

    name = 'pruned_tweets_' + year + '.json'
    with open(name,'w') as outfile:
        for tweet in pruned_tweets:
            json.dump(tweet, outfile)
            outfile.write('\n')
    outfile.close()

    name2 = 'pruned_tweets_best_' + year + '.json'
    with open(name2,'w') as outfile:
        for tweet in pruned_tweets_best:
            json.dump(tweet, outfile)
            outfile.write('\n')
    outfile.close()

    name3 = 'pruned_tweets_red_carpet_' + year + '.json'
    with open(name3,'w') as outfile:
        for tweet in pruned_tweets_red_carpet:
            json.dump(tweet, outfile)
            outfile.write('\n')
    outfile.close()
