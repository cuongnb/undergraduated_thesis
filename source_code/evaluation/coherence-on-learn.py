import sys, string
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
    if (len(sys.argv) < 3):
        print 'usage: python coherence-ovb-dolda.py <data-file> <list-of-model-folders>'
        sys.exit(1)
    # get environmental arguments
    data_file = sys.argv[1]
    filtered_tops = list()
    for m in range(2, len(sys.argv)):
        # read loop
        print'reading loops ...'
        model = sys.argv[m]
        (I_ofw, J_ofw) = read_loops(model)
        # filter topics
        print'filtering topics ...'
        for i in range(I_ofw):
            for j in range(J_ofw):
                filter_topics(model, i, j, filtered_tops)
    filtered_tops.sort()
    num_terms = len(filtered_tops)
    print'\t number of terms in topics %d'%(num_terms)

    print 'reading data...'
    corp  = file(data_file, 'r').readlines()
    wordids = parse_docs(corp)
    del corp
    # compute co-frequencies
    print'computing co-frequencies ...'
    df = [0 for i in range(num_terms)]
    duv = [[] for i in range(num_terms)]
    for i in range(num_terms):
        duv[i] = [1 for j in range(num_terms)]
    for d in range(len(wordids)):
        co_dfreq_all(wordids[d], filtered_tops, num_terms, df, duv)
        if d%10000 == 0: print d
    del wordids
    # compute coherence of topic models
    print'computing topic coherence of gibb_twitter ...'
    for m in range(2, len(sys.argv)):
        model = sys.argv[m]
        print model
        filename_mean = '%s/mean-coherence-top20.csv' % (model)
        fmean = open(filename_mean, 'w')
        for i in range(I_ofw):
            for j in range(J_ofw):
                fmean.writelines('loop %d minibatch %d,' % (i+1, j+1))
        fmean.writelines('\n')
        filename_median = '%s/median-coherence-top20.csv' % (model)
        fmedian = open(filename_median, 'w')
        for i in range(I_ofw):
            for j in range(J_ofw):
                fmedian.writelines('loop %d minibatch %d,' % (i+1, j+1))
        fmedian.writelines('\n')
        filename_coh = '%s/coherence-top20.csv' % (model)
        for i in range(I_ofw):
            for j in range(J_ofw):
                print 'loop %d minibatch %d' % (i+1, j+1)
                # Read the learned model
                print '\t reading model...'
                list_top = read_topics(model, i, j)
                K = list_top.shape[0]
                T = list_top.shape[1]
                #Compute coherence for topics
                print '\t computing coherence...'
                ch  = []
                for k in range(K):
                    # get indices of terms in filtered topic list
                    index = []
                    for t in range(T):
                        index.append(filtered_tops.index(list_top[k][t]))
                    # compute
                    total = 0
                    for ii in range(1,T):
                        for jj in range(0, ii):
                            if(df[index[jj]] > 0):
                                total += np.log(float(duv[index[ii]][index[jj]]) / df[index[jj]])
                    ch.append(total)
                print '%f ' % np.mean(ch)
                #fmean = open(filename_mean, 'a')
                fmean.writelines('%f,' % np.mean(ch))
                #fmean.close()
                #fmedian = open(filename_median, 'a')
                fmedian.writelines('%f,' % np.median(ch))
                #fmedian.close()
                coh = open(filename_coh, 'a')
                coh.writelines('%f,' % item for item in ch)
                coh.writelines('\n')
                coh.close()
        fmean.close()
        fmedian.close()
    print'done!!!'
if __name__ == '__main__':
    main()
