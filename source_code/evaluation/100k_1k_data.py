# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 21:04:46 2015

@author: doanphongtung
"""
import sys

def main():
    original_file_name = sys.argv[1]
    training_file_name = sys.argv[2]
    testing_file_name = sys.argv[3]
    original_file = open(original_file_name, 'r')
    training_file = open(training_file_name, 'w')
    testing_file = open(testing_file_name, 'w')
    # 100k
    for i in xrange(100000):
        line = original_file.readline()
        training_file.writelines(line)
    # 1k
    for i in xrange(1000): 
        line = original_file.readline()
        testing_file.writelines(line)
    original_file.close()
    training_file.close()
    testing_file.close()
    print 'done!!!'
if __name__ == '__main__':
    main()