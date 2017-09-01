# -*- coding: utf-8 -*-
"""
Created on Sat Jul  5 14:46:02 2014

@author: doanphongtung
"""
import numpy as np
import string, sys

def reform_doc(doc):
    ddict = dict()
    if len(doc) != 0:
        for term in doc:
            if (not term in ddict):
                ddict[term] = 0
            ddict[term] += 1
    keys = sorted(ddict.keys())
    values = list()
    for key in keys:
        values.append(ddict[key])
    return(keys, values)

def divide_doc(wordids, wordcts):
    doc = list()
    doc_part_1 = list()
    doc_part_2 = list()
    index_1 = list()
    index_2 = list()
    # recreate doc
    for j in range(len(wordids)):
        for i in range(wordcts[j]):
            doc.append(wordids[j])
    # divide document randomly with rate 70:30
    doc_len = len(doc)
    d2_len = int(doc_len * 0.3)
    while len(index_2) != d2_len:
        index = np.random.randint(doc_len)
        if index not in index_2:
            index_2.append(index)
    for index in range(doc_len):
        if index not in index_2:
            index_1.append(index)
    for index in index_1:
        doc_part_1.append(doc[index])
    for index in index_2:
        doc_part_2.append(doc[index])
    # reform two documents
    (wordids_1, wordcts_1) = reform_doc(doc_part_1)
    (wordids_2, wordcts_2) = reform_doc(doc_part_2)
    return(wordids_1, wordcts_1, wordids_2, wordcts_2)
  
def wrfile_doc(fp, wordids, wordcts):
    M = len(wordids)
    fp.write('%d'%(M))
    if M != 0:
        for i in range(M):
            fp.write(' %d:%d'%(wordids[i], wordcts[i]))
    fp.write('\n')

"""
------------------------------------------------------------------------------------------------------------------------
"""
        
def main():
    # check
    if len(sys.argv) != 3:
        print'usage: python dividedata.py [data file] [divided files folder]'
        exit()
    datafilename = sys.argv[1]
    foldername = sys.argv[2]
    # read data
    datafile = open(datafilename, 'r')
    docs = list()
    for i in range(1000):
        line = datafile.readline()
        docs.append(line)
    datafile.close()
    # change docs to ids and cts
    wordids = list()
    wordcts = list()
    for doc in docs:
        ids = list()
        cts = list()
        terms = string.split(doc)
        for i in range(1,int(terms[0]) + 1):
            term_count = terms[i].split(':')
            ids.append(int(term_count[0]))
            cts.append(int(term_count[1]))
        wordids.append(ids)
        wordcts.append(cts)
    # divide data
    for i in range(10):
        print'***%d***'%(i + 1)
        filename_1 = '%s/data_test_%d_part_1.txt'%(foldername, i + 1)
        filename_2 = '%s/data_test_%d_part_2.txt'%(foldername, i + 1)
        fp_1 = open(filename_1, 'a')
        fp_2 = open(filename_2, 'a')
        for d in range(1000):
            (wordids_1, wordcts_1, wordids_2, wordcts_2) = divide_doc(wordids[d], wordcts[d])     
            wrfile_doc(fp_1, wordids_1, wordcts_1)
            wrfile_doc(fp_2, wordids_2, wordcts_2)
        fp_1.close()
        fp_2.close()
        
if __name__ == '__main__':
    main()
