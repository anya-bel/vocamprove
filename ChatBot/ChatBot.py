#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram import (
    Poll,
    #ParseMode,
    KeyboardButton,
    #KeyboardButtonPollType,
    ReplyKeyboardMarkup,
    #ReplyKeyboardRemove,
)
from telegram.ext import (
    Updater,
    CommandHandler,
    #PollAnswerHandler,
    PollHandler,
    MessageHandler,
    Filters,
)


from Questions import test_questions
import logging, time

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


# Called with the /start command
# Presents itself
def start(update, context):
    me = context.bot.get_me()
    # Welcome message
    msg = "Hello!\n"
    msg += "I'm {0} and I came here to help you improve your vocabulary.\n".format(me.first_name)
    msg += "First, I need to know your current level.\n"
    msg += "Are you ready to take the test?\n\n"
    msg += "/ready - Let's start the test!\n"
    msg += "/stop - We'll do it later\n\n"
    # Commands menu
    main_menu_keyboard = [[KeyboardButton('/ready')],
                          [KeyboardButton('/stop')]]
    reply_kb_markup = ReplyKeyboardMarkup(main_menu_keyboard,
                                                   resize_keyboard=True,
                                                   one_time_keyboard=True)
    # Send the message with buttons
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg, reply_markup=reply_kb_markup)


# Called with the /ready command
# Explains the test and asks if we can start it
def ready(update, context):
    msg = "This test consists of about 60 trials, in each of which you will see a string of letters. "
    msg += "Your task is to decide whether this is an existing English word or not. "
    msg += "If you think it is an existing English word, you click on \"yes\", and if you think it is not an existing English word, you click on \"no\".\n\n"
    msg += "If you are sure that the word exists, even though you don’t know its exact meaning, you may still respond \"yes\". "
    msg += "But if you are not sure if it is an existing word, you should respond \"no\".\n\n"
    msg += "In this experiment, we use British English rather than American English spelling. "
    msg += "For example: \"realise\" instead of \"realize\"; \"colour\" instead of \"color\", and so on. "
    msg += "Please don’t let this confuse you. "
    msg += "This experiment is not about detecting such subtle spelling differences anyway.\n\n"
    msg += "You have as much time as you like for each decision. This part of the experiment will take about 5 minutes.\n"
    msg += "If everything is clear, you can now start the experiment.\n\n"
    msg += "/test - Start the test.\n"
    msg += "/stop - We'll do it later\n\n"
    # Commands menu
    main_menu_keyboard = [[KeyboardButton('/test')],
                          [KeyboardButton('/stop')]]
    reply_kb_markup = ReplyKeyboardMarkup(main_menu_keyboard,
                                                   resize_keyboard=True,
                                                   one_time_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg, reply_markup=reply_kb_markup)


# Called whenever /stop command is called
# Ends the discussion
def stop(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ok, no problem. See you next time then!")


# Called first with /test command, then when user answers a test question
# Asks a test question using a poll
def test(update, context):
    global nb_question, updateTestCommand
    # Not so good, but didn't find better way...
    # Keeps the command update in memory, in order to reuse it for each question
    # (Otherwise, not possible to use update.effective_message when it's the PollHandler update)
    if update.effective_message != None:
        updateTestCommand = update
    # If we already asked all the questions, we stop the test
    if nb_question >= len(test_questions):
        return end_test(updateTestCommand, context)
    # Set the options, question and correct answer
    options = ["No", "Yes"]
    word = test_questions[nb_question]
    question = str(word[0])
    question += ". Does the word "
    question += word[1]
    question += " exist?"
    # Send the poll
    message = updateTestCommand.effective_message.reply_poll(
        question, options, type=Poll.QUIZ, correct_option_id=word[2]
    )
    payload = {
         message.poll.id: {"chat_id": updateTestCommand.effective_chat.id, "message_id": message.message_id}
    }
    context.bot_data.update(payload)
    nb_question += 1

# Every question answered, get results
def end_test(update, context):
    global correctWords, correctNonWords, nb_question
    # Calculate the score using LexTale formula
    score = ((correctWords/40*100) + (correctNonWords/20*100))/2
    msg = "You finished the test! Great job, you got a score of "
    msg += str(score)
    msg += "!"
    # Send a congratulations message
    context.bot.send_message(chat_id=updateTestCommand.effective_chat.id, text=msg)
    # Reset the variables to 0
    # Don't know if it should be reset, that allows the user to redo the test
    # Should we allow it? Don't think so but usefull for the tests
    nb_question = 0
    correctWords = 0
    correctNonWords = 0
    preferred_genre(update, context)

# Asks for the user's preferred genre
def preferred_genre(update, context):
    msg = "Now that I now your current vocabulary level, I can find a text that matches it.\n"
    msg += "But first, tell me a bit more about you. "
    msg += "What do you prefer reading?\n\n"
    msg += "/fiction - I love fiction, want to read this kind of texts!\n"
    msg += "/academic - I prefer reading serious papers\n"
    msg += "/news - I want to get informed about news!\n"
    msg += "/conversations - I prefer something more natural."

    # Commands menu
    main_menu_keyboard = [[KeyboardButton('/fiction')],
                          [KeyboardButton('/academic')],
                          [KeyboardButton('/news')],
                          [KeyboardButton('/conversations')]]
    reply_kb_markup = ReplyKeyboardMarkup(main_menu_keyboard,
                                                   resize_keyboard=True,
                                                   one_time_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg, reply_markup=reply_kb_markup)

# Called when the user chooses an answer on the poll
# Receive the user's answer
def receive_quiz_answer(update, context):
    global correctWords, correctNonWords
    # If there's one answer
    # Surely not necessary, because only one client in the chat
    if update.poll.total_voter_count == 1:
        # The 3 first questions are not taken into account
        # (See LexTale presentation)
        if nb_question >= 4:
            correct = update.poll.correct_option_id
            # If the user clicked on the good answer
            if update.poll.options[correct].voter_count == 1:
                # If it was a non-word, we add one to correct non-words score
                if correct == 0:
                    correctNonWords += 1
                # If it was a word, we add one to correct words score
                elif correct == 1:
                    correctWords += 1
        # We call test function to ask new question
        test(update, context)


# Called any time an unknown command is written
# def unknown(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1239802799:AAGS-N9DZWpzTHjYm1pcXQ6sChzQVpuQQqA", use_context=True)
    dp = updater.dispatcher

    # We set all the handlers
    #dp.add_handler(CommandHandler('unknown', unknown))
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('ready', ready))
    dp.add_handler(CommandHandler('stop', stop))
    dp.add_handler(CommandHandler('test', test))
    dp.add_handler(PollHandler(receive_quiz_answer))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    # We set the global variables
    # nb_question: Position of current question in the list
    # updateTestCommand: Update of /test command
    nb_question, updateTestCommand = 0, 0
    # correctWords: Score of correct words found
    # correctNonWords: Score of correct non-words found
    correctWords, correctNonWords = 0, 0
    main()
