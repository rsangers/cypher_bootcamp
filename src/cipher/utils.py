
import os
import random
import re
from typing import Optional
import fnmatch
import numpy as  np
from collections import OrderedDict


from constants import ALPHABET

class Vocabulary:

    def __init__(self, file_name) -> None:
        self.file_name = file_name
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
                
                # Convert the occurrence count from string to an integer
                # self.occurrence = int(occurrence)
                
                # Add the word and its occurrence count to the dictionary
                self.occurances[word] = int(occurrence)

    def get_candidates(self, pattern, return_top_n: Optional[int] = 20 ):


        # get the characters that are in the pattern already
        characters_to_exclude = [char for char in pattern if char != '?']

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


vocab = Vocabulary('./enwiki-2023-04-13.txt')

# def get_alphabet_with_exclusions(exclusions):
#     from constants import ALPHABET


print( vocab.get_candidates('c?e??') )


# # Tests
# print(vocab.occurances.get('the'))

# print(vocab.get_candidates('??'))

# a = {'a' : { 'i': 1000, 'a': 3000 },
#      'cgz' : {'the': 10, 'ahh' : 1} 
#     }

# print(calculate_rel_frequencies(a))

def select_candidate(word_possibilities_freq: dict) -> (str, str):
    decrypted_word = ""
    encrypted_word = ""
    value = -1
    for word, word_possibilities in word_possibilities_freq.items():
        if list(word_possibilities.values())[0] > value:
            value = list(word_possibilities.values())[0]
            decrypted_word = list(word_possibilities.keys())[0]
            encrypted_word = word

    return encrypted_word, decrypted_word


a = {'a' : { 'i': 3000, 'z': 1000 },
     'cgz' : {'the': 10, 'ahh' : 1} 
    }

print(select_candidate(a))


def create_word_patterns_from_mapping(words: list, mapping: dict) -> dict:
    regexs_per_word = {}
    for word in words:
        regexs_per_word[word] = ''.join([mapping[char] for char in word])

    return regexs_per_word

def update_mapping(word: str, decrypted_word: str, mapping: dict) -> dict:
    for idx in range(len(word)):
        mapping[word[idx]] = decrypted_word[idx]

    return mapping

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