'''
play fair cypher

based on : https://medium.com/analytics-vidhya/play-fair-cipher-encryption-using-python3-f91c42931f52

by: Dan Trepanier

October 3, 2020
'''

import argparse
import numpy as np

def convert_to_pairs(lst):
    return list(map(lambda i: tuple(lst[i:i+2]), range(0,len(lst), 2)))
    
class PlayFair(object):
    def __init__(self, key):
        self.key = key.lower()
        self.full_key = self._get_full_key()
        self.A = np.arange(25).reshape(5,5)
    
    def _get_full_key(self):
        # returns a flat list with the key and all remaining letters of the alphabet
        # but all "j" occurences become "i"
        cleaner = {'j':'i'}
        alphabet = list(map(lambda i: chr(i), range(97, 97+26)))
        new = []
        for x in list(self.key) + alphabet:
            c = cleaner.get(x, x)
            if c not in new:
                new += [c]
        assert len(new) == 25
        return new
    
    def encrypt(self, txt):
        new = []
        last = None
        for x in txt:
            if x == ' ':
                new += ['x']
            elif x == last:
                new += ['x',x]
            else:
                new += [x]
            last = x
        if len(new) % 2 != 0:
            new += ['x']
        pairs = convert_to_pairs(new)
        out = ''
        for pair in pairs:
            out += ''.join(self.parse_pair(pair))
        return out
    
    def decrypt(self, txt):
        pairs = convert_to_pairs(list(txt))
        lst = []
        for pair in pairs:
            lst += self.parse_pair(pair, reverse=True)
        final = ''
        for i,x in enumerate(lst):
            if x == 'x':
                c = ' '
                if i > 0 and i < len(lst) - 1:
                    bef = lst[i-1]
                    aft = lst[i+1]
                    if bef == aft:
                        c = ''
            else:
                c = x
            final += c
        return final
        
    def parse_pair(self, pair, reverse=False):
        mult = -2 * int(reverse) + 1
        assert len(pair) == 2
        # get index of each letter from the full_key
        first = self.full_key.index(pair[0].lower())
        second = self.full_key.index(pair[1].lower()) 
        # get coordinates (column, row)
        c_1 = np.where(self.A == first)
        c_2 = np.where(self.A == second)
        
        if c_1[0] == c_2[0]:
            # column is same, so shift down
            f_1 = (c_1[0], (int(c_1[1]) + mult * 1) % 5)
            f_2 = (c_2[0], (int(c_2[1]) + mult * 1) % 5)
        elif c_1[1] == c_2[1]:
            # row is same, so shift right
            f_1 = ((int(c_1[0]) + mult * 1) % 5, c_1[1])
            f_2 = ((int(c_2[0]) + mult * 1) % 5, c_2[1])
        else:
            # keep row the same but use the column of other character
            f_1 = (c_1[0], c_2[1])
            f_2 = (c_2[0], c_1[1])
        
        i_1 = self.A[f_1][0] # lookup index for first character
        i_2 = self.A[f_2][0] # lookup index for second character
        return [self.full_key[i_1], self.full_key[i_2]]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--key','-k', help="encryption key", type=str, default='rebecca')
    parser.add_argument('--text','-t', help="text to encrypt", type=str, required=True)
    args = parser.parse_args()
    pf = PlayFair(args.key)
    encrypted = pf.encrypt(args.text)
    print('RAW:',args.text)
    print('ENCRYPTED:',encrypted)
    decrypted = pf.decrypt(encrypted)
    print('DECRYPTED:',decrypted)
