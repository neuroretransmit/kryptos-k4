#!/usr/bin/env python3

import pprint as pp

ciphertext      = 'OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR'
known_cleartext = 'OBKRUOXOGHULBSOLIFBBWFLRVNORTHEASTOTWTQSJQSSEKZZWATJKLUDIAWINFBBERLINCLOCKWGDKZXTJCDIGKUHUAUEKCAR'

alphabet = set(ciphertext)

# Populate known cipher characters to cleartext characters and used cleartext characters
known_ciphered_mapping = {}
used = set()
for i in range(len(ciphertext)):
    if ciphertext[i] != known_cleartext[i]:
        if ciphertext[i] not in known_ciphered_mapping:
            known_ciphered_mapping[ciphertext[i]] = set()
        known_ciphered_mapping[ciphertext[i]].add(known_cleartext[i])
        used.add(known_cleartext[i])

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
    """ Generate all possible values for ciphertext letters ignoring assumptions """
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


# Ciphered letters to skip because they already have two values
ciphered_to_skip = ['N', 'P', 'Q', 'T']


def check_assumptions(unique_key):
    """ Check assumptions that a ciphertext value can only have two plaintext values
    and that plaintext values are only used a maximum of two times
    :param unique_key:
    :return:
    """
    mapping_count = cleartext_mapping_count.copy()
    for k, v in unique_key.items():
        # Exclude ciphered mappings that already have two values
        if k in ciphered_to_skip:
            continue
        for possibility in v:
            # Exclude already counted single char mappings
            if (k == 'F' and possibility == 'O')\
              or (k == 'G' and possibility == 'E') \
              or (k == 'K' and possibility == 'A') \
              or (k == 'M' and possibility == 'C') \
              or (k == 'R' and possibility == 'T') \
              or (k == 'S' and possibility == 'T') \
              or (k == 'V' and possibility == 'L') \
              or (k == 'Y' and possibility == 'E') \
              or (k == 'Z' and possibility == 'L'):
                continue
            else:
                if mapping_count[k] + 1 > 2:
                    return False
                mapping_count[k] += 1
    return True


def get_unique_key(initial_prune, ciphererd_key, value_pos, attempted_indices):
    unique_key = dict()
    unique_key[ciphererd_key] = list(initial_prune[ciphererd_key])[value_pos]
    for k, v in initial_prune.items():
        if k == ciphererd_key:
            continue
        unique_key[k] = list(initial_prune[k])[attempted_indices[k]]
        if attempted_indices[k] + 1 >= len(initial_prune[k]):
            continue
        else:
            attempted_indices[k] += 1
    return unique_key, attempted_indices


# Cleartext letters already used twice between ciphertext letters
cleartext_used_twice = ['L', 'E', 'T', 'C', 'N', 'O']


def prune_keys(keys):
    viable_keys = list()
    initial_prune = keys.copy()
    for k, v in keys.items():
        # Skip ciphered chars that already have two plaintext chars
        if k in ciphered_to_skip:
            continue
        for possibility in v:
            # Prune the possibilites that contain cleartext already used twice
            for candidate in cleartext_used_twice:
                if candidate in possibility:
                    new_key = v.copy()
                    new_key.remove(possibility)
                    initial_prune[k] = new_key
    for k, v in initial_prune.items():
        attempted_indices = {
            'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0,
            'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0,
            'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0,
            'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0,
            'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0,
            'Z': 0,
        }
        for i in range(len(v)):
            unique_key, attempted_indices = get_unique_key(initial_prune, k, i, attempted_indices)
            attempted_indices[k] = i
            if not check_assumptions(unique_key):
                continue
            else:
                viable_keys.append(unique_key)
    return viable_keys


print("Viable keys:")
pp.pprint(prune_keys(keygen()))
