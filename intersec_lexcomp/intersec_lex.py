from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS as stopwords

def determ_lvl(text):
    c_vec = CountVectorizer(ngram_range=(2, 2), stop_words='english')
    ngrams = c_vec.fit_transform([text])
    vocab = c_vec.vocabulary_
    bigrams = set([x[0] for x in vocab.items()])
    unigrams = set(word_tokenize(text)) & stopwords

    a1 = [w.strip() for w in open('a1.txt').readlines()]
    a2 = [w.strip() for w in open('a2.txt').readlines()]
    b1 = [w.strip() for w in open('b1.txt').readlines()]
    b2 = [w.strip() for w in open('b2.txt').readlines()]
    c1 = [w.strip() for w in open('c1.txt').readlines()]
    c2 = [w.strip() for w in open('c2.txt').readlines()]

    lvl = {'a1': a1,
           'a2': a2,
           'b1': b1,
           'b2': b2,
           'c1': c1,
           'c2': c2}
    f_lvl  = {'a1': 0,
           'a2': 0,
           'b1': 0,
           'b2': 0,
           'c1': 0,
           'c2': 0}
    for l in lvl:
      f_lvl[l] = len(unigrams & set(lvl[l]))
      f_lvl[l] += len(bigrams & set(lvl[l]))
    return max(f_lvl, key=f_lvl.get)
