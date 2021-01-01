# Vocamprove

![Vocamprove Logo](https://github.com/anya-bel/vocamprove/blob/main/img/logo_vocamprove.png =250x)

Vocamprove is a language learning tool for English, focused on vocabulary building. It is presented to the user as a Telegram chatbot carrying out the main tasks of: (1) assessing the user’s English vocabulary size, (2) recording their reading genre preferences, (3) providing them with suitable reading material, based on such preferences and vocabulary size, and (4) provide the user with information on unknown words in order to help them enrich their English vocabulary. 

#### User interaction pipeline:
After the Telegram chatbot has administered the vocabulary size test to the user, test results are mapped to CEFR (Common European Framework of Reference for Languages) and then used to suggest texts based on the preferred genre from the corpus (currently the British National Corpus, Baby Edition). The lexical CEFR level of the excerpts were assessed after evaluating four lexical complexity estimation methods. Suitable text samples based on user's preference and level are offered to the user, one sentence at a time. At each sentence, the user can decide to continue reading, or, if there are any words that the user does not know, the bot will provide more details. Pronunciation, definition of the word's meaning, word usage examples, and a dependency graph of the sentence are sent to the user, when an unknown word is selected.

<p float="left">
  <img src="https://github.com/anya-bel/vocamprove/blob/main/img/def.jpg" width="100" />
  <img src="https://github.com/anya-bel/vocamprove/blob/main/img/words.jpg" width="100" /> 
  <img src="https://github.com/anya-bel/vocamprove/blob/main/img/def.jpg" width="100" />
</p>

#### User experience Evaluation:
The user experience evaluation consisted in a survey, which full results are available in the evaluation folder. Both quantitative and qualitative data is available.


## Installation

1. cd to the directory where requirements.txt is located;
2. activate your virtualenv;
3. run: `pip install -r requirements.txt` in your shell.


## Usage
N.B. The chatbot was deployed on Heroku and is therefore available without the need to run any of the code in this repository.

### Folder structure
#### 📁 chatbot

&nbsp;&nbsp;&nbsp;&nbsp;📄 _chatbot.py_ - activates the chatbot

&nbsp;&nbsp;&nbsp;&nbsp;📄 _Questions.json_ - from here, the chatbot retrieves the questions to be proposed to the user during the vocabulary test.

#### 📁 data

&nbsp;&nbsp;&nbsp;&nbsp;📁 Texts - contains all the original corpus extracts that are presented to the user sentence by sentence

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  [...]

&nbsp;&nbsp;&nbsp;&nbsp;📁 csv-files - contains all the data in the corpus above, but rearranged in three files with metadata (indexes, POS tags, ...)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  📄 _words.csv_
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  📄 _sentences.csv_
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  📄 _texts.csv_
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  📄 _labeled_texts.csv_ - texts are labeled according to the current best performing algorithm

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;📄 _dataset_setup.py_ - the script creating 3 CSV files containing all the data from the corpus, plus the metadata 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;📄 _word_info.py_ - contains the functions retrieving information from words

#### 📁 evaluation

&nbsp;&nbsp;&nbsp;&nbsp;📁 algorithm_quant_evaluation - contains all the algorithms that were used for the lexical complexity evaluation
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  [...]

&nbsp;&nbsp;&nbsp;&nbsp;📁 ue_evaluation
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  📄 _survey_results.csv_ - results (quantitative and qualitative) from the user experience survey
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  📄 _quality_score.py_ - algorithm processing the quantitative results to calculate the overall system score 

### Functions

```python
#chatbot.py

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

## References
[1] Paula Escudeiro and Nuno Escudeiro. “Evaluating Educational Games in Mobile Platforms”. In: Int. J. Mob. Learn. Organ. 7.1 (Jan. 2013), pp. 14–28. issn: 1746-725X. doi: 10.1504/IJMLO. 2013.051571. url: https://doi.org/10.1504/IJMLO.2013.051571. 

[2] Anders Johannsen, Dirk Hovy, and Anders Søgaard. “Cross-lingual syntactic variation over age and gender”. In: Proceedings of the nineteenth conference on computational natural language learning. 2015, pp. 103–112.

[3] Gerold Lehmann Hans Martin & Schneider. “BNC Dependency Bank 1.0”. In: Oksefjell, S., Ebeling, J. & Hasselgard, H. (Eds.), Aspects of corpus linguistics: compilation, annotation, analysis. Helsinki: Research Unit for Variation, Contacts, and Change in English (2012).

[4] Kristin Lemhöfer and Mirjam Broersma. “Introducing LexTALE: A quick and valid Lexical Test for Advanced Learners of English”. In: Behavior research methods 44 (June 2012), pp. 325–343. doi: https://doi.org/10.3758/s13428-011-0146-0.

[5] XIAOFEI LU. “The Relationship of Lexical Richness to the Quality of ESL Learners’ Oral Narratives”. In: The Modern Language Journal 96.2 (2012), pp. 190–208. doi: https://doi.org/10.1111/j.1540-4781.2011.01232_1.x

[6] Menglin Xia, Ekaterina Kochmar, and Ted Briscoe. “Text Readability Assessment for Second Language Learners”. In: CoRR abs/1906.07580 (2019). arXiv: 1906.07580. url: http://arxiv.org/abs/1906.07580.
