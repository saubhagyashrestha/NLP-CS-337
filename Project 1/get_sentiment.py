import json
import en_core_web_sm
from nltk import word_tokenize, pos_tag
import time



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


def get_sentiments(year):
    start = time.time()
    year = str(year)
    lst = []
    file_name = 'pruned_tweets_' + year +'.json'
    with open(file_name,encoding="utf8") as infile:
        for line in infile:
            text = json.loads(line)['text']
            slt = text.split()
            for item in ["snub", "snubbed", "political", "deserving", "funny", "acceptance", "joke"]:
                if item in slt:
                    lst.append(text.lower())
                    break
    infile.close()

    print(len(lst), "TOTAL TWEETS WE ARE LOOKING AT")

    political_statement = []
    best_acceptance_speech = []
    funny_jokes = []
    snubbed_actors = []
    deserving_actors = []
    for tweet in lst:
        splt = tweet.split()
        #start w/ snubs
        if "snub" in splt or "snubbed" in splt:
            ppl_lst = tagger(tweet)

            for name in ppl_lst:
                if "http" in name or len(name.split()) > 2 or "#" in name or 'golden' in name or '@' in name:
                    continue
                if "'" in name:
                    name = name[:name.index("'")]
                if "’" in name:
                    name = name[:name.index("’")]
                flag = False
                for ii in range(len(snubbed_actors)):
                    if name in snubbed_actors[ii][0]:
                        snubbed_actors[ii][1] += 1
                        flag = True
                if not flag:
                    snubbed_actors.append([name,1])

        #most deserving wins
        if "deserving" in splt:
            ppl_lst = tagger(tweet)

            for name in ppl_lst:
                if "http" in name or len(name.split()) > 2 or "#" in name or 'golden' in name or '@' in name:
                    continue
                if "'" in name:
                    name = name[:name.index("'")]
                if "’" in name:
                    name = name[:name.index("’")]
                flag = False
                for ii in deserving_actors:
                    if name in ii[0]:
                        ii[1] += 1
                        flag = True
                if not flag:
                    deserving_actors.append([name,1])

        #funniest joke
        if "funny" in splt or "joke" in splt or "haha" in splt or "lol" in splt:
            ppl_lst = tagger(tweet)

            for name in ppl_lst:
                if "http" in name or len(name.split()) > 2 or "#" in name or 'golden' in name or '@' in name:
                    continue
                if "'" in name:
                    name = name[:name.index("'")]
                if "’" in name:
                    name = name[:name.index("’")]
                flag = False
                for ii in funny_jokes:
                    if name in ii[0]:
                        ii[1] += 1
                        flag = True
                if not flag:
                    funny_jokes.append([name,1])

        if "acceptance" in splt and "speech" in splt and "best" in splt:
            ppl_lst = tagger(tweet)

            for name in ppl_lst:
                if "http" in name or len(name.split()) > 2 or "#" in name or 'golden' in name or '@' in name:
                    continue
                if "'" in name:
                    name = name[:name.index("'")]
                if "’" in name:
                    name = name[:name.index("’")]
                flag = False
                for ii in best_acceptance_speech:
                    if name in ii[0]:
                        ii[1] += 1
                        flag = True
                if not flag:
                    best_acceptance_speech.append([name,1])

        if "political" in splt:
            ppl_lst = tagger(tweet)

            for name in ppl_lst:
                if "http" in name or len(name.split()) > 2 or "#" in name or 'golden' in name or '@' in name:
                    continue
                if "'" in name:
                    name = name[:name.index("'")]
                if "’" in name:
                    name = name[:name.index("’")]
                flag = False
                for ii in political_statement:
                    if name in ii[0]:
                        ii[1] += 1
                        flag = True
                if not flag:
                    political_statement.append([name,1])

    political_statement.sort(key=lambda x: -x[1])
    best_acceptance_speech.sort(key=lambda x: -x[1])
    funny_jokes.sort(key=lambda x: -x[1])
    deserving_actors.sort(key=lambda x: -x[1])
    snubbed_actors.sort(key=lambda x: -x[1])



    print("Biggest Snub: ", snubbed_actors[0][0].title())
    print("Most Deserving Win: ", deserving_actors[0][0].title())
    print("Funniest Joke Delivery: ", funny_jokes[0][0].title())
    print("Best Acceptance Speech: ", best_acceptance_speech[0][0].title())
    print("Biggest Political Statement: ", political_statement[0][0].title())
    print(time.time() - start, " seconds since beginning")

get_sentiments(2015)
