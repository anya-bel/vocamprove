from nltk.corpus import wordnet as wn
#import nltk
#nltk.download('wordnet')
import spacy
from gtts import gTTS
import numpy as np
import pandas as pd
import csv

# (mock input)
text_index = 5
sentence_index = 5
word_index = 5

word = 'project'
POS_abb = 'v'


# (mock interactive input)
# text_index = input('text index:\n')
# sentence_index = input('sentence index:\n')
# word_index = input('word index:\n')

def locate():
    path = './data/words.csv'

    with open(path, 'r', newline='') as file:
        reader = csv.reader(file, delimiter=',')
        df = pd.DataFrame(reader)
        
        csv_row = df.loc[(df['text-index'] == text_index) & (df['word-index'] == word_index) & (df['sentence-index'] == sentence_index)]
               
        print(csv_row)

# WORD DEFINITION FROM WORDNET
def find_definition():
    columns=['Lemma', 'Definition', 'Example']
    definition = pd.DataFrame(columns=columns)
                              
    for synset in wn.synsets(word)[0:-1]:
        
        if synset.name()[-4] == POS_abb:
        
            # TO DO ► RegEx POS, definition and examples.
            
            #name = synset.name()[-4]
            define = synset.definition()
            example = synset.examples()

            syn = pd.DataFrame(np.array([[name, define, example]], dtype=object), columns=columns)

            definition = definition.append(syn)

    return(definition)

# DEPENDENCY
def find_dependency():
    
    dependency = 'syntactic tag (ex. auxiliary)'
    return(dependency)

# POS
def find_POS():
    POS = ''
    return(POS)
    
# PRONUNCIATION
def find_pronunciation():
    tts = gTTS(word)
    tts.save(word+'.mp3')

# OUTPUT
def word_info():
    print('Definition:')
    print(definition)
    print('Dependency:')
    print(dependency)
    print('POS:')
    print(POS)

if __name__ == "__main__":
    locate()
    definition = find_definition()
    dependency = find_dependency()
    POS = find_POS()
    find_pronunciation()
    word_info()