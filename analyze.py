#!/usr/bin/env python3

import pprint as pp
import collections

ciphertext = 'OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR'
alphabet = set(ciphertext)
used = set()

alphabet_len = len(alphabet)
print("Alphabet Length: %d\n" % alphabet_len)

cleartext  = 'OBKRUOXOGHULBSOLIFBBWFLRVNORTHEASTOTWTQSJQSSEKZZWATJKLUDIAWINFBBERLINCLOCKWGDKZXTJCDIGKUHUAUEKCAR'

possibilities = {}

for i in range(len(ciphertext)):
    if ciphertext[i] != cleartext[i]:
        if ciphertext[i] not in possibilities:
            possibilities[ciphertext[i]] = set()
        possibilities[ciphertext[i]].add(cleartext[i])
        used.add(cleartext[i])
print("KNOWN ALPHABET:\n")
ordered = collections.OrderedDict(sorted(possibilities.items()))
pp.pprint(ordered)
print("")

unsolved_alphabet = alphabet.copy()
for letter in possibilities.keys():
    unsolved_alphabet.remove(letter)
print("UNKNOWN ALPHABET:\n%s\n" % sorted(unsolved_alphabet))
print("USED: %s" % sorted(used))
unused = alphabet
for letter in used:
    unused.remove(letter)
print("UNUSED: %s" % sorted(unused))
