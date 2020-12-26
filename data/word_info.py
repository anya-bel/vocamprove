from nltk.corpus import wordnet as wn
#import nltk
#nltk.download('wordnet')
import spacy
from gtts import gTTS
import numpy as np
import pandas as pd
import csv
import spacy
from spacy.kb import KnowledgeBase

nlp = spacy.load("en_core_web_sm")

# (mock input)
text_index = 6
sentence_index = 5
word_index = 5

word = 'difficulty'
POS_abb = 'n'

dep = {
    'acl': 'clausal modifier of noun (adjectival clause)',
'advcl': 'adverbial clause modifier',
'advmod': 'adverbial modifier',
'amod': 'adjectival modifier',
'appos': 'appositional modifier',
'aux': 'auxiliary',
'case': 'case marking',
'cc': 'coordinating conjunction',
'ccomp': 'clausal complement',
'clf': 'classifier',
'compound': 'compound',
'conj': 'conjunct',
'cop': 'copula',
'csubj': 'clausal subject',
'dep': 'unspecified dependency',
'det': 'determiner',
'discourse': 'discourse element',
'dislocated': 'dislocated elements',
'expl': 'expletive',
'fixed': 'fixed multiword expression',
'flat': 'flat multiword expression',
'goeswith': 'goes with',
'iobj': 'indirect object',
'list': 'list',
'mark': 'marker',
'nmod': 'nominal modifier',
'nsubj': 'nominal subject',
'nummod': 'numeric modifier',
'obj': 'object',
'obl': 'oblique nominal',
'orphan': 'orphan',
'parataxis': 'parataxis',
'punct': 'punctuation',
'reparandum': 'overridden disfluency',
'root': 'root',
'vocative': 'vocative',
'xcomp': 'open clausal complement',
}

pos_anno = {'VERB': 'verb',
 'PREP': 'preposition',
 'ART': 'article',
 'SUBST': 'substantive',
 'ADV': 'adverb',
 'ADJ': 'adjective',
 'CONJ': 'conjunction',
 'PRON': 'pronoun',
 'UNC': 'unclassified',
 'INTERJ': 'interjection'}


#(mock interactive input for debugging)
# text_index = input('text index:\n')
# sentence_index = input('sentence index:\n')
# word_index = input('word index:\n')

def locate(text_index, sentence_index, word_index):
    words_path = '../data/csv-files/words.csv'
    words_df = pd.read_csv(words_path)
    word_csv_row = words_df.loc[(words_df['text-index'] == text_index) & (words_df['word-index'] == word_index) & (words_df['sentence-index'] == sentence_index)]
    sentences_path = '../data/csv-files/sentences.csv'
    sentences_df = pd.read_csv(sentences_path)
    sent_csv_row = sentences_df.loc[(sentences_df['text-index'] == text_index) & (sentences_df['sentence-index'] == sentence_index)]
    return word_csv_row['word-index'].iloc[0], word_csv_row['word'].iloc[0].strip(), word_csv_row['POS'].iloc[0], sent_csv_row['sentence'].iloc[0]

# WORD DEFINITION FROM WORDNET
def find_definition(word, POS):
    columns=['Word', 'Definition', 'Example']
    definition = pd.DataFrame(columns=columns)
    pos_wn = {'ADJ': 'a',
              'SUBST': 'n',
              'VERB': 'v',
              'ADV': 'r'}
    pos = pos_wn.get(POS)
    if pos:
        for synset in wn.synsets(word)[0:-1]:
            if synset.name()[-4] == pos:
                # TO DO ► RegEx POS, definition and examples.

                define = synset.definition()
                example = synset.examples()

                syn = pd.DataFrame(np.array([[word, define, example]], dtype=object), columns=columns)

                definition = definition.append(syn)
    else:
        for synset in wn.synsets(word)[0:-1]:
            define = synset.definition()
            example = synset.examples()
            syn = pd.DataFrame(np.array([[word, define, example]], dtype=object), columns=columns)
            definition = definition.append(syn)

    if definition.empty:
        syn = pd.DataFrame(np.array([[word, '', []]], dtype=object), columns=columns)
        definition = definition.append(syn)
        return definition
    return(definition)

# DEPENDENCY
def find_dependency(idx, word, sentence):
    doc = nlp(sentence)
    for num, token in enumerate(doc):
        if token.text == word:
            if idx-1 <= num <= idx+1:
                dependency = token.dep_
                break
    return dep[dependency]


"""
# POS
def find_POS():
    doc = nlp(sentence)
    POS = word, word.lemma_
    return(POS)
"""
    
# PRONUNCIATION
def find_pronunciation(word):
    tts = gTTS(word)
    tts.save(word+'.mp3')
    return word+'.mp3'

# OUTPUT
def word_info(definition, dependency, POS, audiopath):
    print(f'Definition: {definition}')
    print(f'Dependency: {dependency}')
    print(f'POS: {POS}')
    print(f'Path to mp3: {audiopath}')

if __name__ == "__main__":
    idx, word, POS, sentence = locate(text_index, sentence_index, word_index)
    definition = find_definition(word, POS)
    dependency = find_dependency(idx-1, word, sentence)
    #POS = find_POS(word)
    audiopath = find_pronunciation(word)
    POS = pos_anno[POS]
    word_info(definition, dependency, POS, audiopath)
