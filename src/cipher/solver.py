import re
from cipher.constants import ALPHABET
from cipher.utils import Vocabulary, apply_mapping_final, calculate_rel_frequencies, create_word_patterns_from_mapping, select_candidate, update_mapping


def solve_cipher(ciphertext: str, vocabulary: Vocabulary) -> (str, dict):
    # Change to lowercase
    ciphertext = ciphertext.lower()

    finished = False
    rollback = False
    previous_mappings = []
    mapping = {char: '?' for char in ALPHABET}
    impossible_mappings = []
    solution = ciphertext

    ciphertext_no_punctuation = re.sub(r'[^\w\s]', '', ciphertext)

    words = ciphertext_no_punctuation.split()

    while True:
        regexs_per_word = create_word_patterns_from_mapping(words, mapping)

        # Remove all decrypted words
        words_to_remove = []
        for word, regex in regexs_per_word.items():
            if '?' not in regex:
                words_to_remove.append(word)
        for word in words_to_remove:
            regexs_per_word.pop(word)
            

        # Check if we are finished
        finished = len(regexs_per_word) == 0
        if finished:
            break

        word_possibilities = {}
        for word, regex in regexs_per_word.items():
            word_possibilities[word] = vocabulary.get_candidates(regex, return_top_n=20) # Returns all possible words for a (partly) encrypted word

        # Check if it is still possible
        for word_possibility in word_possibilities.values():
            if len(word_possibility) == 0:
                print("No possible solutions anymore, rollback")
                impossible_mappings.append(mapping)
                mapping = previous_mappings[-1]
                previous_mappings.pop()
                rollback = True
                break
        if rollback:
            rollback = False
            continue
    

        word_possibilities_freq = calculate_rel_frequencies(word_possibilities) # Adds relative prob. of each possible word

        encrypted_word, decrypted_word = select_candidate(word_possibilities_freq, impossible_mappings, mapping) # Selects candidate based on highest relative prob.

        if encrypted_word == "":
            print("No possible solutions anymore, continuing with roundup")
            break
    
        print(f"Selected new fixation: {encrypted_word} -> {decrypted_word}")

        previous_mappings.append(mapping)
        print(mapping)
        mapping = update_mapping(encrypted_word, decrypted_word, mapping)

    # Fill all remaining question-marks with an unused letter
    unused_letters = [char for char in ALPHABET if char not in mapping.values()]
    for char, decrypted_char in mapping.items():
        if decrypted_char == '?':
            mapping[char] = unused_letters.pop()

    for encrypted_char, decrypted_char in mapping.items():
        solution = solution.replace(encrypted_char, decrypted_char)

    return solution, mapping   


#solve_cipher('a cgz ag', vocabulary=Vocabulary('./enwiki-2023-04-13.txt'))