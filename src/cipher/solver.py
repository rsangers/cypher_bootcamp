import re
from cipher.constants import ALPHABET
from cipher.utils import Vocabulary, apply_mapping_final, apply_rollback, calculate_rel_frequencies, create_word_patterns_from_mapping, remove_decrypted_words, select_candidate, update_mapping


def solve_cipher(ciphertext: str, vocabulary: Vocabulary) -> (str, dict):
    ciphertext = ciphertext.lower()
    finished = False
    rollback = False
    mapping = {char: '?' for char in ALPHABET}
    mapping['\''] = '\''
    mapping['-'] = '-'
    impossible_mappings = []
    ciphertext_no_punctuation = re.sub('[^A-Za-z \-\']+', '', ciphertext) # Note: this also removes special characters
    words = ciphertext_no_punctuation.split()

    history = {
        "mappings": [mapping],
        "words": [words],
        "word_possibilities": []
    }

    while True:
        regex_per_word = create_word_patterns_from_mapping(words, mapping)
        
        # Generate word possibilities for each (partly) decrypted word
        word_possibilities  = vocabulary.get_candidates(regex_per_word, mapping, return_top_n=20)

        # Check if it is still possible
        for word, word_possibility in word_possibilities.items():
            if len(word_possibility) == 0:
                
                print(f"No possible solutions anymore for word {word}, rollback")
                rollback = True
                break
        if rollback:
            impossible_mappings, mapping, words, history = apply_rollback(
                impossible_mappings,
                mapping,
                history
            )
            rollback = False
            continue
        
        word_possibilities, words = remove_decrypted_words(regex_per_word, word_possibilities, words)
        history['words'].append(words)
        history['word_possibilities'].append(word_possibilities)

        # Check if we are finished
        finished = len(word_possibilities) == 0
        if finished:
            break

        word_possibilities_freq = calculate_rel_frequencies(word_possibilities) # Adds relative prob. of each possible word

        # Select candidate that does not result in impossible mapping if possible
        encrypted_word, decrypted_word, candidate_found = select_candidate(word_possibilities_freq, impossible_mappings, mapping) # Selects candidate based on highest relative prob.

        if not candidate_found:
            impossible_mappings, mapping, words, history = apply_rollback(
                impossible_mappings,
                mapping,
                history
            )
            continue
    
        print(f"Selected new fixation: {encrypted_word} -> {decrypted_word} (p={round(word_possibilities_freq[encrypted_word][decrypted_word],2)})")

        history['mappings'].append(mapping)
        mapping = update_mapping(encrypted_word, decrypted_word, mapping)

        print(f"New mapping: {mapping}")

    # Fill all remaining question-marks with an unused letter
    unused_letters = [char for char in ALPHABET if char not in mapping.values()]
    for char, decrypted_char in mapping.items():
        if decrypted_char == '?':
            mapping[char] = unused_letters.pop()

    solution = ""
    for char in ciphertext:
        if char in mapping.keys():
            solution += mapping[char]
        else:
            solution += char

    return solution, mapping   