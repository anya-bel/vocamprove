# Vocamprove

Vocamprove is a language learning tool for English, focused on vocabulary building. It is presented to the user as a Telegram chatbot carrying out the main tasks of: (1) assessing the user’s English vocabulary size, (2)recording their reading genre preferences, (3) providing them with suitable reading material, based on such preferences and vocabulary size, and (4) provide the user with information on unknown words in order to help them enrich their English vocabulary. 
Telegram chatbot communicates the vocabulary size test questions. The user's test result is then mapped to CEFR(Common European Framework of Reference for Languages) level and then used to suggest text based on the preferred genre from the corpus (British National Corpus).
Text sample's level is assessed using a number of lexical complexity estimation methods(???)
Suitable text sample based on user's preference and level is then offered to the user, one sentence at a time. user would be able to continue to read, or ask the bot to explain some unknown word. user would be asked to chose the unknown word and will receive the following information: 
The Pronunciation, definition of the word's meaning, other examples of the word's usage, and the dependency graph of the sentence.


## Installation
For prequisites, please check [requirements](https://github.com/anya-bel/vocamprove/blob/main/requirements.txt)

Run the [Chatbot.py](https://github.com/anya-bel/vocamprove/blob/main/chatbot/chatbot.py) script to make a vocabulary test based on the words mentioned in [Questions](https://github.com/anya-bel/vocamprove/blob/main/chatbot/Questions.json).

```bash
#

```

## Usage

```python
#Chatbot

#Command Handlers
start(update, context) # sends information about the bot
ready(update, context) # asks for user confirmation to start the test
stop(update, context) # terminates the conversation
#Message Handler
common_message # sends vocab test questions, processes the answers, and communicates the result 
#Other Functions
score_to_level(update, context, score) # maps the test result into CEFR level
preferred_genre(update, context) # asks the preferred genre
search_text(update, context, genre) #looks up the sentences for the user based on genre and level 
pick_sentence(update, context) # picks the random sample of the text for the user
tell_sentence(update, context) # sends the sentence
split_words(update, context) # offers the words of the sentence in the form of seperate buttons to the user to choose the unknown one
find_definition(word, pos) # looks up the definition from wordnet
find_dependency(idx, word, sentence) # looks up the dependency from 'en_core_web_sm' model of Spacy package
definition(update, context, word, index) # sends the definition, pronunciation and dependency


```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
