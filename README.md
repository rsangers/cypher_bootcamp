Steps:
- We receive an encrypted sentence
- Generate a mapping of possible words for each word in the encrypted message
- For each mapping, order it based on their probability, based on the word frequency file `enwiki-2023-04-13.txt`

Example:
- Unencrypted message: I ate it
- Encrypted: a cgz ag
- Mapping: {a: {'A', 'I'}, cgz: {the, ate, and, ...}, ag: {it, at, ad}}
- Get frequencies: {a: {'A': 1000, 'I': 2000}, cgz: {the: 10000, ate: 100, and: 1000, ...}, ag: {....}}
- Relative probabilities: {a: {'A': 1/3, 'I': 2/3}, cgz: {the: 10000/11100, ate: 100/11100, and: 1000/11100, ...}, ag: {....}}
- Chose word mapping with highest probability: cgz -> the
- Create new mappings: {a: {'A', 'I'}, ag: {uh, ah}}
- Get frequencies: {a: {'A': 1000, 'I': 2000}, ag: {uh:20, ah: 10}}
- Relative probabilities: {a: {'A': 1/3, 'I': 2/3}, ag: {uh: 2/3, ah: 1/3}}
- Chose word mapping with highest probability: a -> I
- Conflict: ih is not present in possible vocabulary: {uh, ah}
- Roll back to previous fixation (a -> I), change mapping because it is not possible: a: {'A': 100%, 'I': 0%}
- Chose word mapping with highest probability: a -> A
- ag -> Ah
-> I the ah


List of all possible english words W
What could cgz be?
Pattern matching between words in W and ???

Lets say we fixate g -> t
What could cgz be?
Pattern matching between words in W and ?t?


# Things to fix:
Mappings should be exclusive (not multiple letters mapping to the same character)
Fix rollback


