from xml.etree import ElementTree as ET
import csv
import glob

#---------------------------
#-----SET-UP-DATA-FILES-----
#---------------------------

data_path = r'C:\Users\lubri\Documents\GitHub\Vocamprove\data\\'

# set up words.csv file
with open((data_path + 'words.csv'), "w", newline='', encoding='utf-8') as file:

    # create the csv writer object
    csvwriter = csv.writer(file)

    # write column names
    col_names = ['word-index','word','sentence-index','text-index','POS']
    csvwriter.writerow(col_names)

# set up text.csv file
with open((data_path + 'text.csv'), "w", newline='', encoding='utf-8') as file:

    # create the csv writer object
    csvwriter = csv.writer(file)

    # write column names
    col_names = ['text-index','text','genre','complexity']
    csvwriter.writerow(col_names)



#----------------------------------
#-----RETRIEVE-VALUES-FROM-XML-----
#-----FILL-CSV-FILE-W/-VALUES------
#----------------------------------

# define path of the xml files
xml_path = r'C:\Users\lubri\Documents\GitHub\Vocamprove\Texts\**\*.xml'

# set counters for increasing variables
text_index = 0
word_index = 0

for f in glob.iglob(xml_path):

    # empty text var each time a new text file is opened
    text = ''

    #assign text index var to be used in words.csv and text.csv 
    text_index =+ 1

    with open(f, 'r', encoding='utf-8') as f:
        tree = ET.parse(f)
        root = tree.getroot()

        # iterate through sentences
        for s in root.iter('s'):

            #assign sentence index var to be used in text.csv
            sentence_index = int(s.attrib['n'])

            # (for debugging)
            if sentence_index == 5:
                quit()

            # iterate through words in each sentence
            for w in s.iter('w'):
                word_index = word_index + 1

                #assign POS var to be used in text.csv
                POS = w.attrib['pos']

                #assign word var to be used in words.csv
                word = w.text

                # open words.csv in append mode
                with open((data_path + 'words.csv'), "a", newline='', encoding='utf-8') as file:

                    # create the csv writer object
                    csvwriter = csv.writer(file)
                    csvwriter.writerow([word_index, word, sentence_index, text_index, POS])


    # TO DO ► retrieve text

    # TO DO ► open text.csv in data folder

    # TO DO ► create structure & insert data



            