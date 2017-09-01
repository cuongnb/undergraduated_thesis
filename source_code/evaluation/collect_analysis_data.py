# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 14:35:15 2015

@author: doanphongtung
"""
import sys

def read_data(data_file_name):
    f = open(data_file_name, 'r')
    line = f.readline()
    f.close()
    return(line)
    
def write_data(result_file_name, method, line):
    line = method + ', ' + line + '\n'
    f = open(result_file_name, 'a')
    f.writelines(line)
    f.close()

def get_methods_files(models_folders):
    methods = list()
    # get methods
    for i in range(len(models_folders)):
        items = models_folders[i].split('/')
        for j in range(len(items)):
            if items[j] == 'gibb_twitter':
                methods.append(items[j + 1])
                break
    return(methods)             

def main():
    if (len(sys.argv) < 3):
        print 'usage: python inter_topic.py <result-file-name> <data-type> <list-of-model-folders>'
        sys.exit(1)
    # get environmental arguments
    result_file_name = sys.argv[1]
    data_type = int(sys.argv[2]) # 0:coherence LCP, 1:coherence NPMI, 2:inter topic , 3:perplexities
    if data_type < 0 and data_type > 3:
        print 'data type : 0:coherence LCP, 1:coherence NPMI, 2:inter topic , 3:perplexities'
        sys.exit(1)
    models_folders = list()
    for m in range(3, len(sys.argv)):
        models_folders.append(sys.argv[m])
    methods = get_methods_files(models_folders)
    # data selection
    data = list()
    data.append('mean-LCP-coherence-top20.csv')
    data.append('mean-NPMI-coherence-top20.csv')
    data.append('inter-topic-top20.csv')
    data.append('perplexities.csv')
    # write files
    for i in range(len(methods)):
        # read data
        data_file_name = models_folders[i] + '/' + data[data_type]
        line = read_data(data_file_name)
        write_data(result_file_name, methods[i], line)   
    print'done!!!'
if __name__ == '__main__':
    main()
