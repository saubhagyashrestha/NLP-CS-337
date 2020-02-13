import json
from classes import *
import string
from tagger import tagger
from tagger import partial_award_check
import time

from tmdbv3api import TMDb
from tmdbv3api import Discover
from tmdbv3api import Movie
tmdb = TMDb()
tmdb.api_key = '5c25bb6fa9590f49afafbb9fe8c3be4a'


def prune_tag(tweet, year, award_list, mov_list):
	
	nomin_count = 0
	lst = []
	tweet_dic = {}

	for award in award_list:
		award = award.lower()
		# ratio = fuzz.partial_ratio(str(award), str(tweet))
		# nomin_contains = 'nomin' in tweet
		# if(nomin_contains):
		#   nomin_count += 1
		# contains = award in tweet
		contains = partial_award_check(award, tweet)
		if(contains):
			 # print(tweet)
		# if(ratio > 80):
			tags = tagger(tweet, mov_list)
			if(len(tags[0]) == 0 and len(tags[1]) == 0):
				break
			tweet_dic['text'] = tweet
			tweet_dic['tags'] = tags
			break

	
	return tweet_dic
	# print(nomin_count)


def movie_list_gen(year):
	year_int = int(year)
	last_year = str(year_int -1)
	start_date = str(last_year) + '-01-01'
	end_date = str(last_year) + '-12-31'
	discover = Discover()
	count = 1
	mov_list = []
	while(count < 12):
		curr_list = discover.discover_movies({
			'primary_release_year': last_year,
			'page': count
		})
		mov_list.append(curr_list)
		count += 1
	count = 0
	while(count < 10):
		curr_list = discover.discover_tv_shows({
			'air_date.gte': start_date,
			'air_date.lte': end_date
		})
		mov_list.append(curr_list)
		count += 1

	flat_list = []
	for sublist in mov_list:
		for item in sublist:
			flat_list.append(item)
	mov_list = flat_list
	return mov_list



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
	start = time.time()
    year = str(year)
    pruned_tweets = []
    pruned_tweets_best = []
    pruned_tweets_red_carpet = []
    present_tweets = []
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
            pres_contain = text1.find('present')
            if(pres_contain != -1):
				tag_tweet = prune_tag(text, year, award_list, mov_list)
				if(tag_tweet != {}):
					present_tweets.append(tag_tweet)
            if contains_key_words(text1):
            	if(pres_contain == -1):
					tag_tweet = prune_tag(text, year, award_list, mov_list)
                tweet_dic = {}
                tweet_dic['text'] = text
                pruned_tweets.append(tweet_dic)
                if(tag_tweet != {}):
					tagged_tweets.append(tag_tweet)
            if 'best' in text1.split():
            	if(pres_contain == -1 and not 'best' in text1.split()):
					tag_tweet = prune_tag(text, year, award_list, mov_list)
                tweet_dic = {}
                tweet_dic['text'] = text
                pruned_tweets_best.append(tweet_dic)
                if(tag_tweet != {}):
					tagged_tweets.append(tag_tweet)
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

    name4 = 'tagged_tweets_' + year + '.json'
	with open(name4,'w') as outfile:
		for tweet in tagged_tweets:
			json.dump(tweet, outfile)
			outfile.write('\n')
	outfile.close()

	name5 = 'presenter_tweets_' + year + '.json'
	with open(name5,'w') as outfile:
		for tweet in present_tweets:
			json.dump(tweet, outfile)
			outfile.write('\n')
	outfile.close()

	end = time.time()
	total = end-start
	print("******************" + year + " ****" + str(total))
