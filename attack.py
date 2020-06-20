#!/usr/bin/env python3

import pprint as pp
import random
import enchant

ciphertext      = 'OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR'
known_cleartext = 'OBKRUOXOGHULBSOLIFBBWFLRVNORTHEASTOTWTQSJQSSEKZZWATJKLUDIAWINFBBERLINCLOCKWGDKZXTJCDIGKUHUAUEKCAR'

alphabet = set(ciphertext)
alphabet_len = len(alphabet)

# Populate known cipher characters to cleartext characters and used cleartext characters
known_ciphered_mapping = {}
used = set()
for i in range(len(ciphertext)):
    if ciphertext[i] != known_cleartext[i]:
        if ciphertext[i] not in known_ciphered_mapping:
            known_ciphered_mapping[ciphertext[i]] = set()
        known_ciphered_mapping[ciphertext[i]].add(known_cleartext[i])
        used.add(known_cleartext[i])

unknown_alphabet = alphabet.copy()
for letter in known_ciphered_mapping.keys():
    unknown_alphabet.remove(letter)

unused = alphabet
for letter in used:
    unused.remove(letter)

# Used to count occurences in known values.
# Converted to set of letters that haven't been used twice
cleartext_mapping_count = {
    'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0,
    'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0,
    'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0,
    'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0,
    'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0,
    'Z': 0,
}

for v in known_ciphered_mapping.values():
    for known in v:
        cleartext_mapping_count[known] += 1

available = {k: v for k, v in cleartext_mapping_count.items() if v < 2}.keys()
available_cleartext_alphabet = set(available)


def substr_gte4(s):
    """ Get substring greater than or equal to 4 characters long
    :param s:
    :return:
    """
    length = len(s)
    return [s[i:j + 4] for i in range(length) for j in range(i, length)]


key_possibilities = 0


def keygen():
    keys = {}
    for k, v in cleartext_mapping_count.items():
        if v >= 1:
            if k not in keys:
                keys[k] = set()
            keys[k].add(k)
            for letter in available:
                if k != letter:
                    keys[k].add(k + letter)
        elif v == 0:
            if k not in keys:
                keys[k] = set()
            for l1 in available:
                for l2 in available:
                    keys[k].add(l1)
                    keys[k].add(l2)
                    if l1 != l2:
                        keys[k].add(l1 + l2)
    return keys

pp.pprint(keygen())

