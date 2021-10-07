'''Marco Riggirello'''

from time import time
import argparse
import matplotlib.pyplot as plt

def counter(string):
    '''Returns the absolute frequency of letters in a string into a dictionary.
    The counter is case unsensitive.
    '''
    letters = 'abcdefghijklmnopqrstuvwxyz'
    lstr = string.lower()
    return dict(zip(letters, list(map(lstr.count, letters))))

if __name__ == '__main__':
    start = time()
    DESC = 'Counts the relative frequencies of letters (case unsensitive).'
    parser = argparse.ArgumentParser(prog='ABCounter', description=DESC)
    parser.add_argument('fname', help='The name of the text file to be processed.')
    parser.add_argument('-p', '--plot', action='store_true',\
            help='Plot histogram of letters frequency.')

    args = parser.parse_args()
    with open(args.fname, 'r', encoding='utf-8') as file:
        text = file.read()

    abs_freqs = counter(text)
    tot = sum(abs_freqs.values())

    print('--------|-----------')
    print(' letter | freq. [%]')
    print('--------|-----------')
    for ch in abs_freqs:
        print(f' {ch}      | {100*abs_freqs[ch]/tot:.2f}')

    if args.plot:
        plt.bar(*zip(*abs_freqs.items()))
        plt.title(args.fname)
        plt.show()

    stop = time()
    print(f'\nTotal elapsed time: {stop-start:.3f}s.')
