from cipher.constants import ALPHABET
from cipher.utils import Vocabulary, apply_mapping_final, calculate_rel_frequencies, create_word_patterns_from_mapping, select_candidate, update_mapping


def solve_cipher(ciphertext: str, vocabulary: Vocabulary) -> (str, dict):
    finished = False
    previous_mappings = []
    mapping = {char: '?' for char in ALPHABET}
    impossible_mappings = []
    plaintext = ciphertext

    words = ciphertext.split()

    while True:
        regexs_per_word = create_word_patterns_from_mapping(words, mapping)

        # Check if we are finished
        finished = '?' not in ''.join(regexs_per_word.values())
        if finished:
            break

        word_possibilities = {}
        for word, regex in regexs_per_word.items():
            word_possibilities[word] = vocabulary.get_candidates(regex, return_top_n=20) # Returns all possible words for a (partly) encrypted word

        # Check if it is still possible
        # if any(len(word_possibilities.values()) == 0):
        #     impossible_mappings.append(mapping)
        #     mapping = previous_mappings.pop()
        #     continue
    

        word_possibilities_freq = calculate_rel_frequencies(word_possibilities) # Adds relative prob. of each possible word

        encrypted_word, decrypted_word = select_candidate(word_possibilities_freq) # Selects candidate based on highest relative prob.

        previous_mappings.append(mapping)
        mapping = update_mapping(encrypted_word, decrypted_word, mapping)


        words.remove(encrypted_word)

    # Fill all remaining question-marks with an unused letter
    unused_letters = [char for char in ALPHABET if char not in mapping.values()]
    for char, decrypted_char in mapping.items():
        if decrypted_char == '?':
            mapping[char] = unused_letters.pop()

    

    plaintext = apply_mapping_final(plaintext, mapping)

    return plaintext, mapping   


solve_cipher('a cgz ag', vocabulary=Vocabulary('./enwiki-2023-04-13.txt'))