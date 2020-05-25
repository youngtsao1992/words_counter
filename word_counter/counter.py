#!/usr/bin/env python


def cleanse_word(word):
    # find regex for word
    return word.lower().strip(',').strip('.').strip('\'').strip('"').strip('*').strip('?').strip('!').strip(';').strip(':')


class WordCounter(object):
    """ Word counting object, counts total words and top 10 occurring words """

    def __init__(self, file_path):
        self.top = list()
        self.total_words = 0
        self.file_path = file_path
        self.word_freq = dict()
        self.word_counter = dict()

    def count_words(self, num):
        with open(self.file_path, 'r') as f:
            for word in f.read().split():
                word = cleanse_word(word)
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

    def show_counter(self, word_in):
        with open(self.file_path, 'r') as f:
            for word in f.read().split():
                word = cleanse_word(word)
                self.word_counter.setdefault(word_in, 0)
                if word == word_in:
                    self.word_counter[word_in] += 1
        print(word_in, self.word_counter[word_in])

