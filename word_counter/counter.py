#!/usr/bin/env python
import re
import csv

def cleanse_word(word):
    # find regex for word
    return re.sub('[^a-zA-Z0-9]', ' ', word.lower())

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
            for word in cleanse_word(f.read()).split():
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
        with open(self.file_path, 'r') as f:
            for w in cleanse_word(f.read()).split():
                if w in words_list:
                    self.words_counter[w] += 1
        for word in self.words_counter:
            print(word, self.words_counter[word])
        self.save_to_csv()

    def save_to_csv(self):
        with open("words_frequency.csv", "w", newline='') as f:
            f_csv = csv.writer(f)
            for key, value in self.words_counter.items():
                f_csv.writerow([key, value])

