
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

import json
import string
import logging, time

# maakes the quiz object everytime a user starts the test
class Quiz:
    def __init__(self , update=None , Questions='Questions.json'):
        self.update=update
        self.Questions=Questions
        self.correct_words=0
        self.correct_non_words=0
        self.answered=0

# fetches the next word to be asked
    def get_next_word(self):
        with open(self.Questions) as json_file:
            self.data = json.load(json_file)
        try:
            return [str(self.answered+1),self.data[str(self.answered+1)]["word"],self.data[str(self.answered+1)]["correct"]]
        except:
            return None

# gets the answer of the poll as input and updates quiz results
    def update_result(self , count):
        if self.answered>2:
            with open(self.Questions) as json_file:
                self.data = json.load(json_file)
            if((count==1) and (int(self.data[str(self.answered+1)]["correct"]) ==0)):
                self.correct_non_words+=1
            elif((count==1) and (int(self.data[str(self.answered+1)]["correct"]) ==1)):
                self.correct_words+=1
        self.answered+=1

# calculates the user's final score based on the formula
    def score(self):
        return ((self.correct_words/40*100) + (self.correct_non_words/20*100))/2

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# creates the quiz instance upon the interaction
q=Quiz()

# called when the user enters the start command
# introduces the bot and asks the user to participate in the test
def start(update, context):
    me = context.bot.get_me()
    msg = (f"Hello!\n I'm {me.first_name} and I came here to help you improve your vocabulary.\n"
           "First, I need to know your current level.\n Are you ready to take the test?\n"
           "/ready - Let's start the test!\n /stop - We'll do it later\n\n")
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
      "/test - Start the test.\n"
      "/stop - We'll do it later\n\n")
    main_menu_keyboard = [[KeyboardButton('/test')],[KeyboardButton('/stop')]]
    reply_kb_markup = ReplyKeyboardMarkup(main_menu_keyboard,resize_keyboard=True,one_time_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg, reply_markup=reply_kb_markup)


# called when the user enters the stop command
# sends the message and deletes the quiz instance
def stop(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ok, no problem. See you next time then!")
    del q


# called when the user enters the test command
# sets the update attribute of the quiz object and reset other attribues in order to start the test multiple times
# if theres no word left to be asked, calls the end_test function, else gets next word from quiz object, makes the poll and send it
def test(update, context):
    if update.effective_message != None:
        q.update=update
        q.correct_words=0
        q.correct_non_words=0
        q.answered=0
    if q.get_next_word()==None:
        return end_test(q.update, context)
    options = ["No", "Yes"]
    word = q.get_next_word()
    question = f'{str(max((int(word[0])-3),0))}. Does the word "{word[1]}" exist?'
    message = q.update.message.reply_poll(question, options, type=Poll.QUIZ, correct_option_id=word[2])
    payload = {message.poll.id: { "chat_id": q.update.effective_chat.id,"message_id": message.message_id}}
    context.bot_data.update(payload)


# used when the user enters the answer to a poll
# gets the user's answer and call the update_result method of the quiz object
# calls the test function to send the next poll or end the test
def receive_quiz_answer(update, context):
    if update.poll.total_voter_count == 1:
        correct = update.poll.correct_option_id
        res=int(update.poll.options[correct].voter_count)
        q.update_result(res)
    test(update, context)


# called when the user enters there is no word to ask
# calls the score method of the quiz object and sends the result to the user
# calls the preferred_genre function
def end_test(update, context):
    score=q.score()
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'You finished the test! Great job, you got a score of {q.score()}!')

    preferred_genre(update, context)

# asks the user to select preferred genre using keyboard buttons
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


# called when the user enters a message and not a command
# two cases: the user chooses the genre or wants a definition
def message(update, context):
    msg = update.message.text
    genres = ["fiction", "academic", "news", "conversations"]
    if msg in genres:
        search_text(update, context, msg)
    else:
        definition(update, context, msg)

# looks for a text of the genre
# needs to be completed
def search_text(update, context, genre):
    msg = "We are looking for a text of the genre " + genre + " for you."
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
    tell_sentence(update, context)


# shows the sentence
# needs to be completed with different sentences
def tell_sentence(update, context):
    sentence = "Hello World! This is a test sentence, to see if you can read it."
    msg = sentence + ("\n\n/continue - I understood everything, let's go for the next sentence!\n"
      "/explanations - I didn\'t understand some words, can you help me?")
    main_menu_keyboard = [[KeyboardButton('/continue')],
                          [KeyboardButton('/explanations')]]
    reply_kb_markup = ReplyKeyboardMarkup(main_menu_keyboard , resize_keyboard=True , one_time_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg, reply_markup=reply_kb_markup)


# calls next sentence
# not sure if necessary but may be useful when really implemented
# needs to be completed with real sentences
def next_sentence(update, context):
    tell_sentence(update, context)


# split the words of the sentence and create buttons to ask
def split_words(update, context, sentence="Hello World! This is a test sentence, to see if you can read it."):
    translation = str.maketrans('', '', string.punctuation)
    words = [w.translate(translation) for w in sentence.split()]
    main_menu_keyboard = []
    msg = "What word did you not understand?"
    for w in words:
        main_menu_keyboard.append([KeyboardButton(w)])
    reply_kb_markup = ReplyKeyboardMarkup(main_menu_keyboard , resize_keyboard=True , one_time_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg, reply_markup=reply_kb_markup)


# provides definiton of the chosen word
# needs to be completed
def definition(update, context, word):
    msg = "Definition of the word " + word
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


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
    dp.add_handler(CommandHandler('test', test))
    dp.add_handler(CommandHandler('continue', next_sentence))
    dp.add_handler(CommandHandler('explanations', split_words))

# message handlers
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), message))
# Handler instance to handle Telegram updates that contain a poll
    dp.add_handler(PollHandler(receive_quiz_answer))
# Starts polling updates from Telegram
    updater.start_polling()
# Blocks until one of the signals are received and stops the updater
    updater.idle()


if __name__ == '__main__':

    main()
