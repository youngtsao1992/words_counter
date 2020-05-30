Easy steps to use:
1. install python3.8
2. install the requirements, using command: pip install -r requirements.txt
3. install nltk related packages
4. install words_counter\installer\Output\word-counter.exe
5. run program. (For example, double click the shortcut on desktop, or click start.bat)

usage: word_counter.py [-h] [-w WORD] [-n NUM] file_path

Example:
1. python word_counter.py C:\Users\yangcao\Desktop\word-counter\samples\sample.doc

2. Count the given word "TANGTANG" in file sample.doc:
python word_counter.py C:\Users\yangcao\Desktop\word-counter\samples\sample.doc -w TANGTANG

Note:
1. v2 use NLTK to calcute the words, refer to https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html for the TAG info.
2. Need to install wordnet, averaged_perceptron_tagger and punkt packages.
       >>> import nltk
       >>> nltk.download('xxx')
