import regex as re
import numpy as np

first_words = ["adieu", "audio", "auloi", "aurei",
               "louie", "miaou", "ouija", "ourie", "uraei"]

text = "The quick brown fox jumps over the lazy dog"
regex_template = ['.', '.', '.', 'i', 'o']
for word in first_words:
    if re.search(''.join(regex_template), word):
        print(word)
