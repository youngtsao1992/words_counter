#!/usr/bin/env python

import argparse
import os
from word_counter.counter import WordCounter
from filetype_convert.doc2txt import FileTypeConvert


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Word counting program, counts frequency of words in a file.')
    parser.add_argument("file_path")
    parser.add_argument("-w","--words", help="calculate counter of given words", type = str)
    parser.add_argument("-c","--clean", help="clean temp files", type = bool, default = True)
    
    args = parser.parse_args()
    if os.path.isabs(args.file_path):
        file_path = args.file_path
    else:
        file_path = os.path.abspath(args.file_path)

    txt_file = FileTypeConvert(file_path)
    txt_file.convertDocxToText()

    wc = WordCounter(txt_file.textFilename)

    if args.words != None:
        wc.counter_words_v2(args.words)

    fileExtension = file_path.split(".")[-1]
    if args.clean == True and fileExtension != "txt":
        os.remove(txt_file.textFilename)
