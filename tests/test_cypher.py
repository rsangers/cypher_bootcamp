import cipher
from cipher.constants import ALPHABET
from cipher.utils import calculate_rel_frequencies, generate_cipher, create_word_patterns_from_mapping
import pytest


@pytest.fixture
def random_cipher():
    return generate_cipher()

@pytest.fixture
def deterministic_cipher():
    # Cipher with reversed mapping based on position in the alphabet, e.g. a -> z
    return {ALPHABET[i]: ALPHABET[-i -1] for i in range(len(ALPHABET))}

@pytest.fixture
def decrypted_words():
    return "I ate it".lower().split()

@pytest.fixture
def word_possibilities():
    return {
        'a' : { 'i': 1000, 'a': 3000 },
        'cgz' : {'the': 30000, 'and': 20000}  
    }

@pytest.fixture
def word_possibilities_freq():
    return {
        'a' : { 'a': 3/4, 'i': 1/4, },
        'cgz' : {'the': 0.6, 'and': 0.4}
    }  

def test_generate_cipher(random_cipher):

    assert all(char in random_cipher.keys() and char in random_cipher.values() for char in ALPHABET)
    assert any(random_cipher[char] != char for char in ALPHABET) # This test fails once every 26! (factorial) times

def test_create_word_patterns_from_mapping(random_cipher, deterministic_cipher, decrypted_words):

    reverse_random_cipher = {value: key for key, value in random_cipher.items()}
    encrypted_words_true = ['r', 'zgv', 'rg']
    empty_mapping = {char: '?' for char in ALPHABET}

    # Assert if applying empty mapping returns only question marks
    encrypted_words = list(create_word_patterns_from_mapping(decrypted_words, empty_mapping).values())
    assert all(encrypted_words[i] == '?'*len(encrypted_words[i]) for i in range(len(decrypted_words)))
    
    # Assert if at least one word has changed by applying cipher
    encrypted_words = list(create_word_patterns_from_mapping(decrypted_words, reverse_random_cipher).values())
    assert any(encrypted_words[i] != decrypted_words[i] for i in range(len(decrypted_words)))

    # Assert if applying cipher and reverse cipher returns the same words
    decrypted_encrypted_words = list(create_word_patterns_from_mapping(encrypted_words, random_cipher).values())
    assert all(decrypted_encrypted_words[i] == decrypted_words[i] for i in range(len(decrypted_words)))

    # Assert if deterministic cipher behaves as expected
    encrypted_words = list(create_word_patterns_from_mapping(decrypted_words, deterministic_cipher).values())
    assert all(encrypted_words[i] == encrypted_words_true[i] for i in range(len(decrypted_words))), deterministic_cipher

def test_calculate_rel_frequencies(word_possibilities, word_possibilities_freq):

    assert word_possibilities_freq == calculate_rel_frequencies(word_possibilities)




# @pytest.mark.parametrize('input', [('IIII'), ('IC'), ('VVV')])
# def test_input_check(input):
#     with pytest.raises(ValueError):
#         roman.check_input(input)