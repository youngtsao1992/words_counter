#!/usr/bin/env python

import argparse
from word_counter.counter import WordCounter
from filetype_convert.doc2txt import FileTypeConvert


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Word counting program, counts frequency of words in a file.')
    parser.add_argument("file_path")
    parser.add_argument("-w","--word", help="calculate counter of given word", type = str)
    parser.add_argument("-n","--num", help="top number to generate", type = int, default = 10)
    
    args = parser.parse_args()
    file_path = args.file_path

    txt_file = FileTypeConvert(file_path)
    txt_file.convertDocxToText()

    wc = WordCounter(txt_file.textFilename)

    if args.word != None:
        wc.show_counter(args.word)

    if args.num > 0:
        wc.count_words(args.num)
        print("=========================")
        print("   Top " + str(args.num) +"    Words:")
        print("=========================")
        wc.display_top()
        print("Total Words: {}".format(wc.total_words))