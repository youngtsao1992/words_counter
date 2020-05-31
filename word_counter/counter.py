#!/usr/bin/env python
import os
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

csv_header = ['WORD', 'COUNT', 'TAG']

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

    def __init__(self, file_path):
        self.total_words = 0
        self.file_path = file_path

    def counter_words_v2(self, words_in, od):
        if od[-1] == '\\' or od[-1] == '/':
            od = od[:-1]
        with open(self.file_path, 'r', encoding='utf-8') as f:
            w_clean = merge(cleanse_word(f.read()))
            self.total_words = len(w_clean)
            self.save_all_to_csv(w_clean, od)

            if words_in != "":
                w_select = []
                w_no_find = []
                words_list = words_in.split()
                for w in w_clean:
                    if w in words_list:
                        w_select.append(w)
                for w in words_list:
                    if not w in w_select:
                        w_no_find.append(w)
                self.save_to_csv(w_select, w_no_find, od)

    def save_to_csv(self, w_select, w_no_find, od):
        file_name = os.getcwd() + "\words_frequency_given.csv"
        if os.path.isdir(od) == True:
            file_name = od + "\words_frequency_given.csv"
        words = collections.Counter(w_select)
        print("Save given words counter to " + file_name)
        with open(file_name, "w", newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(["Hello, Miss Tang :)"])
            f_csv.writerow(["  This is the sorted words of file given. And for the TAG definition, please refer to https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html"])
            f_csv.writerow([]) # empty line
            f_csv.writerow(['TOTAL', self.total_words])
            f_csv.writerow([]) # empty line
            f_csv.writerow(csv_header)
            f_csv.writerows(append_ext(words.most_common()))
            for word in w_no_find:
                f_csv.writerow([word, 0])

    def save_all_to_csv(self, w_clean, od):
        file_name = os.getcwd() + "\words_frequency_all.csv"
        if os.path.isdir(od):
            file_name = od + "\words_frequency_all.csv"
        words = collections.Counter(w_clean)
        print("Save given words counter to " + file_name)
        with open(file_name, "w", newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(["Hello, Miss Tang :)"])
            f_csv.writerow(["  This is the whole words of file given. And for the TAG definition, please refer to https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html"])
            f_csv.writerow([]) # empty line
            f_csv.writerow(['TOTAL', self.total_words])
            f_csv.writerow([]) # empty line
            f_csv.writerow(csv_header)
            f_csv.writerows(append_ext(words.most_common()))

