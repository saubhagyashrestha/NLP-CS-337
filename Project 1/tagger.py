from imdb import IMDb
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm

import probablepeople as pp

# import nltk
# from nltk.tokenize import word_tokenize
# from nltk.tag import pos_tag

nlp = en_core_web_sm.load()
ia = IMDb()

# pattern = 'NP: {<DT>?<JJ>*<NN>}'

# def preprocess(sent):
#     sent = nltk.word_tokenize(sent)
#     sent = nltk.pos_tag(sent)
#     cp = nltk.RegexpParser(pattern)
#     cs = cp.parse(sent)
#     return sent

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

def movie_filter(ent):
	white_list = ['WORK_OF_ART', 'DATE']
	if(ent.label_ == 'WORK_OF_ART'):
		return True
	elif ent.label_ == 'DATE':
		movies = ia.search_movie(ent.text)
		if movies != [] and (str(movies[0]).lower() == str(ent.text).lower()):
			return True
	else:
		return False

def lower_it(name):
	return name.text.lower()

def tagger(tweet):
	doc = nlp(tweet)
	print(pp.parse(tweet))
	# sent = preprocess(tweet)
	# print(sent)
	#print([(X.text, X.label_) for X in doc.ents])
	#print([(X, X.ent_iob_, X.ent_type_) for X in doc])
	actor_filtered = list(filter(actor_filter, doc.ents))
	actor_names = list(map(lower_it, actor_filtered))

	movie_filtered = list(filter(movie_filter, doc.ents))
	movie_names = list(map(lower_it, movie_filtered))
	#print(actor_filtered)
	#if(len(actor_filtered) > 0 and len(movie_filtered) > 0):
	#	return ['actor', 'movie']
	#if(len(actor_filtered) > 0):
	#	return ['actor']
	#if(len(movie_filtered) > 0):
	#	return ['movie']

	return [actor_names,movie_names]


def main():

	tags = tagger("jennifer lopez receives a sweet note from Alex Rodriguez after Golden Globe loss")
	print(tags)

if __name__ == "__main__":
    # execute only if run as a script
    main()
