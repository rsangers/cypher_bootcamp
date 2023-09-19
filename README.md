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


# Issues
- The solver continues until it has found a perfect solution, and it therefore not robust to words that do not appear in its vocabulary. To fix this, a module should be implemented that enables some sort of tolerance in checking its mapping, e.g. allow for at most one 'unknown' word in the final solution.
- To increase performance: implement a function to reuse the word-possibilities dictionary, instead of repeatedly mapping the complete vocabulary against the current regex.

# Benchmarking
The accuracy and runtime of this solver strongly depend on a parameter, which should be set manually: `occurrence_cutoff`. This parameter determines the minimum amount of times a word should appear on wikipedia to include it in the vocabulary. It is recommended to start with a relatively high value for this parameter (e.g. 200), and decrease this value if the solver takes longer than a few minutes to come to a solution.

## Examples
### Occurrence cutoff = 200

beetles eat the most when they are larvae. some beetle larvae eat the outside of plants; some eat inside plants. some beetle larvae are predators, which means they hunt for other insects to eat. other beetle larvae eat dead things, such as dead plants and dead animals. it influences surface energy, clouds, precipitation, hydrology, and the way both air and water move about in the atmosphere and oceans. the cryosphere is important to understanding how the climate of earth works and how it affects global climate.

Accuracy: 100.0%

Time taken: 15.17 seconds

although they frequently live in dryland forests, tapirs with access to rivers spend a good deal of time in and under water, feeding on soft vegetation, taking refuge from predators, and cooling off during hot periods. tapirs near a water source will swim, sink to the bottom, and walk along the riverbed to feed, and have been known to submerge themselves to allow small fish to pick parasites off their bulky bodies. along with freshwater lounging, tapirs often wallow in mud pits, which helps to keep them cool and free of insects.

Accuracy: 100.0%

Time taken: 18.9 seconds

### Occurrence cutoff = 10
in the wild, the tapir's diet consists of fruit, berries, and leaves, particularly young, tender vegetation. tapirs will spend many of their waking hours foraging along well-worn trails, snouts to the ground in search of food. baird's tapirs have been observed to eat around 40 kg (85 lb) of vegetation in one day. tapirs are largely nocturnal and crepuscular, although the smaller mountain tapir of the andes is generally more active during the day than its congeners. they have monocular vision.

Accuracy: 100.0%

Time taken: 97.12 seconds


