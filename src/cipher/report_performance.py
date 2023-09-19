import re
from cipher.constants import ALPHABET
from cipher.solver import solve_cipher
from cipher.utils import Vocabulary, create_word_patterns_from_mapping, generate_cipher
import time

vocab = Vocabulary('./enwiki-2023-04-13.txt', occurrence_cutoff=10)

# encrypted_text = 'rddutdj dau ukd cpju gkdv ukdh aod taoqad. jpcd rddutd taoqad dau ukd peujmsd px ltavuj; jpcd dau mvjmsd ltavuj. jpcd rddutd taoqad aod lodsaupoj, gkmzk cdavj ukdh kevu xpo pukdo mvjdzuj up dau. pukdo rddutd taoqad dau sdas ukmvwj, jezk aj sdas ltavuj avs sdas avmcatj. mu mvxtedvzdj jeoxazd dvdowh, ztpesj, lodzmlmuaumpv, khsoptpwh, avs ukd gah rpuk amo avs gaudo cpqd arpeu mv ukd aucpjlkdod avs pzdavj. ukd zohpjlkdod mj mclpouavu up evsdojuavsmvw kpg ukd ztmcaud px daouk gpofj avs kpg mu axxdzuj wtprat ztmcaud.'
# decrypted_text = 'beetles eat the most when they are larvae. some beetle larvae eat the outside of plants; some eat inside plants. some beetle larvae are predators, which means they hunt for other insects to eat. other beetle larvae eat dead things, such as dead plants and dead animals. it influences surface energy, clouds, precipitation, hydrology, and the way both air and water move about in the atmosphere and oceans. the cryosphere is important to understanding how the climate of earth works and how it affects global climate.'

#decrypted_text = 'Although they frequently live in dryland forests, tapirs with access to rivers spend a good deal of time in and under water, feeding on soft vegetation, taking refuge from predators, and cooling off during hot periods. Tapirs near a water source will swim, sink to the bottom, and walk along the riverbed to feed, and have been known to submerge themselves to allow small fish to pick parasites off their bulky bodies. Along with freshwater lounging, tapirs often wallow in mud pits, which helps to keep them cool and free of insects.'.lower()
decrypted_text = "In the wild, the tapir's diet consists of fruit, berries, and leaves, particularly young, tender vegetation. Tapirs will spend many of their waking hours foraging along well-worn trails, snouts to the ground in search of food. Baird's tapirs have been observed to eat around 40 kg (85 lb) of vegetation in one day. Tapirs are largely nocturnal and crepuscular, although the smaller mountain tapir of the Andes is generally more active during the day than its congeners. They have monocular vision.".lower()
cipher = generate_cipher()
encrypted_text = ""
for char in decrypted_text:
    if char in cipher.keys():
        encrypted_text += cipher[char]
    else:
        encrypted_text += char

if __name__ == "__main__":
    decrypted_text_no_punctuation = re.sub('[^A-Za-z]+', '', decrypted_text)
    encrypted_text_no_punctuation = re.sub('[^A-Za-z]+', '', encrypted_text)

    true_mapping = {}
    for idx, char in enumerate(encrypted_text_no_punctuation):
        true_mapping[char] = decrypted_text_no_punctuation[idx]
    true_mapping = dict(sorted(true_mapping.items()))
    
    print(encrypted_text)
    start = time.time()
    solution, mapping = solve_cipher(encrypted_text, vocab)
    end = time.time()

    n_correct = 0
    for key, value in true_mapping.items():
        if value == mapping[key]:
            n_correct += 1
    
    print(solution)
    print(f"Accuracy: {n_correct/len(true_mapping.keys())*100}%")
    print(f"Time taken: {round(end-start, 2)} seconds")
    print(f"Mapping: {mapping}")
    print(f"True mapping: {true_mapping}")
