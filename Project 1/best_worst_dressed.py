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
from random import sample

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

def redcarpet(year):
    start_time = time.time()
    print("JUST STARTED")
    year = str(year)
    lst = []
    file_name = 'pruned_tweets_red_carpet_' + year +'.json'
    with open(file_name,encoding="utf8") as infile:
        for line in infile:
            text = json.loads(line)['text']
            lst.append(text.lower())


    infile.close()

    print(time.time() - start_time, " seconds to load file")

    key_words_red_carpet = {"best", "dressed", "worst", "beautiful", "stunning", "ugly", "bad", "amazing"}

    relevant_tweets = []
    for tweet in lst:
        slt = tweet.split()
        if len(set(slt).intersection(key_words_red_carpet)) > 1:
            relevant_tweets.append(tweet)

    print(time.time() - start_time, " seconds to check for intersection")
    print("\nnow we have ", len(relevant_tweets), "relevant tweets after checking for more than one word present.\n")

    if len(relevant_tweets) > 1000:
        relevant_tweets = sample(relevant_tweets, 1000)

    print("now there are ", len(relevant_tweets))

    print("\n\nTagging them with spacy now...")
    ppl_sent = {}
    for tweet in relevant_tweets:
        ppl_lst = tagger(tweet)
        if ppl_lst != []:
            for person in ppl_lst:
                #taking care of designers -- don't want to count as best or worst dressed
                if "in " + person in tweet or person == "golden globes" or "'" in tweet or "’" in tweet or "http" in tweet:
                    #print("youve hit a designer")
                    break
                if person not in ppl_sent:
                    ppl_sent[person] = [[tweet],0,0,1]
                else:
                    ppl_sent[person][0].append(tweet)
                    ppl_sent[person][3] += 1

    print(time.time() - start_time, " seconds to run spacy")

    ppl_sent = {k: v for k, v in sorted(ppl_sent.items(), key=lambda item: -item[1][3])}
    count = 0
    narrowed_list = {}
    for name,info in ppl_sent.items():
        if count < 10 and len(name.split()) == 2:
            narrowed_list[name] = info
            count += 1
        elif count >= 10:
            break

    positive_terms = ["beautiful", "amazing", "gorgeous", "stunnning", "favorite", "love", "great", "hot", "sexy"]
    negative_terms = ["ugly", "terrible", "bad", "not"]

    worst_dressed = ["", -1]
    best_dressed = ["", -1]
    most_controversial = ["", 10000]
    most_discussed = ["", -1]
    for name,info in narrowed_list.items():
        #print("THIS IS INFO: ", info)
        for tweeet in info[0]:
            if "best dressed" in tweeet and "worst dressed" in tweeet:
                if abs(tweeet.index("best") - tweeet.index(name)) > abs(tweeet.index("worst") - tweeet.index(name)):
                    info[2] += 2
                else:
                    info[1] += 2
            elif "best dressed" in tweeet:
                info[1] += 2
            elif "worst dressed" in tweeet:
                info[2] += 2

            for wrd in tweeet.split():
                if wrd in positive_terms:
                    info[1] += 1
                if wrd in negative_terms:
                    info[2] += 1

        pos = info[1]
        neg = info[2]
        if not pos:
            pos += 1
        if not neg:
            neg += 1
        metric = (pos/neg)*(pos + neg)
        info.append(metric)

        if info[2] > worst_dressed[1]:
            worst_dressed = [name, info[2]]
        if info[1] > best_dressed[1]:
            best_dressed = [name, info[1]]
        if info[3] > most_discussed[1]:
            most_discussed = [name, info[3]]
        #print((info[1] - info[2]) / info[3])
        if (info[1] - info[2]) == 0 and 1 / info[3] < most_controversial[1] and abs((info[1] - info[2] + 1) / info[3]) < most_controversial[1]:
            most_controversial = [name, abs((info[1] - info[2]+1) / info[3])]
            #print("new most controversial. ", name, " value of ", abs((info[1] - info[2]+1) / info[3]))
            #print("value of info1 ", info[1], "value of info2, ", info[2], " value of info3, ", info[3])
        elif info[1] - info[2] != 0 and abs((info[1] - info[2]) / info[3]) < most_controversial[1]:
            most_controversial = [name, abs((info[1] - info[2]) / info[3])]
            #print("new most controversial (NOT ZERO ROUTE). ", name, " value of ", abs((info[1] - info[2]) / info[3]))


        #print("\n", name, " scores: ", info[1:])

    #print("Best Dressed:", best_dressed[0].title())
    #print("Worst Dressed: ", worst_dressed[0].title())
    #print("Most Controversially Dressed: ", most_controversial[0].title())
    #print("Most Discussed: ", most_discussed[0].title())

    return ["Best Dressed: " + best_dressed[0].title(), "Worst Dressed: " + worst_dressed[0].title(), "Most Controversially Dressed: " + most_controversial[0].title(), "Most Discussed: " + most_discussed[0].title()]
