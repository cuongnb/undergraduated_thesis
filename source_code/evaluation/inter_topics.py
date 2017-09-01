# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 09:03:42 2015

@author: doanphongtung
"""
import sys

def compute_inter_topic(file_name):
    total_count = dict()
    with open(file_name) as f:
        for line in f:
            temp1 = line.strip()
            temp2 = temp1.split(' ')
            length = len(temp2)
            for i in range(length):
                tid = int(temp2[i])
                if tid not in total_count:
                    total_count[tid] = 1
                else:
                    total_count[tid] += 1
    result = 0
    for key in total_count:
        if (total_count[key] == 1):
            result += 1
    return result
    
def read_loops(model_folder):
    loops_filename = '%s/loops.csv'%(model_folder)
    f = open(loops_filename, 'r')
    line = f.readline()
    ij = line.split(',')
    I = int(ij[0])
    J = int(ij[1])
    print'model folder: %s'%(model_folder)
    print'\t number of iters of training %d'%(I)
    print'\t number of minibatch %d'%(J)
    return(I, J)
    
def main():
    if (len(sys.argv) < 2):
        print 'usage: python inter_topic.py <list-of-model-folders>'
        sys.exit(1)
    for m in range(1, len(sys.argv)):
        # read loop
        print'reading loops ...'
        model = sys.argv[m]
        (I, J) = read_loops(model)
        # compute inter topic
        print model
        filename_inter_topic = '%s/inter-topic-top20.csv' % (model)
        finter_topic = open(filename_inter_topic, 'w')
        for i in range(I):
            for j in range(J):
                print 'loop %d minibatch %d' % (i+1, j+1)
                filename_topic_N = '%s/top20_%d_%d.dat' % (model, i+1, j+1)
                result = compute_inter_topic(filename_topic_N)
                print '%d' % (result)
                finter_topic.writelines('%d,' % (result))
        finter_topic.close()
    print'done!!!'
if __name__ == '__main__':
    main()      