# Importing necessary libraries
from msilib.schema import Error
import nltk
import numpy as np
import pandas as pd
from HashTable import PriorityHashQueue


def filterWords(word_list, banned_letters, misplaced_letters):
    # This function has four parameters: "word_list" as the complete word set, "banned_letters" as the forbidden letters,
    # "baseline_answer" as the array containing the regex of the final answer, and "misplaced_letters" as the array that contains letters that are correct but misplaced.
    # Priority list:
    # 1. Words that has at least one banned letters will be removed
    # 2. Words that match the baseline answer (in regex) will be put on top of the list
    # 3. Words that has the misplaced letters will be put on the middle of the list
    # 4. Other words will be put on the bottom of the list
    wordHashList = PriorityHashQueue()
    try:
        for i in range(word_list.returnLength()):
            word = word_list.dequeue(0).get_word()
            isBanned = False
            matching_letters = 0  # Contains the number of misplaced letters in the word
            for letter in banned_letters:
                if letter in word:
                    isBanned = True
                    break
            if not isBanned:
                for letter in misplaced_letters:
                    if letter in word:
                        matching_letters += 1
                wordHashList.enqueue(word, matching_letters)
    except Exception as e:
        print(repr(e))
    return wordHashList


def hasUpperCase(word):
    # This function takes a list of words and returns a list of words that contain at least one uppercase letter
    for i in word:
        if i.isupper():
            return True
    return False


# Using heuristics, there are nine words in the English dictionary that has the most vowels
# "adieu", "audio", "auloi", "aurei", "louie", "miaou", "ouija", "ourie", "uraei"
first_words = ["adieu", "audio", "auloi", "aurei",
               "louie", "miaou", "ouija", "ourie", "uraei"]

# Importing the list of english words and limit the length of the words to five (as in Wordle)
# All words here is assumed to have a meaning and is a valid answer to a wordle (lowercase).
raw_english_words = nltk.corpus.words.words()
# sample_words = ["bruhs", "boing", "adieu", "meows", "blood",
#                 "tiger", "pussy", "louie", "miaou", "ouija", "ourie", "uraei"]
print(len(raw_english_words))
# TODO: NANTI HAPUS
# raw_english_words = raw_english_words[:100]
wordHashList = PriorityHashQueue()
for word in raw_english_words:
    if len(word) == 5 and not hasUpperCase(word):
        wordHashList.enqueue(word, 0)
print(wordHashList.returnLength())

# Retrieve a random word from the list of english words as the answer
answer = wordHashList.returnRandomValue().get_word()
print("The answer is {}".format(answer))
answer_arr = list(answer)

# Create array for baseline answers as regex and for misplaced but correct letters
baseline_answers = ['.'] * 5  # This serves as the final answer
# This serves as a temporary list to store the correct letters that are misplaced
misplaced_letters = []

# Create array to safe the letters that are not in the answer
banned_letters = []

# Main program
hasFoundAnswer = False
num_iterations = 1
while not hasFoundAnswer:
    # If the loop starts at zero or baseline_answers are all '.' (wildcards), then the try words from the first_words list
    if num_iterations == 0:
        attempt = first_words.pop(0)
    else:
        # If the loop starts at one or more than baseline_answers are not all '.' (wildcards), then the try words from the wordHashList list
        attempt = wordHashList.dequeue(0).get_word()
    attempt_arr = list(attempt)
    for i in range(5):  # 5 is the length of words in the answer (default)
        if attempt_arr[i] == answer_arr[i]:
            # Replace the '.' with the correct letter
            baseline_answers[i] = attempt_arr[i]
        elif attempt_arr[i] in answer and attempt_arr[i] not in misplaced_letters:
            misplaced_letters.append(attempt_arr[i])
        elif attempt_arr[i] not in banned_letters and attempt_arr[i] not in answer:
            banned_letters.append(attempt_arr[i])
    # If the baseline_answers are all not '.', then the loop is over
    if all(x != '.' for x in baseline_answers):
        hasFoundAnswer = True
        print("\nThe word is {} and the number of iterations are {}".format(
            attempt, num_iterations))
    else:
        # Refresh the wordHashList list
        wordHashList = filterWords(
            wordHashList, banned_letters, misplaced_letters)
        print("\nCurrent state:")
        print("Attempt word: {}".format(attempt))
        print("Number of iterations: {}".format(num_iterations))
        print("Baseline answer: {}".format(''.join(baseline_answers)))
        print("Misplaced letters: {}".format(''.join(misplaced_letters)))
        print("Banned letters: {}".format(''.join(banned_letters)))
        print("Current length of wordHashList: {}".format(
            wordHashList.returnLength()))
        num_iterations += 1
