import json
from tagger import tagger
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm

nlp = en_core_web_sm.load()

with open("gg2020.json",encoding="utf8") as infile:
    for line in infile:
        message = json.loads(line)
        text = message["text"]

        if "animated" in text:
            pass
            #print(text, "\n\n")

infile.close()

#print("new section \n\n")

str = "it’s golden globes day so i want to see roman griffin david win for jojo rabbit, paul rudd for living with yourself, saoirse ronan for little women, jojo rabbit for comedy picture, and frozen 2 for animated film"

print([(X.text, X.label_) for X in nlp(str).ents])

str = "Minha predictions corrigidas pro Golden Globes de amanhã: picture drama: joker picture com/mus: once upon a time in hollywood director: martin scorsese screenplay: marriage story score: 1917 foreign film: parasite animated: frozen 2 song: Im gonna love me again - elton john "

print([(X.text, X.label_) for X in nlp(str).ents])
