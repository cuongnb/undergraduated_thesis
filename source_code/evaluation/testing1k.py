# -*- coding: utf-8 -*-
"""
Created on Mon May 11 16:15:28 2015

@author: dhbk
"""
import numpy as np
import sys, random

def devide_data(raw_data, part_1, part_2, indexes, times):
    fp_raw_data = open(raw_data, 'r')
    fp_part_1 = open(part_1, 'w')
    fp_part_2 = open(part_2, 'w')
    raw_index = 0
    new_index = 0
    while True:
        line = fp_raw_data.readline()
        # check end of file
        if len(line) < 5:
            break
        raw_index += 1
        if raw_index != indexes[new_index]:
            fp_part_1.writelines(line)
        else:
            fp_part_2.writelines(line)
            if new_index < (times - 1):
                new_index += 1
		print new_index
    fp_raw_data.close()
    fp_part_1.close()
    fp_part_2.close()

def main():
    # check
    if len(sys.argv) != 5:
        print'usage: python testing1k.py [raw_data_file] [part_1_file] [part_2_file] [num_docs]'
        exit()
    raw_data_file_name = sys.argv[1]
    part_1_file_name = sys.argv[2]
    part_2_file_name = sys.argv[3]
    num_docs = int(sys.argv[4])
    #
    times = 1000
    indexes = np.sort(random.sample(xrange(num_docs), times))
    # devide data
    devide_data(raw_data_file_name, part_1_file_name, part_2_file_name, indexes, times)
if __name__ == '__main__':
    main()
