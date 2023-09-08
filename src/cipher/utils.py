
import os
import re
from typing import Optional
import fnmatch

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


vocab = Vocabulary('./enwiki-2023-04-13.txt')

print(vocab.occurances.get('the'))

print(vocab.get_candidates('??'))