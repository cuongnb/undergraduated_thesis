# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 16:14:49 2015

@author: doanphongtung
"""
import sys, string
import numpy as np   

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
    filename = '%s/top10_%d_%d.dat' % (folder, i+1, j+1)
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
    filename = '%s/top10_%d_%d.dat' % (folder, i+1, j+1)
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
    
def online_counting(data_file, batch_size, filtered_tops):
    # numbers of terms and documents
    num_terms = len(filtered_tops)
    num_docs = 0
    # single and double frequencies
    df = [0 for i in range(num_terms)]
    duv = [[] for i in range(num_terms)]
    for i in range(num_terms):
        duv[i] = [1 for j in range(num_terms)]
    # online counting
    fp = open(data_file, 'r')
    count = 0
    while True:
        count += 1
        print 'mini batch %d ...' % (count)
        (wordids, stop) = read_minibatch(fp, batch_size)
        length = len(wordids)
        num_docs += length
        for d in range(length):
            co_dfreq_all(wordids[d], filtered_tops, num_terms, df, duv)
        if stop == 1:
            break   
    fp.close()
    return(df, duv, num_docs)
#####################################################################
def main():
    if (len(sys.argv) < 4):
        print 'usage: python bigdata_NPMI.py <data-file> <batch_size> <list-of-model-folders>'
        sys.exit(1)
    # get environmental arguments
    data_file = sys.argv[1]
    batch_size = int(sys.argv[2])
    filtered_tops = list()
    # ------------------------------------------
    print 'read topic'
    for m in range(3, len(sys.argv)):
	model = sys.argv[m]
        print model
        # read loop
        print'reading loops ...'
        (I, J) = read_loops(model)
        # filter topics
        print'filtering topics ...'
        for i in range(I):
            for j in range(J):
                filter_topics(model, i, j, filtered_tops)
    filtered_tops.sort()
    num_terms = len(filtered_tops)
    print'total terms in topics %d'%(num_terms)
    # ------------------------------------------
    print 'read data and count'
    (df, duv, N) = online_counting(data_file, batch_size, filtered_tops)
    logN = np.log(N)
    # ------------------------------------------
    # compute coherence of topic models
    print'computing topic coherence of gibb_twitter ...'
    for m in range(3, len(sys.argv)):
        model = sys.argv[m]
        print model
        # file names for writing NPMI measures
        filename_mean_NPMI = '%s/mean-NPMI-coherence-top10.csv' % (model)
        fmean_NPMI = open(filename_mean_NPMI, 'w')
        filename_median_NPMI = '%s/median-NPMI-coherence-top10.csv' % (model)
        fmedian_NPMI = open(filename_median_NPMI, 'w')
        filename_coh_NPMI = '%s/coherence-NPMI-top10.csv' % (model)
	# read loops
	(I, J) = read_loops(model)
        for i in range(I):
            for j in range(J):
                print 'loop %d minibatch %d' % (i+1, j+1)
                # Read the learned model
                print 'reading model...'
                list_top = read_topics(model, i, j)
                K = list_top.shape[0]
                T = list_top.shape[1]
                #Compute coherence for topics
                print 'computing coherence...'
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
                                total_NPMI += -1. + (np.log(df[index[ii]] * df[index[jj]]) - 2*logN) / (np.log(duv[index[ii]][index[jj]]) - logN)
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
    print'done!!!'
if __name__ == '__main__':
    main()

