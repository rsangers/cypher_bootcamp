from cipher.utils import Vocabulary

# Read once for all tests in this file
vocab = Vocabulary('./enwiki-2023-04-13.txt')

def test_get_candidates():

    pattern = 'c?e??'
    words = vocab.get_candidates(pattern, return_top_n=100).keys()
    
    assert all(len(word) == len(pattern) for word in words)

    diff_chars_at_wildcards = True
    same_characters_at_knows = True

    for word in words:

        if word[0] != 'c' or word[2] != 'e':
            same_characters_at_knows = False

        if word[1] == 'c' or word[1] == 'e' or word[3] == 'c' or word[3] == 'e' or word[4] == 'c' or word[4] == 'e':
            diff_chars_at_wildcards = False

    assert same_characters_at_knows
    assert diff_chars_at_wildcards
