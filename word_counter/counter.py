#!/usr/bin/env python
import re
import csv
import sys,collections,nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize


# patterns that used to find or/and replace particular chars or words
# to find chars that are not a letter, a blank or a quotation
pat_letter = re.compile(r'[^a-zA-Z \']+')
# to find the 's following the pronouns. re.I is refers to ignore case
pat_is = re.compile("(it|he|she|that|this|there|here)(\'s)", re.I)
# to find the 's following the letters
pat_s = re.compile("(?<=[a-zA-Z])\'s")
# to find the ' following the words ending by s
pat_s2 = re.compile("(?<=s)\'s?")
# to find the abbreviation of not
pat_not = re.compile("(?<=[a-zA-Z])n\'t")
# to find the abbreviation of would
pat_would = re.compile("(?<=[a-zA-Z])\'d")
# to find the abbreviation of will
pat_will = re.compile("(?<=[a-zA-Z])\'ll")
# to find the abbreviation of am
pat_am = re.compile("(?<=[I|i])\'m")
# to find the abbreviation of are
pat_are = re.compile("(?<=[a-zA-Z])\'re")
# to find the abbreviation of have
pat_ve = re.compile("(?<=[a-zA-Z])\'ve")

lmtzr = WordNetLemmatizer()

def replace_abbreviations(text):
    new_text = text
    new_text = pat_letter.sub(' ', text).strip().lower()
    new_text = pat_is.sub(r"\1 is", new_text)
    new_text = pat_s.sub("", new_text)
    new_text = pat_s2.sub("", new_text)
    new_text = pat_not.sub(" not", new_text)
    new_text = pat_would.sub(" would", new_text)
    new_text = pat_will.sub(" will", new_text)
    new_text = pat_am.sub(" am", new_text)
    new_text = pat_are.sub(" are", new_text)
    new_text = pat_ve.sub(" have", new_text)
    new_text = new_text.replace('\'', ' ')
    return new_text

def cleanse_word(word):
    # find regex for word
    return replace_abbreviations(word).split()

def merge(words):
    new_words = []
    for word in words:
        if word:
            tag = nltk.pos_tag(word_tokenize(word)) # tag is like [('bigger', 'JJR')]
            pos = get_wordnet_pos(tag[0][1])
            if pos:
                lemmatized_word = lmtzr.lemmatize(word, pos)
                new_words.append(lemmatized_word)
            else:
                new_words.append(word)
    return new_words
    
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return nltk.corpus.wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return nltk.corpus.wordnet.VERB
    elif treebank_tag.startswith('N'):
        return nltk.corpus.wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return nltk.corpus.wordnet.ADV
    else:
        return ''

def append_ext(words):
    new_words = []
    for item in words:
        word, count = item
        tag = nltk.pos_tag(word_tokenize(word))[0][1] # tag is like [('bigger', 'JJR')]
        new_words.append((word, count, tag))
    return new_words

class WordCounter(object):
    """ Word counting object, counts total words and top 10 occurring words """

    def __init__(self, file_path):
        self.top = list()
        self.total_words = 0
        self.file_path = file_path
        self.word_freq = dict()
        self.words_counter = dict()

    def count_words(self, num):
        with open(self.file_path, 'r') as f:
            for word in cleanse_word(f.read()):
                self.word_freq.setdefault(word, 0)
                self.word_freq[word] += 1
                self.total_words += 1
                self._insert_to_top(word, num)

    def _insert_to_top(self, w, num):
        if self.top:
            for index, item in enumerate(self.top):
                if self.word_freq[item] <= self.word_freq[w]:
                    if w in self.top:
                        del self.top[self.top.index(w)]
                    self.top.insert(index, w)
                    del self.top[num:]
                    break
        else:
            self.top.append(w)

    def display_top(self):
        for word in self.top:
            print(word, self.word_freq[word])

    def counter_words(self, words_in):
        words_list = words_in.split()
        for word in words_list:
            self.words_counter.setdefault(word, 0)
        with open(self.file_path, 'r', encoding='utf-8') as f:
            for w in cleanse_word(f.read()):
                if w in words_list:
                    self.words_counter[w] += 1
        for word in self.words_counter:
            print(word, self.words_counter[word])
        self.save_to_csv()

    def counter_words_v2(self, words_in):
        words_list = words_in.split()
        for word in words_list:
            self.words_counter.setdefault(word, 0)
        with open(self.file_path, 'r', encoding='utf-8') as f:
            w_clean = merge(cleanse_word(f.read()))
            for w in w_clean:
                if w in words_list:
                    self.words_counter[w] += 1
        for word in self.words_counter:
            print(word, self.words_counter[word])
        self.save_to_csv()
        self.save_all_to_csv(w_clean)

    def save_to_csv(self):
        with open("words_frequency.csv", "w", newline='') as f:
            f_csv = csv.writer(f)
            for key, value in self.words_counter.items():
                f_csv.writerow([key, value])

    def save_all_to_csv(self, w_clean):
        words = collections.Counter(w_clean)
        with open("words_frequency_all.csv", "w", newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerows(append_ext(words.most_common()))

