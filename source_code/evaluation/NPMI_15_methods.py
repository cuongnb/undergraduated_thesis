# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 14:48:16 2015

@author: doanphongtung
"""

import os, sys, string
import numpy as np

def read_minibatch(fp, batch_size):
    wordids = list()
    stop = 0
    for i in range(batch_size):
        line = fp.readline()
        # check end of file
        if len(line) < 5:
            stop = 1
            break
        ids = list()
        terms = string.split(line)
        for i in range(1,int(terms[0]) + 1):
            term_count = terms[i].split(':')
            ids.append(int(term_count[0]))
        wordids.append(ids)
    return(wordids, stop)    

def parse_docs(corp):
    wordids = list()
    for line in corp:
        ids = list()
        terms = string.split(line)
        for i in range(1,int(terms[0]) + 1):
            term_count = terms[i].split(':')
            ids.append(int(term_count[0]))
        wordids.append(ids)
    return(wordids)

def read_topics(folder, i, j):
    filename = '%s/top20_%d_%d.dat' % (folder, i+1, j+1)
    topics = np.loadtxt(filename)
    topics = topics.astype(int)
    return(topics)
    
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
    
def filter_topics(folder, i, j, filtered_tops):
    filename = '%s/top20_%d_%d.dat' % (folder, i+1, j+1)
    # get topics
    topics = np.loadtxt(filename)
    K = topics.shape[0]
    T = topics.shape[1]
    for k in range(K):
        for t in range(T):
            if not int(topics[k][t]) in filtered_tops:
                filtered_tops.append(int(topics[k][t]))

def co_dfreq_all(wordids, filtered_tops, num_terms, df, duv):
    tmp = list()
    for i in range(num_terms):
        if filtered_tops[i] in wordids:
            df[i] += 1
            tmp.append(i)
    n = len(tmp)
    if n < 2: return
    for i in range(n):
        for j in range(i+1, n):
            duv[tmp[i]][tmp[j]] += 1
            duv[tmp[j]][tmp[i]] += 1

#####################################################################
def main():
    if (len(sys.argv) != 3):
        print 'usage: python NPMI_15_methods.py <data-folder> <model-folder>'
        sys.exit(1)
    # get environmental arguments
    data_folder = sys.argv[1]
    models_folder = sys.argv[2]
    # data_types
    types = ['nyt', 'pubmed', 'yahoo']
    # get data files
    data_files = list()
    for _type in types:
        data_files.append('%s/%s/%s_training_100k_frequencies.txt' % (data_folder, _type, _type))
    # get methods
    methods = os.listdir(models_folder)
    # get gibb_models
    models_folder_in_type = [[] for i in range(len(types))]
    for method in methods:
        path = '%s/%s' % (models_folder, method)
        models = os.listdir(path)
        for model in models:
            for i in range(len(types)):
                if types[i] in model:
                    models_folder_in_type[i].append('%s/%s' % (path, model))
                    break
    # compute NPMI
    for i in range(len(types)):
        print '----------type : %s----------' % (types[i])
        data_file = data_files[i]
        models = models_folder_in_type[i]
        filtered_tops = list()
        for model in models:
            print 'folder %s' % (model)
            # read loop
            print 'reading loops ...'
            (I, J) = read_loops(model)
            # filter topics
            print'filtering topics ...'
            for i in range(I):
                for j in range(J):
                    filter_topics(model, i, j, filtered_tops)
        filtered_tops.sort()
        num_terms = len(filtered_tops)
        print '\t number of terms in topics %d' % (num_terms)
        print 'reading data...'
        corp  = file(data_file, 'r').readlines()
        wordids = parse_docs(corp)
        del corp
        # define constants
        N = len(wordids) # number of documents in training data
        logN = np.log(N) # 
        # compute co-frequenciesmean-NPMI-coherence-top20.csv
        print'computing co-frequencies ...'
        df = [0 for i in range(num_terms)]
        duv = [[] for i in range(num_terms)]
        for i in range(num_terms):
            duv[i] = [1 for j in range(num_terms)]
        for d in range(N):
            co_dfreq_all(wordids[d], filtered_tops, num_terms, df, duv)
            if d%10000 == 0: print d
        del wordids
        # compute coherence of topic gibb_models
        print'computing topic coherence of gibb_twitter ...'
        for model in models:
            print model
            # file names for writing NPMI measures
            filename_mean_NPMI = '%s/mean-NPMI-coherence-top20.csv' % (model)
            fmean_NPMI = open(filename_mean_NPMI, 'w')
            filename_median_NPMI = '%s/median-NPMI-coherence-top20.csv' % (model)
            fmedian_NPMI = open(filename_median_NPMI, 'w')
            filename_coh_NPMI = '%s/coherence-NPMI-top20.csv' % (model)
            for i in range(I):
                for j in range(J):
                    print 'loop %d minibatch %d' % (i+1, j+1)
                    # Read the learned model
                    print '\t reading model...'
                    list_top = read_topics(model, i, j)
                    K = list_top.shape[0]
                    T = list_top.shape[1]
                    #Compute coherence for topics
                    print '\t computing coherence...'
                    ch_NPMI = []
                    for k in range(K):
                        # get indices of terms in filtered topic list
                        index = []
                        for t in range(T):
                            index.append(filtered_tops.index(list_top[k][t]))
                        # compute
                        total_NPMI = 0.
                        for ii in range(1,T):
                            for jj in range(0, ii):
                                if(duv[index[ii]][index[jj]]) != 0 and (df[index[ii]] > 0) and (df[index[jj]] > 0):
                                    total_NPMI += -1. + (np.log(df[index[ii]] * \
                                    df[index[jj]]) - 2*logN) / (np.log(duv[index[ii]][index[jj]]) - logN)
                        ch_NPMI.append(total_NPMI)
                    print 'NPMI %f' % np.mean(ch_NPMI)
                    #fmean = open(filename_mean, 'a')
                    fmean_NPMI.writelines('%f,' % np.mean(ch_NPMI))
                    #fmedian = open(filename_median, 'a')
                    fmedian_NPMI.writelines('%f,' % np.median(ch_NPMI))
                    coh_NPMI = open(filename_coh_NPMI, 'a')
                    coh_NPMI.writelines('%f,' % item for item in ch_NPMI)
                    coh_NPMI.writelines('\n')
                    coh_NPMI.close()
            fmean_NPMI.close()
            fmedian_NPMI.close()
    print 'done!!!'
if __name__ == '__main__':
    main()
