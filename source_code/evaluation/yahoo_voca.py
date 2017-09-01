# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 22:18:15 2015

@author: doanphongtung
"""
import sys

def main():
    original_file_name = sys.argv[1]
    yahoo_voca_file_name = sys.argv[2]
    max_count = 0
    with open(original_file_name) as original_file:
        for line in original_file:
            line = line.strip()
            tokens = line.split(' ')
            length = len(tokens)
            for i in xrange(length):
                if int(tokens[i]) > max_count:
                    max_count = int(tokens[i])
    yahoo_voca_file = open(yahoo_voca_file_name, 'w')
    yahoo_voca_file.writelines('number of terms: %d' % (max_count + 1))
    yahoo_voca_file.close()
    print 'done!!!'
if __name__ == '__main__':
    main()
    