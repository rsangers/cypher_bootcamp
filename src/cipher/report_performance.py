import re
from cipher.constants import ALPHABET
from cipher.solver import solve_cipher
from cipher.utils import Vocabulary

vocab = Vocabulary('./enwiki-2023-04-13.txt', occurrence_cutoff=10000)

encrypted_text = 'rddutdj dau ukd cpju gkdv ukdh aod taoqad. jpcd rddutd taoqad dau ukd peujmsd px ltavuj; jpcd dau mvjmsd ltavuj. jpcd rddutd taoqad aod lodsaupoj, gkmzk cdavj ukdh kevu xpo pukdo mvjdzuj up dau. pukdo rddutd taoqad dau sdas ukmvwj, jezk aj sdas ltavuj avs sdas avmcatj. mu mvxtedvzdj jeoxazd dvdowh, ztpesj, lodzmlmuaumpv, khsoptpwh, avs ukd gah rpuk amo avs gaudo cpqd arpeu mv ukd aucpjlkdod avs pzdavj. ukd zohpjlkdod mj mclpouavu up evsdojuavsmvw kpg ukd ztmcaud px daouk gpofj avs kpg mu axxdzuj wtprat ztmcaud.'
decrypted_text = 'beetles eat the most when they are larvae. some beetle larvae eat the outside of plants; some eat inside plants. some beetle larvae are predators, which means they hunt for other insects to eat. other beetle larvae eat dead things, such as dead plants and dead animals. it influences surface energy, clouds, precipitation, hydrology, and the way both air and water move about in the atmosphere and oceans. the cryosphere is important to understanding how the climate of earth works and how it affects global climate.'

if __name__ == "__main__":
    decrypted_text_no_punctuation = "".join(re.sub(r'[^\w\s]', '', decrypted_text).split())
    encrypted_text_no_punctuation = "".join(re.sub(r'[^\w\s]', '', encrypted_text).split())

    true_mapping = {}
    for idx, char in enumerate(encrypted_text_no_punctuation):
        true_mapping[char] = decrypted_text_no_punctuation[idx]
    true_mapping = dict(sorted(true_mapping.items()))
        
    solution, mapping = solve_cipher(encrypted_text, vocab)

    n_correct = 0
    for key, value in true_mapping.items():
        if value == mapping[key]:
            n_correct += 1
    
    print(f"Accuracy: {n_correct/len(true_mapping.keys())*100}%")
    print(mapping)
    print(true_mapping)
