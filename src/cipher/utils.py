
import os
import re
from typing import Optional
import fnmatch
import numpy as  np
from collections import OrderedDict

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
                self.occurrence = int(occurrence)
                
                # Add the word and its occurrence count to the dictionary
                self.occurances[word] = occurrence

    def get_candidates(self, pattern, return_top_n: Optional[int] = None ):

        output = {}
        
        filtered = fnmatch.filter(self.occurances.keys(), pattern)

        for key in filtered:
            output[key] = self.occurances[key]
        
        return output


def calculate_rel_frequencies(input: dict):
    """
    input is in shape of:

    {'a' : { 'i': 1000, 'a': 3000 }
     'cgz' : {'the': 30000, ...}  
    }

    returns in shape of {'a' : { 'i': 1/4, 'a': 3/4 }
     'cgz' : {'the': 30000, ...}  

    Note: the keys will be ordered by probabilities
    """
    output = {}

    for key, value in input.items():

        sum = np.sum(list(input[key].values()))
        
        for k2, val in value.items():

            if key in output:
                output[key].update({k2: val / sum})
            else:
                output[key] = {k2: val / sum}


            output[key] = {k: v for k, v in sorted(output[key].items(), key=lambda item: item[1], reverse=True)}


    return output


vocab = Vocabulary('./enwiki-2023-04-13.txt')


# Tests
print(vocab.occurances.get('the'))

print(vocab.get_candidates('??'))

a = {'a' : { 'i': 1000, 'a': 3000 },
     'cgz' : {'the': 10, 'ahh' : 1} 
    }

print(calculate_rel_frequencies(a))

