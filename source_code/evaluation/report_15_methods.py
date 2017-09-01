# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 16:10:22 2015

@author: doanphongtung
"""

import sys
import numpy as np

def read_file(path):
    f = open(path, 'r')
    line = f.readline()
    f.close()
    temp = line.split(',')
    del temp[-1]
    return (temp)
    
def write_file(path, matrix, methods, _type):
    f = open(path, 'w')
    num_methods = matrix.shape[1]
    num_running = matrix.shape[0]
    types = ['minibatch', 'run']
    type_index = 0
    if _type == 'fin':
        type_index = 1 
    #
    f.write('methods,')
    for i in range(num_methods - 1):
        f.write('%s,' % (methods[i]))
    f.write('%s\n' % (methods[num_methods - 1]))
    #
    for i in range(num_running):
        f.write('%s %d,' % (types[type_index], i+1))
        for j in range (num_methods - 1):
            f.write('%f,' % (matrix[i][j]))
        f.write('%f\n' % (matrix[i][num_methods - 1]))          
    f.close()
    
def read_time(path):
    f = open(path, 'r')
    e_time_list = list()
    m_time_list = list()
    lines = f.readlines()
    for line in lines:
        temp = line.split(',')
        e_time_list.append(temp[1])
        m_time_list.append(temp[2])
    f.close()
    return (e_time_list, m_time_list)
    
def average_time(models):
    time_file_name = 'time.csv'
    e_time = list()
    m_time = list()
    for model in models:
        path = '%s/%s' % (model, time_file_name)
        (e_time_list, m_time_list) = read_time(path)
        e_time.append(e_time_list)
        m_time.append(m_time_list)
    e = np.array(e_time, dtype = float)
    m = np.array(m_time, dtype = float)
    ave_e = e.sum(axis = 0)
    ave_e /= e.shape[0]
    ave_m = m.sum(axis = 0)
    ave_m /= m.shape[0]
    return (ave_e, ave_m)

def average_perplexity(models):
    perplexity_file_name = 'perplexities.csv'
    lines = list()
    for model in models:
        path = '%s/%s' % (model, perplexity_file_name)
        line = read_file(path)
        lines.append(line)
    per = np.array(lines, dtype = float)
    ave = per.sum(axis = 0)
    ave /= per.shape[0]
    return (ave)

def average_coherence(models):
    coherence_file_name = 'mean-NPMI-coherence-top20.csv'
    lines = list()
    for model in models:
        path = '%s/%s' % (model, coherence_file_name)
        line = read_file(path)
        lines.append(line)
    coh = np.array(lines, dtype = float)
    ave = coh.sum(axis = 0)
    ave /= coh.shape[0]
    return (ave)

def median_perplexity(models):
    perplexity_file_name = 'perplexities.csv'
    lines = list()
    for model in models:
        path = '%s/%s' % (model, perplexity_file_name)
        line = read_file(path)
        lines.append(line)
    per = np.array(lines, dtype = float)
    med = np.zeros(per.shape[1], dtype = float)
    for i in range(len(med)):
        med[i] = np.median(per[:,i])
    return (med)

def median_coherence(models):
    perplexity_file_name = 'mean-NPMI-coherence-top20.csv'
    lines = list()
    for model in models:
        path = '%s/%s' % (model, perplexity_file_name)
        line = read_file(path)
        lines.append(line)
    coh = np.array(lines, dtype = float)
    med = np.zeros(coh.shape[1], dtype = float)
    for i in range(len(med)):
        med[i] = np.median(coh[:,i])
    return (med)
    
def final_perplexity(models):
    perplexity_file_name = 'perplexities.csv'
    num_model = len(models)
    finals = np.zeros(num_model)
    for i in range(num_model):
        path = '%s/%s' % (models[i], perplexity_file_name)
        line = read_file(path)
        finals[i] = float(line[len(line) - 1])
    return (finals)
            
def final_coherence(models):
    coherence_file_name = 'mean-NPMI-coherence-top20.csv'
    num_model = len(models)
    finals = np.zeros(num_model)
    for i in range(num_model):
        path = '%s/%s' % (models[i], coherence_file_name)
        line = read_file(path)
        finals[i] = float(line[len(line) - 1])
    return (finals)

#####################################################################
def main():
    if (len(sys.argv) != 3):
        print 'usage: python report_15_methods.py <model-folder> <result-folder>'
        sys.exit(1)
    # get environmental arguments
    models_folder = sys.argv[1]
    result_folder = sys.argv[2]
    # declare variables
    types = ['nyt', 'pubmed', 'yahoo']
    methods = ['ML_CGS', 'ML_CVB0', 'ML_FW', 'ML_OFW', 'ML_VB',
               'Online_CGS', 'Online_CVB0', 'Online_FW', 'Online_OFW', 'Online_VB',
               'Streaming_CGS', 'Streaming_CVB0', 'Streaming_FW', 'Streaming_OFW', 'Streaming_VB']
    models = [[] for i in range(len(methods))]
    for i in range(len(methods)):
        for j in range(len(types)):
            for k in range(5):
                models[i].append('%s/%s/%s_%d' % (models_folder, methods[i], types[j], k+1))
    # report
    # average_perplexities
    for j in range(len(types)):
        lines = list()
        for i in range(len(methods)):
            ave = average_perplexity(models[i][(j*5):(j*5+5)])
            lines.append(ave)
        matrix = np.array(lines).T
        path = '%s/average_perplexities_%s.csv' % (result_folder, types[j])
        write_file(path, matrix, methods, 'ave')
    # average_coherence
    for j in range(len(types)):
        lines = list()
        for i in range(len(methods)):
            ave = average_coherence(models[i][(j*5):(j*5+5)])
            lines.append(ave)
        matrix = np.array(lines).T
        path = '%s/average_coherence_%s.csv' % (result_folder, types[j])
        write_file(path, matrix, methods, 'ave')
    # median_perplexities
    for j in range(len(types)):
        lines = list()
        for i in range(len(methods)):
            med = median_perplexity(models[i][(j*5):(j*5+5)])
            lines.append(med)
        matrix = np.array(lines).T
        path = '%s/median_perplexities_%s.csv' % (result_folder, types[j])
        write_file(path, matrix, methods, 'ave')
    # median_coherence
    for j in range(len(types)):
        lines = list()
        for i in range(len(methods)):
            med = median_coherence(models[i][(j*5):(j*5+5)])
            lines.append(med)
        matrix = np.array(lines).T
        path = '%s/median_coherence_%s.csv' % (result_folder, types[j])
        write_file(path, matrix, methods, 'ave')
    # final_perplexities
    for j in range(len(types)):
        lines = list()
        for i in range(len(methods)):
            fin = final_perplexity(models[i][(j*5):(j*5+5)])
            lines.append(fin)
        matrix = np.array(lines).T
        path = '%s/final_perplexities_%s.csv' % (result_folder, types[j])
        write_file(path, matrix, methods, 'fin')
    # final_coherence
    for j in range(len(types)):
        lines = list()
        for i in range(len(methods)):
            fin = final_coherence(models[i][(j*5):(j*5+5)])
            lines.append(fin)
        matrix = np.array(lines).T
        path = '%s/final_coherence_%s.csv' % (result_folder, types[j])
        write_file(path, matrix, methods, 'fin')
    # average time
    for j in range(len(types)):
        e_lines = list()
        m_lines = list()
        for i in range(len(methods)):
            (ave_e, ave_m) = average_time(models[i][(j*5):(j*5+5)])
            e_lines.append(ave_e)
            m_lines.append(ave_m)
        e_matrix = np.array(e_lines).T
        m_matrix = np.array(m_lines).T
        t_matrix = e_matrix + m_matrix
        path = '%s/average_e_time_%s.csv' % (result_folder, types[j])
        write_file(path, e_matrix, methods, 'ave')
        path = '%s/average_t_time_%s.csv' % (result_folder, types[j])
        write_file(path, t_matrix, methods, 'ave')                    
    print 'done!!!'
if __name__ == '__main__':
    main()
