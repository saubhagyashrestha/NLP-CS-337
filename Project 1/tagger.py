import imdb
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm

nlp = en_core_web_sm.load()
ia = imdb.IMDB()

def actor_filter(ent):
	white_list = ['PERSON', 'WORK_OF_ART', 'DATE']
	if(ent.label_ in white_list):
		return True
	else:
		return False

def movie_filter(ent):
	white_list = ['PERSON', 'WORK_OF_ART', 'DATE']
	if(ent.label_ in white_list):
		return True
	else:
		return False

def actor_check

def tagger(tweet):
	doc = nlp(tweet)
	#print([(X.text, X.label_) for X in doc.ents])
	actor_bool, movie_bool = False
	#print([(X, X.ent_iob_, X.ent_type_) for X in doc])
	filtered = filter(ent_filter, doc.ents)

	for X in filtered:
		print(X.text)


def main():

	#tagger("‘1917’ and ‘Once Upon a Time… in Hollywood’ take top prizes at Golden Globes")
	tagger("henlo bitches")

if __name__ == "__main__":
    # execute only if run as a script
    main()

