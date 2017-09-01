# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 14:32:35 2015

@author: bkhn
"""
import sys, os

def main():
    if (len(sys.argv) != 2):
        print 'usage: python report_15_methods.py <model-folder>'
        sys.exit(1)
    # get environmental arguments
    models_folder = sys.argv[1]
    # declare variables
    deleting_files = ['coherence-NPMI-top20.csv', 'mean-NPMI-coherence-top20.csv', 'median-NPMI-coherence-top20.csv']
    types = ['nyt', 'pubmed', 'yahoo']
    methods = ['ML_CGS', 'ML_CVB0', 'ML_FW', 'ML_OFW', 'ML_VB',
               'Online_CGS', 'Online_CVB0', 'Online_FW', 'Online_OFW', 'Online_VB',
               'Streaming_CGS', 'Streaming_CVB0', 'Streaming_FW', 'Streaming_OFW', 'Streaming_VB']
    models = [[] for i in range(len(methods))]
    for i in range(len(methods)):
        for j in range(len(types)):
            for k in range(5):
                models[i].append('%s/%s/%s_%d' % (models_folder, methods[i], types[j], k+1))
    for method_models in models:
        for model in method_models:
            for deleting_file in deleting_files:
                file_name = '%s/%s' % (model, deleting_file)
                if os.path.exists(file_name):
                    print file_name
                    os.remove(file_name)
print 'done!!!'
if __name__ == '__main__':
    main()