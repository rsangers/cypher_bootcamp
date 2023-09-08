from cipher.constants import ALPHABET


def solve_cipher(ciphertext: str) -> (str, dict):
    finished = False
    mapping = {}
    plaintext = ciphertext

    words = ciphertext.split()

    while not finished:
        regexs_per_word = create_word_patterns_from_mapping(words, mapping)

        # Check if we are finished

        word_possibilities = {}
        for word, regex in regexs_per_word.items():
            word_possibilities[word] = get_candidates(regex) # Returns all possible words for a (partly) encrypted word
            
        # Check if it is still possible
        

        word_possibilities_freq = calculate_rel_frequencies(word_possibilities) # Adds relative prob. of each possible word

        fixated_word = select_candidate(word_possibilities_freq) # Selects candidate based on highest relative prob.

        mapping = update_mapping(mapping, fixated_word)


    

    return plaintext, ciphertext