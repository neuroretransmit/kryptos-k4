#!/usr/bin/env python3

import pprint as pp
import itertools
from collections import OrderedDict
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

unused = alphabet.copy()
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
    for letter in sorted(alphabet):
        if letter in known_ciphered_mapping:
            keys[letter] = known_ciphered_mapping[letter]
            if len(keys[letter]) == 1:
                for l1 in available:
                    if l1 not in keys[letter]:
                        keys[letter].add(l1)
        else:
            keys[letter] = set()
            for l1 in available:
                keys[letter].add(l1)
                for l2 in available:
                    if l1 != l2:
                        keys[letter].add(l1)
                        keys[letter].add(l2)
    permuted = dict()
    for k, v in keys.items():
        permutations = set()
        if len(v) != 2:
            for l1 in v:
                permutations.add(l1)
                if len(v) != 1:
                    for l2 in v:
                        if l1 != l2:
                            permutations.add(l1 + l2)
            permuted[k] = permutations
        else:
            permuted[k] = set()
            permuted[k].add(''.join(v))
    return permuted


def prune_keys(keys):
    # Cleartext letters already used twice between ciphertext letters
    cleartext_used_twice = ['L', 'E', 'T', 'C', 'N', 'O']
    # Ciphered letters to skip because they already have two values
    ciphered_to_skip = ['N', 'P', 'Q', 'T']
    new_keys = keys.copy()
    for k, v in keys.items():
        if k in ciphered_to_skip:
            continue
        for possibility in v:
            for candidate in cleartext_used_twice:
                if candidate in possibility:
                    new_key = v.copy()
                    new_key.remove(possibility)
                    new_keys[k] = new_key
    return new_keys

pp.pprint(prune_keys(keygen()))

