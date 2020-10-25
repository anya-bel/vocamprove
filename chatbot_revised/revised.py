
from telegram import (
    Poll,
    KeyboardButton,
    ReplyKeyboardMarkup)

from telegram.ext import (
    Updater,
    CommandHandler,
    PollHandler)

import json
import logging, time

class Quiz:
    def __init__(self , update=None , Questions='Questions.json'):
        self.update=update
        self.Questions=Questions
        self.correct_words=0
        self.correct_non_words=0
        self.answered=0
    
    def get_next_word(self):
        with open(self.Questions) as json_file:
            self.data = json.load(json_file)
        try:
            return [str(self.answered+1),self.data[str(self.answered+1)]["word"],self.data[str(self.answered+1)]["correct"]]
        except:
            return None
    
    def update_result(self , count):
        if self.answered>2:
            with open(self.Questions) as json_file:
                self.data = json.load(json_file) 
            if((count==1) and (int(self.data[str(self.answered+1)]["correct"]) ==0)):
                self.correct_non_words+=1
            elif((count==1) and (int(self.data[str(self.answered+1)]["correct"]) ==1)):
                self.correct_words+=1
        self.answered+=1
        
    def score(self):
        return ((self.correct_words/40*100) + (self.correct_non_words/20*100))/2
    
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

q=Quiz()
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
def ready(update, context):
    msg = ("This test consists of about 60 trials, in each of which you will see a string of letters. "
      "Your task is to decide whether this is an existing English word or not. "
      "If you think it is an existing English word, you click on \"yes\", and if you think it is not an existing English word, you click on \"no\".\n\n"
      "If you are sure that the word exists, even though you don’t know its exact meaning, you may still respond \"yes\". "
      "But if you are not sure if it is an existing word, you should respond \"no\".\n\n"
      "In this experiment, we use British English rather than American English spelling. "
      "For example: \"realise\" instead of \"realize\"; \"colour\" instead of \"color\", and so on. "
      "Please don’t let this confuse you. "
      "This experiment is not about detecting such subtle spelling differences anyway.\n\n"
      "You have as much time as you like for each decision. This part of the experiment will take about 5 minutes.\n"
      "If everything is clear, you can now start the experiment.\n\n"
      "/test - Start the test.\n"
      "/stop - We'll do it later\n\n")
    main_menu_keyboard = [[KeyboardButton('/test')],[KeyboardButton('/stop')]]
    reply_kb_markup = ReplyKeyboardMarkup(main_menu_keyboard,resize_keyboard=True,one_time_keyboard=True)                                                 
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg, reply_markup=reply_kb_markup)

def stop(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ok, no problem. See you next time then!")
    del q

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
    question = f'{str(word[0])}. Does the word "{word[1]}" exist?'
    message = q.update.message.reply_poll(question, options, type=Poll.QUIZ, correct_option_id=word[2])
    payload = {message.poll.id: { "chat_id": q.update.effective_chat.id,"message_id": message.message_id}}
    context.bot_data.update(payload)
        
def receive_quiz_answer(update, context):
    if update.poll.total_voter_count == 1:
        correct = update.poll.correct_option_id
        res=int(update.poll.options[correct].voter_count)
        q.update_result(res)
    test(update, context)

def end_test(update, context):
    score=q.score()
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'You finished the test! Great job, you got a score of {q.score()}!')
    
    preferred_genre(update, context)

    
def preferred_genre(update, context):
    msg = ("Now that I now your current vocabulary level, I can find a text that matches it.\n"
      "But first, tell me a bit more about you. "
      "What do you prefer reading?\n\n"
      "/fiction - I love fiction, want to read this kind of texts!\n"
      "/academic - I prefer reading serious papers\n"
      "/news - I want to get informed about news!\n"
      "/conversations - I prefer something more natural.")
    main_menu_keyboard = [[KeyboardButton('/fiction')],
                          [KeyboardButton('/academic')],
                          [KeyboardButton('/news')],
                          [KeyboardButton('/conversations')]]
    reply_kb_markup = ReplyKeyboardMarkup(main_menu_keyboard , resize_keyboard=True , one_time_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg, reply_markup=reply_kb_markup)

    
    
def main():
    updater = Updater("1239802799:AAGS-N9DZWpzTHjYm1pcXQ6sChzQVpuQQqA", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('ready', ready))
    dp.add_handler(CommandHandler('stop', stop))
    dp.add_handler(CommandHandler('test', test))
    dp.add_handler(PollHandler(receive_quiz_answer))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':

    main()
