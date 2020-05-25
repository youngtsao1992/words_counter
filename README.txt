Install running environment:
1. install python3.8
2. install the requirements, using command: pip install -r requirements.txt


usage: word_counter.py [-h] [-w WORD] [-n NUM] file_path

Example:
1. Count the top 10 frequency words in file sample2.doc:
python word_counter.py C:\Users\yangcao\Desktop\word-counter\samples\sample2.doc -n 10

2. Count the specific word "TANGTANG" in file sample2.doc:
python word_counter.py C:\Users\yangcao\Desktop\word-counter\samples\sample2.doc -w TANGTANG