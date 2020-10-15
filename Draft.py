
        # open words.csv file for writing
        with open('words.csv', "w", newline='', encoding='utf-8') as file:

            # create the csv writer object
            csvwriter = csv.writer(file)
            head = []

        # open texts.csv file for writing
        with open('texts.csv', "w", newline='', encoding='utf-8') as file:
            # create the csv writer object
            csvwriter = csv.writer(file)
            head = []







# iterate through each child folder (representing genre)
for genre in list(f.path for f in os.scandir(text_path) if f.is_dir()):
    os.chdir(genre)

    # iterate through files in genre directories
    for filename in os.listdir(genre):
        print(os.listdir(genre))
        print(os.getcwd())
        path = (os.getcwd() + "\\" + filename)
        print(path)











counter = 0


'''


os.chdir(text_path)
print(os.getcwd())
'''

# c path = (os.getcwd() + "\\" + filename)


# iterate through each child folder (representing genre)
for genre in list(f.path for f in os.scandir(text_path) if f.is_dir()):

    #print("genre: " + genre)

    folder = (list(f.path for f in os.scandir(text_path) if f.is_dir()))[counter]

    # iterate through files in child directories
    for filename in os.listdir(genre):


        #. if (filename.endswith(".xml")):
        tree = ET.parse(filename)
        root = tree.getroot()

        counter =+ 1

        for member in root.findall('w'):
                print(member)



'''
# create CSV file with the same name
name = filename[:-4]
file = open((str(name)+'.csv'), 'w', newline='', encoding='utf-8')
csvwriter = csv.writer(file)

col_names = ['word-index','word','sentence-index','text-index','POS']
csvwriter.writerow(col_names)
'''

'''
import os
def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]
'''