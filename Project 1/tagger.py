from imdb import IMDb
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm

nlp = en_core_web_sm.load()
ia = IMDb()

def actor_filter(ent):
	if(ent.label_ == 'PERSON'):
		people = ia.search_person(ent.text)
		if(people[0] == ent.text):
			return True
		else:
			return False
	else:
		return False

def movie_filter(ent):
	white_list = ['WORK_OF_ART', 'DATE']
	if(ent.label_ in white_list):
		movies = ia.search_movie(ent.text)
		if(str(movies[0]) == str(ent.text) and movies[0]['year'] == 2019):
			return True
	else:
		return False

def tagger(tweet):
	doc = nlp(tweet)
	#print([(X.text, X.label_) for X in doc.ents])
	#print([(X, X.ent_iob_, X.ent_type_) for X in doc])
	actor_filtered = list(filter(actor_filter, doc.ents))
	movie_filtered = list(filter(movie_filter, doc.ents))
	if(len(actor_filtered) > 0 and len(movie_filtered) > 0):
		return ['actor', 'movie']
	if(len(actor_filtered) > 0):
		return ['actor']
	if(len(movie_filtered) > 0):
		return ['movie']
	return []


def main():

	#tagger("‘1917’ and ‘Once Upon a Time… in Hollywood’ take top prizes at Golden Globes")
	tags = tagger("1917")
	print(tags)

if __name__ == "__main__":
    # execute only if run as a script
    main()

