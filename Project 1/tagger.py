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
		if(str(people[0]).lower() == str(ent.text).lower()):
			return True
		else:
			return False
	else:
		return False

def movie_filter(ent):
	white_list = ['WORK_OF_ART', 'DATE']
	if(ent.label_ in white_list):
		movies = ia.search_movie(ent.text)
		if(str(movies[0]).lower() == str(ent.text).lower()):
			return True
	else:
		return False

def tagger(tweet):
	doc = nlp(tweet)
	#print([(X.text, X.label_) for X in doc.ents])
	#print([(X, X.ent_iob_, X.ent_type_) for X in doc])
	actor_filtered = list(filter(actor_filter, doc.ents))
	movie_filtered = list(filter(movie_filter, doc.ents))
	#print(actor_filtered)
	if(len(actor_filtered) > 0 and len(movie_filtered) > 0):
		return ['actor', 'movie']
	if(len(actor_filtered) > 0):
		return ['actor']
	if(len(movie_filtered) > 0):
		return ['movie']
	return []


def main():

	tags = tagger("jennifer lopez receives a sweet note from Alex Rodriguez after Golden Globe loss")
	#tags = tagger("1917")
	#print(tags)

if __name__ == "__main__":
    # execute only if run as a script
    main()

