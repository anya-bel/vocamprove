#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from telegram import (
    Poll,
    KeyboardButton,
    ReplyKeyboardMarkup)

from telegram.ext import (
    Updater,
    CommandHandler,
    PollHandler,
    MessageHandler,
    Filters)
from gtts import gTTS
from nltk.corpus import wordnet as wn
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg
import spacy
import numpy as np
import pandas as pd
import en_core_web_sm
import csv
import json
import string
import random
import os
import logging, time


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)



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



# called when the user enters the start command
# introduces the bot and asks the user to participate in the test
def start(update, context):
    me = context.bot.get_me()
    msg = (f"Hello!\nI'm {me.first_name} and I came here to help you improve your vocabulary.\n"
           "First, I need to know your current level.\n Are you ready to take the test?\n"
           "/ready - Let's start the test!\n /stop - We'll do it later\n"
           "At any time in this conversation, press /stop to close the bot.\n\n")
    main_menu_keyboard = [[KeyboardButton('/ready')],
                          [KeyboardButton('/stop')]]
    reply_kb_markup = ReplyKeyboardMarkup(main_menu_keyboard,
                                                   resize_keyboard=True,
                                                   one_time_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg, reply_markup=reply_kb_markup)

# called when the user enters the ready command
# explains the test to the user and asks the user to start
def ready(update, context):
    msg = ("This test consists of about 60 trials, in each of which you will see a string of letters. "
      "Your task is to decide whether this is an existing English word or not. "
      "If you think it is an existing English word, select \"yes\", and if you think it is not an existing English word, select \"no\".\n\n"
      "If you are sure that the word exists, even though you don’t know its exact meaning, you should still respond \"yes\". "
      "However, if you are not sure if it is an existing word or not, you should respond \"no\".\n\n"
      "In this experiment, we use British English rather than American English spelling. "
      "For example: \"realise\" instead of \"realize\"; \"colour\" instead of \"color\", and so on. "
      "Please don’t let this confuse you: "
      "this experiment is not about detecting such subtle spelling differences.\n\n"
      "You have as much time as you like for each decision. This part of the experiment will take about 5 minutes.\n"
      "If everything is clear, you can now start the test.\n\n"
      "test - Start the test.\n"
      "/stop - We'll do it later\n\n")
    main_menu_keyboard = [[KeyboardButton('test')],[KeyboardButton('/stop')]]
    reply_kb_markup = ReplyKeyboardMarkup(main_menu_keyboard,resize_keyboard=True,one_time_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg, reply_markup=reply_kb_markup)


# called when the user enters the stop command
# sends the message and deletes the quiz instance
def stop(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ok, no problem. See you next time then!")


def common_message(update, context):
    msg = update.message
    user = msg.from_user
    if msg.text in ["test", "Yes", "No"]:
        if 'quiz' not in context.user_data:
            context.user_data['quiz'] = {}
            context.user_data['quiz']['correct_words']=0
            context.user_data['quiz']['correct_nonwords']=0
            context.user_data['quiz']['current_qid']=0
        else:
            if (msg.text=='No' and int(context.user_data['quiz']['current_res'])==0):
                context.bot.send_message(msg.chat_id, text="Correct answer!")
                if context.user_data['quiz']['current_qid']>3:
                    context.user_data['quiz']['correct_nonwords']+=1
            elif (msg.text=='Yes' and int(context.user_data['quiz']['current_res'])==1):
                context.bot.send_message(msg.chat_id, text="Correct answer!")
                if context.user_data['quiz']['current_qid']>3:
                    context.user_data['quiz']['correct_words']+=1
            else:
                context.bot.send_message(msg.chat_id, text="Wrong answer...")

        if (int(context.user_data['quiz']['current_qid'])< 63):
            with open('Questions.json') as json_file:
                data = json.load(json_file)
            word = [str(context.user_data['quiz']['current_qid']+1),
                    data[str(context.user_data['quiz']['current_qid']+1)]["word"],
                    data[str(context.user_data['quiz']['current_qid']+1)]["correct"]]
            question = ""
            if int(word[0]) - 3 > 0:
                question += f'{str((int(word[0])-3))}. '
            question += f'Does the word "{word[1]}" exist?'
            response_keyboard = [[KeyboardButton('Yes')],
                                [KeyboardButton('No')]]
            reply_kb = ReplyKeyboardMarkup(response_keyboard,
                                                       resize_keyboard=True,
                                                       one_time_keyboard=True)
            context.bot.send_message(msg.chat_id, text=question, reply_markup=reply_kb)
            context.user_data['quiz']['current_qid'] = int(word[0])
            context.user_data['quiz']['current_res'] = int(word[2])

#         when user has answered all the question
        else:
            score = ((context.user_data['quiz']['correct_words']/40*100) + (context.user_data['quiz']['correct_nonwords']/20*100))/2
            if msg.text == "test":
                msgError = "This test is meant to be taken only once by you, we will offer you some text based on your previous results."
                msgError += f'For a reminder, you got a score of {score}.'
                context.bot.send_message(chat_id=msg.chat_id, text=msgError)
            else:
                context.bot.send_message(chat_id=msg.chat_id, text=f'You finished the test! Great job, you got a score of {score}!')

            # transforms the score into level
            context.user_data['level'] = score_to_level(update, context, score)

#           calls the preferred_genre function
            preferred_genre(update, context)
    else:
        msg = update.message.text
        genres = ["fiction", "academic", "news", "conversations"]
        if msg in genres:
            search_text(update, context, msg)
        else:
            definition(update, context, msg, context.user_data['text']['words'].index(msg))


def score_to_level(update, context, score):
    if score <= 50:
        return "A2"
    if score <= 59:
        return "B1"
    if score <= 80:
        return "B2"
    if score <= 90:
        return "C1"
    return "C2"


def preferred_genre(update, context):
    msg = ("Now that I know your current vocabulary level, I can find something you might enjoy reading.\n"
      "But first, tell me a bit more about you. "
      "What do you prefer reading?\n\n"
      "fiction - I love fiction, and would love to read this kind of texts!\n"
      "academic - I like reading studies and essays.\n"
      "news - I want to read stories about real life events.\n"
      "conversations - I prefer something more casual.")
    main_menu_keyboard = [[KeyboardButton('fiction')],
                          [KeyboardButton('academic')],
                          [KeyboardButton('news')],
                          [KeyboardButton('conversations')]]
    reply_kb_markup = ReplyKeyboardMarkup(main_menu_keyboard , resize_keyboard=True , one_time_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg, reply_markup=reply_kb_markup)



# looks for a text of the genre
# needs to be completed
def search_text(update, context, genre):
    level = context.user_data['level']

    rows_to_read = []
    if genre == "academic":
        rows_to_read = range(1, 30)
    elif genre == "conversations":
        rows_to_read = range(31, 60)
    elif genre == "fiction":
        rows_to_read = range(61, 85)
    else:
        rows_to_read = range(86, 182)

    with open('../data/csv-files/labeled_texts.csv') as f:
        reader = csv.reader(f)
        interesting_rows = [row for i, row in enumerate(reader) if i in rows_to_read]
        print(level, genre)

    rows = []
    for row in interesting_rows:
        if row[2] == level:
            rows.append(row[0])
    if len(rows) == 0:
        msg_error = "Oops, we don't have any matching text in our corpus yet..."
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg_error)
        preferred_genre(update, context)
        return

    context.user_data['text'] = {}
    context.user_data['text']['nb_text'] = int(random.choice(rows))
    context.user_data['text']['nb_sentence'] = 1
    tell_sentence(update, context)


# shows the sentence
# needs to be completed with different sentences
def tell_sentence(update, context):
    print(context.user_data['text']['nb_text'], context.user_data['text']['nb_sentence'])
    sentence = pick_sentence(update, context)
    if sentence == None:
        msg = "Hooray! You finished the text!"
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
    else:
        context.user_data['text']['sentence'] = sentence
        msg = sentence + ("\n\n/continue - I understood everything, let's go for the next sentence!\n"
         "/explanations - I didn\'t understand some words, can you help me?")
        main_menu_keyboard = [[KeyboardButton('/continue')],
                            [KeyboardButton('/explanations')]]
        reply_kb_markup = ReplyKeyboardMarkup(main_menu_keyboard , resize_keyboard=True , one_time_keyboard=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg, reply_markup=reply_kb_markup)


def pick_sentence(update, context):
    sentence = ""
    with open('../data/csv-files/sentences.csv') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if int(row[2]) == context.user_data['text']['nb_text'] and int(row[0]) == context.user_data['text']['nb_sentence']:
                sentence = row[1]
                context.user_data['text']['nb_sentence'] += 1
                break
            if int(row[2]) > context.user_data['text']['nb_text']:
                print(type(row[2]), row[2])
                return None
    return sentence



# split the words of the sentence and create buttons to ask
def split_words(update, context):
    sentence = context.user_data['text']['sentence'].lower()
    translation = str.maketrans('', '', string.punctuation)
    words = [w.translate(translation) for w in sentence.split()]
    context.user_data['text']['words'] = words
    main_menu_keyboard = []
    msg = "What word did you not understand?"
    for w in words:
        main_menu_keyboard.append([KeyboardButton(w)])
    reply_kb_markup = ReplyKeyboardMarkup(main_menu_keyboard , resize_keyboard=True , one_time_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg, reply_markup=reply_kb_markup)


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

                syn = pd.DataFrame(np.array([[word, define, example]]), columns=columns)

                definition = definition.append(syn)
    else:
        for synset in wn.synsets(word)[0:-1]:
            define = synset.definition()
            example = synset.examples()
            syn = pd.DataFrame(np.array([[word, define, example]]), columns=columns)
            definition = definition.append(syn)

    if definition.empty:
        syn = pd.DataFrame(np.array([[word, '', []]]), columns=columns)
        definition = definition.append(syn)
        return definition
    return(definition)

def find_dependency(idx, word, sentence):
    try:
        nlp = en_core_web_sm.load()
        doc = nlp(sentence)
        svg = spacy.displacy.render(doc, style="dep", jupyter=False)
        file_name = word+'.svg'
        with open(file_name, 'w') as image:
            image.write(svg)
        drawing = svg2rlg(word+'.svg')
        renderPM.drawToFile(drawing, word+'.png', fmt="PNG")
        os.remove(word+'.svg')
        dependency = ""
        for num, token in enumerate(doc):
            if token.text == word:
                if idx-1 <= num <= idx+1:
                    dependency = token.dep_
                    break
        return dep[dependency]
    except:
        return "Not found"

# provides definiton of the chosen word
# needs to be completed
def definition(update, context, word, index):
    try:
        df = pd.read_csv('../data/csv-files/words.csv')
        word_index = int(index)+1
        text_index = context.user_data['text']['nb_text']
        sentence_index = int(context.user_data['text']['nb_sentence']) -1
        sentence = context.user_data['text']['sentence']
        csv_row = df.loc[(df['text-index'] == text_index) & (df['word'] == word+' ') & (df['sentence-index'] == sentence_index)]
        POS_abb = csv_row['POS'].values[0]
        definition_df = find_definition(word, POS_abb)
        definition=''
        for index in range(len(definition_df)):
            if len(definition_df.iloc[index]['Definition'])>0:
                definition+= f'\ndefinition number  {index+1}:\n'
                definition+= definition_df.iloc[index]['Definition']
                definition+= "\n"
            else:
                definition+= f'\n'
            if len(definition_df.iloc[index]['Example'])>0:
                definition+= f'An example of this would be: \n'
                if type(definition_df.iloc[index]['Example'])==list:
                    definition+= '__'+definition_df.iloc[index]['Example'][0]+'__'
                else:
                    definition+= '__'+definition_df.iloc[index]['Example']+'__'
                definition+= f'\n'
    except:
        definition = "Definition not found."
    msg = ""
    try:
        tts = gTTS(word)
        audio_name = str(word+'.mp3')
        tts.save(audio_name)
        context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(audio_name, 'rb'))
        os.remove(audio_name)
        msg += "This was the pronounciation.\n"
    except:
        msg+= "Pronunciation not found.\n"

    depend = find_dependency(word_index,word,sentence)
    msg += f'{definition}\nThe dependency of this word is: {depend}'

    main_menu_keyboard = [[KeyboardButton('/continue')],
                        [KeyboardButton('/explanations')]]
    reply_kb_markup = ReplyKeyboardMarkup(main_menu_keyboard , resize_keyboard=True , one_time_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg, reply_markup=reply_kb_markup)
    try:
        photo_name = str(word+'.png')
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(photo_name, 'rb'))
        os.remove(photo_name)
    except:
        pass



def main():
# creates the updater object to provide a frontend to bot. it receives the updates from Telegram
    updater = Updater("1239802799:AAGS-N9DZWpzTHjYm1pcXQ6sChzQVpuQQqA", use_context=True)
# Dispatcher handles the updates and dispatches them to the handlers
    dp = updater.dispatcher
# command handlers Handler instance to handle Telegram commands.
# Commands are Telegram messages that start with /
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('ready', ready))
    dp.add_handler(CommandHandler('stop', stop))
    dp.add_handler(CommandHandler('continue', tell_sentence))
    dp.add_handler(CommandHandler('explanations', split_words))

# message handlers
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), common_message))
#     dp.add_handler(MessageHandler(Filters.text & (~Filters.command), message))
# Handler instance to handle Telegram updates that contain a poll

# Starts polling updates from Telegram
    updater.start_polling()
# Blocks until one of the signals are received and stops the updater
    updater.idle()


if __name__ == '__main__':

    main()
