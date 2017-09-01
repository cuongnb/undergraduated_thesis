# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 22:58:04 2015

@author: doanphongtung
"""

import sys

def main():
    sequences_file_name = sys.argv[1]
    frequencies_file_name = sys.argv[2]
    frequencies_file = open(frequencies_file_name, 'w')
    with open(sequences_file_name) as sequences_file:
        for line in sequences_file:
            ddict = dict()
            line = line.strip()
            tokens = line.split(' ')
            for token in tokens:
                temp = int(token)
                if temp not in ddict:
                    ddict[temp] = 1
                else:
                    ddict[temp] += 1
            keys = ddict.keys()
            keys.sort()
            length = len(keys)
            frequencies_file.write('%d ' % length)
            for i in xrange(length - 1):
                frequencies_file.write('%d:%d ' % (keys[i], ddict[keys[i]]))
            frequencies_file.write('%d:%d\n' % (keys[length - 1], ddict[keys[length - 1]]))
    frequencies_file.close()
    print 'done!!!'
if __name__ == '__main__':
    main()