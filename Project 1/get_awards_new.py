import json
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
import nltk

nlp = en_core_web_sm.load()
#takes a file name and gets a list of awards from it
def get_awards():
    relevant_tweets = []

    with open('pruned_tweets.json',encoding="utf8") as infile:
        for line in infile:
            text = json.loads(line)['text']
            relevant_tweets.append(text)


    infile.close()

    best = "best"
    awarded_words = ["best", "congrats"]
    verb_words_entity_first = ["won", "wins", "winner", "got"]
    verb_words_entity_second = ["goes to", "awarded to"]

    example = "Sad about paul rudd but happy that emily jenkins got best director"
    example2 = "best picture animated goes to frozen 2"
    example1 = "happy that emily got best director"

    token = nltk.word_tokenize(example)
    print(nltk.pos_tag(token)[example.split().index('emily')])

    for word in awarded_words:
        if word in example:
            print("found " + word + "\n")
            ent_list = nlp(example).ents
            for wordz in verb_words_entity_first:
                if wordz in example:
                    for person in ent_list:
                        if person.label_ == 'PERSON':
                            if example.index(person.text) < example.index(wordz):
                                print("This person may have gotten an award: ", person.text)


    for i in [example1, example2]:
        if best in i:
            start = i.index(best)
            print("found " + best + "\n")
            for word in verb_words_entity_second:
                if word in i:
                    end = i.index(word)
                    print(i[start:end])
            for word in verb_words_entity_first:
                if word in i:
                    end = len(i)
                    print(i[start:end])

                        #indx = example.index(wordz)
                        #str = ''
                        #print(nltk.pos_tag(example[indx]))
                        #while (indx > -1 and nlp(example[indx]).ents and nlp(example[indx]).ents[0].label_ == 'PERSON'):
                        #while (indx > -1 and nlp(example[indx]).ents and nlp(example[indx]).ents[0].label_ == 'PERSON'):
                        #    str = example[indx] + " " + str
                        #    indx = indx - 1
                        #    print(indx)
                        #    print(str)

get_awards()
