# Marco Riggirello

import argparse

parser = argparse.ArgumentParser(prog='ABCounter', description='Counts the relative frequencies of letters (case unsensitive).')
parser.add_argument('fname', help='The name of the text file to be processed.')

args = parser.parse_args()

letters = 'abcdefghijklmnopqrstuvwxyz'
text = open(args.fname, 'r').read().lower()

abs_freqs = dict(zip(letters, list(map(text.count, letters))))
tot = sum(abs_freqs.values())

print('--------|-----------')
print(' letter | freq. [%]')
print('--------|-----------')
for ch in abs_freqs:
    print(f' {ch}      | {100*abs_freqs[ch]/tot:.2f}')

