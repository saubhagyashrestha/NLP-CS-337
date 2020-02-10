# from imdb import IMDb
import string
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
import json
# from fuzzywuzzy import fuzz

from tmdbv3api import TMDb
from tmdbv3api import Discover
from tmdbv3api import Movie
tmdb = TMDb()
tmdb.api_key = '5c25bb6fa9590f49afafbb9fe8c3be4a'

import time
# import probablepeople as pp

# import nltk
# from nltk.tokenize import word_tokenize
# from nltk.tag import pos_tag

nlp = en_core_web_sm.load()
# ia = IMDb()



# pattern = 'NP: {<DT>?<JJ>*<NN>}'

# def preprocess(sent):
#     sent = nltk.word_tokenize(sent)
#     sent = nltk.pos_tag(sent)
#     cp = nltk.RegexpParser(pattern)
#     cs = cp.parse(sent)
#     return sent

# def strip_accents(text):
# 	try:
# 		text = unicode(text, 'utf-8')
# 	except NameError: # unicode is a default on python 3 
# 		pass
# 	text = unicodedata.normalize('NFD', str(text)).encode('ascii', 'ignore').decode("utf-8")
# 	return str(text)

def partial_award_check(award, tweet):
	tweet = tweet.lower()
	best_contains = 'best' in award
	performance_contains = 'best performance by an' in award
	if(performance_contains):
		offset = len('best performance by an ')
		award = award[offset:]
	elif(best_contains):
		offset = len('best ')
		award = award[offset:]
	no_punc_award= award.translate(str.maketrans('', '', string.punctuation))
	no_punc_tweet = tweet.translate(str.maketrans('', '', string.punctuation))
	if(no_punc_award in no_punc_tweet):
		return True
	return False


def actor_filter(ent):
	if(ent.label_ == 'PERSON'):
		#people = ia.search_person(ent.text)
		#if(str(people[0]).lower() == str(ent.text).lower()):
		#	return True
		#else:
		#	return False
		return True
	else:
		return False

def lower_it(name):
	return name.lower()

def tagger(tweet, mov_list):
	

	doc = nlp(tweet)
	# sent = preprocess(tweet)
	# print(sent)
	#print([(X.text, X.label_) for X in doc.ents])
	#print([(X, X.ent_iob_, X.ent_type_) for X in doc])
	actor_filtered = list(filter(actor_filter, doc.ents))
	actor_names = list(map(lower_it, map(str,actor_filtered)))

	movies = []
	mov_list_lower = map(lower_it, map(str, mov_list))
	for movie in mov_list_lower:
		tweet_lower = str(tweet).lower()
		contains = movie in tweet_lower
		if(contains):
			movies.append(movie)
			break
	
	movie_names = list(map(lower_it, map(str, movies)))
	#print(actor_filtered)
	#if(len(actor_filtered) > 0 and len(movie_filtered) > 0):
	#	return ['actor', 'movie']
	#if(len(actor_filtered) > 0):
	#	return ['actor']
	#if(len(movie_filtered) > 0):
	#	return ['movie']

	return [actor_names,movie_names]



def prune_tag(year, award_list):
	start = time.time()
	nomin_count = 0
	lst = []
	final_lst = []
	year_int = int(year)
	last_year = str(year_int -1)
	start_date = str(last_year) + '-01-01'
	end_date = str(last_year) + '-12-31'
	discover = Discover()
	count = 1
	mov_list = []
	while(count < 15):
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
	# mov_list = map(strip_accents, mov_list)
	file_name_1 = 'pruned_tweets_best_' + year +'.json'
	with open(file_name_1,encoding="utf8") as infile:
		for line in infile:
			text = json.loads(line)['text']
			lst.append(text.lower())
	infile.close()

	file_name_2 = 'pruned_tweets_' + year +'.json'
	with open(file_name_2,encoding="utf8") as infile:
		for line in infile:
			text = json.loads(line)['text']
			lst.append(text.lower())
	infile.close()

	for tweet in lst:
		for award in award_list:
			award = award.lower()
			# ratio = fuzz.partial_ratio(str(award), str(tweet))
			# nomin_contains = 'nomin' in tweet
			# if(nomin_contains):
			# 	nomin_count += 1
			# contains = award in tweet
			contains = partial_award_check(award, tweet)
			if(contains):
				 # print(tweet)
			# if(ratio > 80):
				tags = tagger(tweet, mov_list)
				tweet_dic = {}
				tweet_dic['text'] = tweet
				tweet_dic['tags'] = tags
				final_lst.append(tweet_dic)
				break

	name = 'tagged_tweets_' + year + '.json'
	with open(name,'w') as outfile:
		for tweet in final_lst:
			json.dump(tweet, outfile)
			outfile.write('\n')
		outfile.close()
	end = time.time()
	total = end-start
	print("******************" + year + " ****" + str(total))
	# print(nomin_count)





def main():

	tags = tagger("jennifer lopez receives a sweet note from Alex Rodriguez after Golden Globe loss")
	print(tags)

if __name__ == "__main__":
	# execute only if run as a script
	main()
