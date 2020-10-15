from xml.etree import ElementTree as ET
import csv
import glob
import pandas as pd
import numpy as np
from itertools import chain
import spacy
import time
startTime = time.time()

#---------------------------------------------------------------------------------
#-----SET-UP-DATA-FILES-----------------------------------------------------------
#---------------------------------------------------------------------------------
#-----------------SETTING UP 3 CSV FILES------------------------------------------
# STORING: INDIVIDUAL WORDS, SENTENCES AND TEXTS----------------------------------
#---------------------------------------------------------------------------------

# define path to store data
data_path = r'data/'

# set up words.csv file
with open((data_path + 'words.csv'), "w", newline='', encoding='utf-8') as file:

    # create the csv writer object
    csvwriter = csv.writer(file)

    # write column names
    col_names = ['word-index','word','sentence-index','text-index','POS']
    csvwriter.writerow(col_names)

# set up sentences.csv file
with open((data_path + 'sentences.csv'), "w", newline='', encoding='utf-8') as file:

    # create the csv writer object
    csvwriter = csv.writer(file)

    # write column names
    col_names = ['sentence-index','sentence','text-index']
    csvwriter.writerow(col_names)
    print('sentences.csv created')
    
# set up text.csv file
with open((data_path + 'texts.csv'), "w", newline='', encoding='utf-8') as file:

    # create the csv writer object
    csvwriter = csv.writer(file)

    # write column names
    col_names = ['text-index','genre','complexity']
    csvwriter.writerow(col_names)


    
#----------------------------------
#-----RETRIEVE-VALUES-FROM-XML-----
#-----FILL-CSV-FILE-W/-VALUES------
#----------------------------------

# define path of the XML files
xml_path = r'Texts/**/*.xml'

# set counters for increasing variables
text_index = 0
genres = {'a': 'academic','d': 'conversations', 'f': 'fiction', 'n': 'news'}

# iterate through each XML file
for f in glob.iglob(xml_path):

    sentence_index = 0

    #assign text index var to be used in words.csv and text.csv
    text_index += 1

    # TO DO ► find complexity score
    complexity = 0

    # find genre
# TO DO ► substitute with RegEx
    genre = genres[f[6]]

    # open words.csv in append mode
    with open((data_path + 'texts.csv'), "a", newline='', encoding='utf-8') as file:

        # create the csv writer object
        csvwriter = csv.writer(file)
        csvwriter.writerow([text_index, genre, complexity])


    # import XML file
    with open(f, 'r', encoding='utf-8') as f:
        tree = ET.parse(f)
        root = tree.getroot()

        # iterate through sentences
        for s in root.iter('s'):

            word_index = 0
            sentence_index += 1

            #assign sentence_index var
            # sentence_index = int(s.attrib['n'])

            sentence_as_word_list = []

            ## (for debugging)
            #if sentence_index == 5:
            #    break

            # iterate through units in each sentence
            for u in list(s):

                ## iterate through words in each sentence
                #for w in s.iter('w'):
                
                unit = ET.tostring(u, encoding='unicode')

                # if unit is a word, extract POS
                if unit[1] == ('w'):
                    word = u.text
                    word_index = word_index + 1

                    #assign POS var to be used in texts.csv
                    POS = u.attrib['pos']
                    
                    # open words.csv in append mode
                    with open((data_path + 'words.csv'), "a", newline='', encoding='utf-8') as file:

                        # create the csv writer object
                        csvwriter = csv.writer(file)
                        csvwriter.writerow([word_index, word, sentence_index, text_index, POS])                

                #assign word var to be used in words.csv
                unit = u.text

                # store word into sentence
                if unit is not None:
                    sentence_as_word_list.append(unit)
                    sentence = ''.join(sentence_as_word_list)


            # set up sentences.csv file
            with open((data_path + 'sentences.csv'), "a", newline='', encoding='utf-8') as file:

                # create the csv writer object
                csvwriter = csv.writer(file)

                # write column names
                csvwriter.writerow([sentence_index, sentence, text_index])

        ## (for debugging)
        #if  text_index == 5:
        #    break


                    
#---------------------------------------------------------------------------------
#-----TURN-CSV-INTO-DF------------------------------------------------------------
#---------------------------------------------------------------------------------


    
    
#if __name__ == "__main__":convert_to_csv()


executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))