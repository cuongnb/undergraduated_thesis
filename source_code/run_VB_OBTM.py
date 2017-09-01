"""
Created: 31/03/2017
@author: Cuong Nguyen Ba
"""
import os
import shutil
import sys
import time
from datetime import datetime

from btm import drop_vb_obtm
from common import utilities
from common.utilities import write_time

all_dataset_dir = 'dataset'
all_dataset = {'nyt': 'nyt_titles.txt.sf', 'twitter': 'tweet.txt.sf', 'yahoo': 'yahoo.txt.sf'}
setting_file_name = 'settings.txt'
all_model_folder = 'gibb_twitter'


def main():
    # Check input
    if len(sys.argv) != 3:
        print "Usage: python run_Dropout_OnlineVB.py [dataset_name] [drop_rate]"
        print "all dataset: nyt twitter yahoo"
        exit()
    # Get environment variables
    dataset_name = sys.argv[1]
    drop_rate = float(sys.argv[2])

    # dataset_name = "twitter"
    # drop_rate = 0.0

    # em params
    dataset_dir = '/'.join([all_dataset_dir, dataset_name])
    train_file = '/'.join([dataset_dir, all_dataset[dataset_name]])
    setting_file = '/'.join([dataset_dir, setting_file_name])
    rate_name = str(drop_rate)
    rate_name = rate_name.replace('.', '')
    model_name = 'DropOBTMVB' + rate_name
    model_folder = '/'.join([dataset_dir, all_model_folder, model_name])
    divided_data_folder = dataset_dir
    run_em(train_file, setting_file, model_folder, divided_data_folder, drop_rate)


def run_em(train_file, setting_file, model_folder, divided_data_folder, drop_rate):
    tops = 20
    # if os.path.exists(model_folder):
    #     shutil.rmtree(model_folder)
    # os.makedirs(model_folder)
    print 'Perform DropoutOnlineVB with rate = ', drop_rate, ' in ', train_file
    print datetime.now()
    # read settings
    print'\treading setting ...'
    ddict = utilities.read_setting(setting_file)
    # model_folder += 'tau' + str(int(ddict['tau0']))
    if os.path.exists(model_folder):
        shutil.rmtree(model_folder)
    os.makedirs(model_folder)
    # insert to settings
    ddict['drop_rate'] = drop_rate
    # write settings
    print'\twrite setting ...'
    file_name = '%s/setting.txt' % model_folder
    utilities.write_setting(ddict, file_name)

    # data for computing perplexities
    print'\tread data for computing perplexities ...'
    (corpusids_part1, corpuscts_part1, corpusids_part2, corpuscts_part2) = \
        utilities.read_data_for_perpl(divided_data_folder)

    # todo initialize the algorithm
    print'\tinitialize the algorithm ...'
    # num_term, num_topic, alpha, beta, stepCount, stepPower, stepOffset, r_drop
    online_obtm = drop_vb_obtm.VbObtm(ddict['num_terms'], ddict['num_topics'], ddict['alpha'], ddict['beta'],
                                      ddict['step_count'], ddict['step_power'], ddict['step_offset'],
                                      ddict['drop_rate'])

    # start
    print'\tstart!!!'
    iter_no = 0
    while ddict['iter_train'] > 0:
        ddict['iter_train'] -= 1
        iter_no += 1
        print'\n\t***iter_train:%d***\n' % iter_no
        print datetime.now()
        start = time.time()
        datafile = open(train_file, 'r')
        batch_no = 0
        while True:
            batch_no += 1
            # chia du lieu thanh cac minibatch
            (word1ids, word2ids, stop) = utilities.read_minibatch_list_frequencies_gen_biterm(datafile,
                                                                                              ddict['batch_size'])

            if stop == 0 or len(word1ids) > (ddict['batch_size'] / 2):
                print'\t\t---num_minibatch:%d---' % batch_no
                # training tung minibatch
                (time_e, time_m, phi, theta) = online_obtm.fitMiniBatch(word1ids, word2ids)
                if batch_no % 50 == 0:
                    # tinh do do perplexities
                    (LD2, ld2_list) = utilities.compute_perplexities_vb(phi, ddict['alpha'],
                                                                        ddict['eta'], ddict['iter_infer'],
                                                                        corpusids_part1,
                                                                        corpuscts_part1, corpusids_part2,
                                                                        corpuscts_part2)
                    # search top of each topics
                    list_tops = utilities.list_top(phi, tops)
                    # list_tops = []
                    # write files
                    # time_e = 0
                    # time_m = 0
                    # ghi file
                    utilities.write_file(iter_no, batch_no, phi, theta, time_e, time_m,
                                         model_folder, LD2, ld2_list, list_tops, tops)
            else:
                break
        datafile.close()
    # write final model to file
    file_name = '%s/beta_final.dat' % model_folder
    utilities.write_topic_distributions(phi, file_name)
    # finish
    print 'done!!!'
    print datetime.now()
    end1 = time.time()
    write_time(0, 0, end1 - start, end1 - start, model_folder)


if __name__ == '__main__':
    main()
