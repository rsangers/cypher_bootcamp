
import os
import random
import re
from typing import Optional
import fnmatch
import numpy as  np
from collections import OrderedDict

from cipher.constants import ALPHABET

class Vocabulary:

    def __init__(self, file_name, occurrence_cutoff = -1) -> None:
        self.file_name = file_name
        self.occurrence_cutoff = occurrence_cutoff
        self.occurances = {}
        self.read_file()

    def read_file(self):
        print('path ', os.getcwd())
        
        # Open the text file for reading
        with open(self.file_name, 'r') as file:
            # Iterate through each line in the file
            for line in file:
                # Split each line into word and occurrence using whitespace as the separator
                word, occurrence = line.strip().split()

                if int(occurrence) < self.occurrence_cutoff:
                    return
                
                # Convert the occurrence count from string to an integer
                # self.occurrence = int(occurrence)
                
                # Add the word and its occurrence count to the dictionary
                self.occurances[word] = int(occurrence)

    def get_candidates(self, regexs_per_word, mapping, return_top_n=20):

        characters_to_exclude = [value for value in mapping.values() if value != '?']

        word_possibilities = {}
        for word, regex in regexs_per_word.items():
            word_possibilities[word] = self.get_candidates_per_word(regex, characters_to_exclude, return_top_n)

        return word_possibilities

    def get_candidates_per_word(self, pattern, characters_to_exclude, return_top_n: Optional[int] = 20 ):

        # get the characters without the constants
        possible_chars = "".join([char for char in ALPHABET if char not in characters_to_exclude])

        # replace the '?' with the possible characters based on exclusions 
        pattern = pattern.replace('?',f'[{possible_chars}]')

        output = {}
        
        counter = 0

        filtered = fnmatch.filter(self.occurances.keys(), pattern)

        for key in filtered:
            if counter < return_top_n:
                output[key] = self.occurances[key]
                counter+=1
            else:
                break
        
        return output


def calculate_rel_frequencies(input: dict):
    """
    input is in shape of:

    {'a' : { 'i': 1000, 'a': 3000 }
     'cgz' : {'the': 30000, ...}  
    }

    returns in shape of {'a' : {  'a': 3/4, 'i': 1/4, }
     'cgz' : {'the': 0.77, ...}  

    Note: the keys will be ordered by probabilities
    """
    output = {}

    for key, value in input.items():

        sum = np.sum(np.array(list(input[key].values())))
        
        for k2, val in value.items():

            if key in output:
                output[key].update({k2: val / sum})
            else:
                output[key] = {k2: val / sum}

            output[key] = {k: v for k, v in sorted(output[key].items(), key=lambda item: item[1], reverse=True)}


    return output


# vocab = Vocabulary('./enwiki-2023-04-13.txt')


# # Tests
# print(vocab.occurances.get('the'))

# print(vocab.get_candidates('??'))

# a = {'a' : { 'i': 1000, 'a': 3000 },
#      'cgz' : {'the': 10, 'ahh' : 1} 
#     }

# print(calculate_rel_frequencies(a))

def select_candidate(word_possibilities_freq: dict, impossible_mappings, mapping) -> (str, str):
    valid_mapping = False
    while not valid_mapping:

        decrypted_word = ""
        encrypted_word = ""
        value = -1
        for word, word_possibilities in word_possibilities_freq.items():
            if len(word_possibilities.values()) == 0:
                print("Rollback another step")
                return "", "", False
            if list(word_possibilities.values())[0] > value:
                value = list(word_possibilities.values())[0]
                decrypted_word = list(word_possibilities.keys())[0]
                encrypted_word = word
        
        new_mapping = update_mapping(encrypted_word, decrypted_word, mapping)

        valid_mapping = new_mapping not in impossible_mappings

        if not valid_mapping:
            print("Found impossible mapping")
            del word_possibilities_freq[encrypted_word][decrypted_word]

    return encrypted_word, decrypted_word, True

def create_word_patterns_from_mapping(words: list, mapping: dict) -> dict:
    regexs_per_word = {}
    for word in words:
        regexs_per_word[word] = ''.join([mapping[char] for char in word])

    return regexs_per_word

def update_mapping(word: str, decrypted_word: str, mapping: dict) -> dict:
    new_mapping = mapping.copy()
    for idx in range(len(word)):
        new_mapping[word[idx]] = decrypted_word[idx]

    return new_mapping

def apply_mapping_final(plaintext, mapping):
    out = ''
    
    for word in plaintext.split():
        for letter in word:
            out += mapping[letter]

        out += ' '
    out = out[:-1]

    return out

def generate_cipher():
    shuffled_alphabet = ALPHABET.copy()
    random.shuffle(shuffled_alphabet)

    cipher = {ALPHABET[i]: shuffled_alphabet[i] for i in range(len(ALPHABET))}
    return cipher

def apply_rollback(impossible_mappings, mapping, history):
    impossible_mappings.append(mapping)
    mapping = history['mappings'].pop()
    words = history['words'].pop()

    return impossible_mappings, mapping, words, history

def remove_decrypted_words(regexs_per_word, word_possibilities, words):
    words_to_remove = []
    for word, regex in regexs_per_word.items():
        if '?' not in regex:
            words_to_remove.append(word)

    for word in words_to_remove:
        word_possibilities.pop(word)
        words = [w for w in words if w != word]

    return word_possibilities, words