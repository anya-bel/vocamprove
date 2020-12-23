from xml.etree import ElementTree as ET
import csv
import glob
import time
import pathlib
import pandas as pd

startTime = time.time()

# SET UP CSV FILES FOR STORING DATA
def create_csv():
    # Define path to store CSV files.
    data_path = r'data/'

    fieldnames_w = ['word-index', 'word', 'sentence-index', 'text-index', 'POS']
    fieldnames_s = ['sentence-index', 'sentence', 'text-index']
    fieldnames_t = ['text-index', 'genre', 'complexity']

    # Set up words.csv file.
    with open((data_path + 'words.csv'), "w", newline='', encoding='utf-8') as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(fieldnames_w)

    # Set up sentences.csv file.
    with open((data_path + 'sentences.csv'), "w", newline='', encoding='utf-8') as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(fieldnames_s)

    # Set up text.csv file.
    with open((data_path + 'texts.csv'), "w", newline='', encoding='utf-8') as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(fieldnames_t)


# RETRIEVE VALUES FROM XML AND STORE THEM IN CSV FILES
def from_xml_to_csv():
    # Define path of the XML files.
    xml_path = r'Texts/**/*.xml'

    # Define path to store CSV files.
    data_path = r'data/'

    # Set counter.
    text_index = 0

    genres = {'a': 'academic', 'd': 'conversations', 'f': 'fiction', 'n': 'news'}

    # Iterate through each XML file.
    for f in glob.iglob(xml_path):

        # Set counter.
        sentence_index = 0

        # Increase text counter each time a file is opened.
        text_index += 1

        # TO DO ► Find complexity score.
        complexity = 0

        # Find genre based on path of the file.
        dir = pathlib.PurePath(f).parts[-2]
        genre = genres[dir[0]]

        # Store text data.
        with open((data_path + 'texts.csv'), "a", newline='', encoding='utf-8') as file:

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

                # assign sentence_index var
                # sentence_index = int(s.attrib['n'])

                units = []

                ## (for debugging)
                # if sentence_index == 5:
                #    break

                # iterate through units in each sentence
                for u in list(s):

                    unit = ET.tostring(u, encoding='utf-8')


                    # if unit is a word, extract pos
                    if str(unit)[3] == 'w':

                        word = u.text
                        word_index = word_index + 1

                        # assign pos var to be used in texts.csv
                        pos = u.attrib['pos']

                        # open words.csv in append mode
                        with open((data_path + 'words.csv'), "a", newline='', encoding='utf-8') as file:
                            # create the csv writer object
                            csvwriter = csv.writer(file)
                            csvwriter.writerow([word_index, word, sentence_index, text_index, pos])

                    # assign word var to be used in words.csv
                    unit = u.text

                    # store word into sentence
                    if unit is not None:
                        units.append(unit)
                        sentence = ''.join(units)

                # set up sentences.csv file
                with open((data_path + 'sentences.csv'), "a", newline='', encoding='utf-8') as file:

                    # create the csv writer object
                    csvwriter = csv.writer(file)

                    # write column names
                    csvwriter.writerow([sentence_index, sentence, text_index])

            # (for debugging)
            #if text_index == 5:
            #    break


if __name__ == "__main__":
    create_csv()
    from_xml_to_csv()

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))
