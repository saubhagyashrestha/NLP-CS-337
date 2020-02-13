import json
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
from nltk import word_tokenize, pos_tag
import string
import re
from collections import deque
import time
from emoji import UNICODE_EMOJI
import itertools
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

nlp = en_core_web_sm.load()

def get_tags(sentence):
    tokens = word_tokenize(sentence)
    tags = pos_tag(tokens)
    return [x[1] for x in tags]

def has_emoji(word):
    for char in word:
        if char in UNICODE_EMOJI:
            return True
    return False

def actor_filter(ent):
	if('goldenglobes' not in ent.text and ent.label_ == 'PERSON'):
		return True
	return False

def tagger(tweet):
    doc = nlp(tweet)
    actors = list(filter(actor_filter,doc.ents))
    return [str(actor) for actor in actors]

def hosts(year):
    year = str(year)
    lst = []
    file_name = 'pruned_tweets_' + year +'.json'
    with open(file_name,encoding="utf8") as infile:
        for line in infile:
            text = json.loads(line)['text']
            lst.append(text.lower())


    infile.close()

    # run it through tagger w/ "host" tweets
    relevant_tweets = []
    for tweet in lst:
        if "hosted" in tweet:
            relevant_tweets.append(tweet)
    #print(len(relevant_tweets), " is the number of tweets containing host")

    #print("\n\nTagging them with spacy now...")
    countt = 0
    shorter_list = []
    tinacount = 0
    yikes = False

    while countt < len(relevant_tweets):
        ppl_lst = tagger(relevant_tweets[countt])
        if ppl_lst != []:
            for person in ppl_lst:
                if "'" in person:
                    person = person[:person.index("'")]
                if "’" in person:
                    person = person[:person.index("’")]

                flag = False
                for ii in range(len(shorter_list)):
                    if person in shorter_list[ii][0] and "http" not in person and len(person.split()) < 3:
                        shorter_list[ii][1] += 1
                        flag = True
                if not flag and "http" not in person and len(person.split()) < 3:
                    shorter_list.append([person, 1])
        countt += 1

    shorter_list.sort(key = lambda x: -x[1])
    shorter_list = shorter_list[:10]

    curr = len(shorter_list)-1
    new_shorter_list = []
    while curr >= 0:
        name = shorter_list[curr][0]
        score = shorter_list[curr][1]
        chk = curr-1
        found = False
        while chk >= 0:
            name2 = shorter_list[chk][0]
            #check if fuzz is above a threshold
            threshold = max(fuzz.partial_ratio(name, name2), fuzz.ratio(name,name2))
            if threshold > 85:
                found = True
                #name at top is not a good name
                if len(name2.split()) < 2:
                    shorter_list[chk][0] = name
                shorter_list[chk][1] += score
                break
            chk -= 1
        if found == False:
            new_shorter_list.append([name,score])
        curr -= 1

    new_shorter_list.sort(key = lambda x: -x[1])


    if new_shorter_list[0][1] > 4 * new_shorter_list[1][1]:
        #print("Host is", new_shorter_list[0][0].title())
        return [new_shorter_list[0][0].title()]
    else:
        return [new_shorter_list[0][0].title(),new_shorter_list[1][0].title()]
        #print("Hosts are", new_shorter_list[0][0].title(), "and", new_shorter_list[1][0].title())
