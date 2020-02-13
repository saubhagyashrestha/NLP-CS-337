import json
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
from nltk import word_tokenize, pos_tag
import nltk
import string
import re
from collections import deque
import time
from emoji import UNICODE_EMOJI

nlp = en_core_web_sm.load()
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def get_tags(sentence):
    tokens = word_tokenize(sentence)
    tags = pos_tag(tokens)
    return [x[1] for x in tags]

def has_emoji(word):
    for char in word:
        if char in UNICODE_EMOJI:
            return True
    return False


def get_awards_fun(year):
    year = str(year)
    ll = []
    #for i in OFFICIAL_AWARDS:
    #    lll = pos_tag(word_tokenize(i))
    #    for ii in lll:
    #        if ii[1] not in ll:
    #            ll.append(ii[1])
    #print(ll)

    lst = []
    #print("**************STARTED " + year + "********************")
    #startt = time.time()

    file_name = 'pruned_tweets_best_' + year +'.json'
    with open(file_name,encoding="utf8") as infile:
        for line in infile:
            text = json.loads(line)['text']
            lst.append(text.lower())


    infile.close()
    point = time.time()
    #print(point-startt, " seconds since the start")

    #print(len(lst))

    verb_conj = ["goes", "awarded", "went", "to", "and", "but", "at", "with", "on", "is", "https", "http", "win", "won", "wins", "award", "...", "#"]
    in_word = ['http']
    puncs = string.punctuation.replace("-","").replace(",","")
    one_b4 = ['his','her','them']
    cut = ["\n"]
    banned = ["of", "on", "from", "golden", "tv", "over", "into", "globe", "globes"]
    banned_char = "@&()';:/’" + '"'
    #verb_words_entity_first = ["won", "wins", "winner", "got"]

    potential_awards = {}
    for tweet in lst:
        slt = tweet.split()
        i,start = 0,0
        b_huh = False
        already = False
        while i < len(slt):
            wrd = slt[i]
            if b_huh and (',' in wrd or '-' in wrd):
                if already:
                    p_name = " ".join(slt[start:i])
                    if p_name in potential_awards:
                        potential_awards[p_name] += 1
                    else:
                        potential_awards[p_name] = 1
                    b_huh = False
                    already = False
                else:
                    already = True
            if b_huh and wrd in banned:
                b_huh = False
                already = False
            if b_huh:
                for char in banned_char:
                    if char in wrd:
                        b_huh = False
                        already = False
                        break
            if has_emoji(wrd):
                b_huh = False
                already = False
            if wrd == "best":
                if b_huh:
                    p_name = " ".join(slt[start:i])
                    if p_name in potential_awards:
                        potential_awards[p_name] += 1
                    else:
                        potential_awards[p_name] = 1
                b_huh = True
                start = i
            if b_huh and wrd[-1] in puncs:
                p_name = " ".join(slt[start:i+1])
                while p_name[-1] in puncs:
                    p_name = p_name[:-1]
                if p_name in potential_awards:
                    potential_awards[p_name] += 1
                else:
                    potential_awards[p_name] = 1
                b_huh = False
                already = False
            if b_huh and wrd[-2:] == '\n':
                p_name = " ".join(slt[start:i])[:-2]
                if p_name in potential_awards:
                    potential_awards[p_name] += 1
                else:
                    potential_awards[p_name] = 1
                b_huh = False
                already = False
            if b_huh and '#' == wrd[0]:
                p_name = " ".join(slt[start:i])
                if p_name in potential_awards:
                    potential_awards[p_name] += 1
                else:
                    potential_awards[p_name] = 1
                b_huh = False
                already = False
            if b_huh and wrd in verb_conj:
                p_name = " ".join(slt[start:i])
                if p_name in potential_awards:
                    potential_awards[p_name] += 1
                else:
                    potential_awards[p_name] = 1
                b_huh = False
            if b_huh and wrd in one_b4:
                p_name = " ".join(slt[start:i-1])
                if p_name in potential_awards:
                    potential_awards[p_name] += 1
                else:
                    potential_awards[p_name] = 1
                b_huh = False
            if b_huh and 'http' in wrd:
                p_name = " ".join(slt[start:i])
                if p_name in potential_awards:
                    potential_awards[p_name] += 1
                else:
                    potential_awards[p_name] = 1
                b_huh = False
            i += 1
            if i == len(slt) and b_huh:
                p_name = " ".join(slt[start:i])
                if p_name in potential_awards:
                    potential_awards[p_name] += 1
                else:
                    potential_awards[p_name] = 1


    #point = time.time()

    #print(point-startt, " seconds to do trim")
    #print("There are ", len(potential_awards), " potential awards")



    #countt = 0
    #print("HERE are the direct matches: ")
    #for name,value in potential_awards.items():
    #    if name in OFFICIAL_AWARDS:
    #        print(name,value)
    #        countt += 1
    #print("There are ", countt, " of them.")
    #print(potential_awards)
    p_names = []
    booger = []
    for name,value in potential_awards.items():
        splitted = name.split()

        #for o_name in OFFICIAL_AWARDS:
        #    if o_name in name and o_name not in booger:
        #        booger.append(o_name)
        #    if o_name in name and o_name != name:
        #        print("Improve trim: ", name)
        if value > 1 and len(splitted) > 3 and pos_tag(word_tokenize(splitted[1]))[0][1] in ['NN', 'VBN', 'JJ', 'NNS']:
            p_names.append([name,value])
        #except:
        #    pass
    #print(p_names)

    #point = time.time()
    #print(point-startt, " seconds since the start")

    #print("Potential award names ending determined by verb_conj, puncuation, pronouns")
    #print("In the potential names, there exists " , len(booger), " perfect award names somewhere in there")

    p_names.sort(key = lambda x: -x[1])

    countt = 0
    #print("HERE are the direct matches: ")
    #for x in p_names:
    #    if x[0] in OFFICIAL_AWARDS:
    #        print(x)
    #        countt += 1
    #print("There are ", countt, " of them.")


    #print("\nWe have a total of ", len(p_names), " potential awards.\nHere are the top half of them: ")
    #for ind in range(int(len(p_names)/2)):
    #    print("FIRST CUT: ", p_names[ind])

#############################################################################################################################################
    #prune list of possible awards

    possibletags = set(['JJS', 'NN', ':', 'JJ', 'CC', 'RBS', 'IN', 'DT', 'VBN', ',', 'VBZ', 'RB', 'NNS'])
    banned = {"of", "on", "from", "golden", "tv", "win"}
    newlst = []
    for pair in p_names:
        tags = get_tags(pair[0])
        flag = True
        for tag in tags:
            if tag not in possibletags:
                flag = False
                break
        if flag:
            ### my part hello
            if len(set(pair[0].split()).intersection(banned)) < 1:
                last_word_tag = get_tags(pair[0].split()[-1])
                if 'NN' in last_word_tag or 'VBN' in last_word_tag or 'JJ' in last_word_tag:
                    if pair[0][-1] != "–" and pair[0][-1] != "," and pair[0][-1] != " ":
                        newlst.append(pair)

    #print("\nWe have now taken out awards with specific words such as on, from, golden, globes")
    #print("Last word also has to be a noun and cannot end in a punctuation")
    #point = time.time()
    #print(point-startt, " seconds since the start")

    #countt = 0
    #print("HERE are the direct matches: ")
    #for x in newlst:
    #    if x[0] in OFFICIAL_AWARDS:
    #        print(x)
    #        countt += 1
    #print("There are ", countt, " of them.")

    #print("\nWe have a total of ", len(newlst), " potential awards.\nHere are the top half of them: ")
    #for ind in range(len(newlst)):
    #    print("SECOND CUT: ", newlst[ind])

#############################################################################################################################################

    lets_see = set(["-", "for", "in", "by"])
    newlst_key = []
    for item in newlst:
        if len(item[0].split()) < 7:
            item[1] += len(set(item[0].split()).intersection(lets_see))*20
        else:
            item[1] += len(set(item[0].split()).intersection(lets_see))*15
    newlst.sort(key = lambda x: -x[1])

    newlst_key = newlst[:27]

    #print("\n\nModified list!! by adding value for keywords")
    #point = time.time()
    #print(point-startt, " seconds since the start")

    #print("There are not a total of ", len(newlst_key), " of them.\n Here they are: ")
    #for x in newlst_key:
    #    print(x)

#############################################################################################################################################

    #print("\n\nTagging them with spacy now...")
    newlst_key_spac = []
    for x in newlst_key:
        if nlp(x[0]).ents:
            pass
        else:
            newlst_key_spac.append(x)

    #point = time.time()
    #print(point-startt, " seconds since the start")
    #print("There are not a total of ", len(newlst_key_spac), " of them.\n Here they are: ")
    #for x in newlst_key_spac:
    #    print(x)

#############################################################################################################################################

    #matches = []
    #for i in OFFICIAL_AWARDS:
    #    for j in newlst_key:
    #        if i == j[0]:
    #            matches.append(j)

    #print("\nThere are now ", len(matches), " perfect matches.")
    #for pair in matches: #.items():
    #    print("Found perfect match for : ",  pair[0], "Value: ", pair[1])
    #print("\n")
    names = [x[0] for x in newlst_key_spac]
    #print(newlst_key)
    #print(newlst_key_spac)
    #for jj in OFFICIAL_AWARDS:
    #    if jj not in names:
    #        print("not found: ", jj)
    #print(names)
    return names
