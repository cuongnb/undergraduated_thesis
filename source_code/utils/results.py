import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math as math
from common import utilities
import os

styles = ['k', 'r', 'g', 'b', 'y', 'r-.', 'g-.', 'b-.', 'y-.', 'r--', 'g--', 'b--', 'y--', 'r:', 'g:', 'b:', 'y:']


def read_perflexity_dataframe(model_folder):
    print model_folder
    try:
        # perflexity_df = pd.read_csv(
        #     model_folder + '/perplexities_pairs.csv', header=-1,
        #     names=['perflexity1', 'perflexity2', 'perflexity3',
        #            'perflexity4', 'perflexity5', 'none'],
        #     usecols=['perflexity1', 'perflexity2', 'perflexity3', 'perflexity4', 'perflexity5'])
        perflexity_df = pd.read_csv(
            model_folder + '/perplexities_pairs.csv', header=-1,
            names=['average_perflexity', 'none'],
            usecols=['average_perflexity'])

        time = pd.read_csv(model_folder + '/time.csv', header=-1,
                           names=['loop', 'estep', 'mstep', 'total', 'none'],
                           usecols=['estep', 'mstep', 'total'])
        time_values = time.total.values
        total_time = 0
        total_time_list = []
        for i in time_values:
            total_time += i
            total_time_list.append(np.log(total_time / 3600.0))
        perflexity_df['time'] = total_time_list
        perflexity_df['docs_seen'] = (perflexity_df.index + 1) * \
                                     utilities.read_setting(model_folder + '/setting.txt')['batch_size']
        if 'Drop' in model_folder:
            perflexity_df['average_num_update'] = (perflexity_df.index + 1) * \
                                                  (1 - utilities.read_setting(model_folder + '/setting.txt')[
                                                      'drop_rate'])
        else:
            perflexity_df['average_num_update'] = perflexity_df.index + 1
        # perflexity_df['average_perflexity'] = perflexity_df[['perflexity1', 'perflexity2',
        #                                                      'perflexity3', 'perflexity4', 'perflexity5']].mean(1)
        return perflexity_df
    except Exception:
        return None


def read_all_perflexity_dataframe(model_folder_list):
    # all_perflexity_dfs = dict()
    all_perflexity_dfs = list()
    for model_folder in model_folder_list:
        df = read_perflexity_dataframe(model_folder)
        # if df is not None:
        all_perflexity_dfs.append(df)
    return all_perflexity_dfs


def plot_all_perflexity_against_docs(model_folder_list, title, start_index=0, step=1):
    # styles = ['r:', 'g:', 'b:', 'y:', 'r-.', 'g-.', 'b-.', 'y-.', 'r--', 'g--', 'b--', 'y--', 'r', 'g', 'b', 'y'
    fig = plt.figure(1)
    all_perflexity_dfs = read_all_perflexity_dataframe(model_folder_list)

    max_pers = [df.max()['average_perflexity'] for df in all_perflexity_dfs]
    max_per = max(max_pers)
    max_per = int(max_per * 2) / 2.
    min_per = max_per - 3.

    axes = plt.gca()
    axes.set_ylim([min_per, max_per])

    for idx, model in enumerate(model_folder_list):
        df = all_perflexity_dfs[idx]
        if df is not None:
            temp = df[start_index::step].set_index('docs_seen')['average_perflexity']
            label = os.path.split(model)[-1]
            plt.plot(temp.index, temp.values, styles[idx], label=label)
    plt.title(title)
    plt.xlabel('Documents seen')
    plt.ylabel('Log Predictive Probability')
    plt.legend(loc='lower right', prop={'size': 10})
    # plt.show()
    return fig


def plot_all_perflexity_against_time(model_folder_list, title, start_index=0, step=1):
    # styles = ['r:', 'g:', 'b:', 'y:', 'r-.', 'g-.', 'b-.', 'y-.', 'r--', 'g--', 'b--', 'y--', 'r', 'g', 'b', 'y']
    fig = plt.figure(1)
    all_perflexity_dfs = read_all_perflexity_dataframe(model_folder_list)
    max_pers = [df.max()['average_perflexity'] for df in all_perflexity_dfs]
    max_per = max(max_pers)
    max_per = int(max_per * 2) / 2.
    min_per = max_per - 3.
    axes = plt.gca()
    axes.set_ylim([min_per, max_per])
    for idx, model in enumerate(model_folder_list):
        df = all_perflexity_dfs[idx]
        if df is not None:
            temp = df[start_index::step].set_index('time')['average_perflexity']
            label = os.path.split(model)[-1]
            plt.plot(temp.index, temp.values, styles[idx], label=label)
    plt.title(title)
    plt.xlabel('Learning time (log scale)')
    plt.ylabel('Log Predictive Probability')
    plt.legend(loc='lower right', prop={'size': 10})
    plt.show()
    # return fig


def plot_all_perflexity_against_average_num_update(model_folder_list, title, start_index=0, step=1):
    # styles = ['r:', 'g:', 'b:', 'y:', 'r-.', 'g-.', 'b-.', 'y-.', 'r--', 'g--', 'b--', 'y--', 'r', 'g', 'b', 'y']
    fig = plt.figure(1)
    all_perflexity_dfs = read_all_perflexity_data(model_folder_list)

    max_pers = [df.max()['average_perflexity'] for df in all_perflexity_dfs]
    max_per = max(max_pers)
    max_per = int(max_per * 2) / 2.
    min_per = max_per - 3.

    axes = plt.gca()
    axes.set_ylim([min_per, max_per])

    for idx, model in enumerate(model_folder_list):
        df = all_perflexity_dfs[idx]
        if df is not None:
            temp = df[start_index::step].set_index('average_num_update')['average_perflexity']
            label = os.path.split(model)[-1]
            plt.plot(temp.index, temp.values, styles[idx], label=label)
    plt.title(title)
    plt.xlabel('Average number of update per lambda')
    plt.ylabel('Log Predictive Probability')
    plt.legend(loc='lower right', prop={'size': 10})
    # plt.show()
    return fig


def get_length_all_perflexity_dfs(all_perflexity_dfs):
    all_lengths = dict()
    for model in all_perflexity_dfs.keys():
        all_lengths[model] = len(all_perflexity_dfs[model].index)


def read_all_perflexity_data(path):
    # all_perflexity_dfs = dict()
    all_perflexity_dfs = list()
    # path = '/home/cuongnb/PycharmProjects/online_vb_obtm/result/gibb_models/100tp0'
    num_folder = 10
    model_folder_list = list()
    for i in range(num_folder):
        model_folder_list.append(path + str(i))
    for model_folder in model_folder_list:
        df = read_perflexity_dataframe(model_folder)
        # # if df is not None:
        all_perflexity_dfs.append(df)
        print df
    return all_perflexity_dfs


if __name__ == '__main__':
    path = '/home/cuongnb/PycharmProjects/online_vb_obtm/result/vb_twitter/100_0'
    read_all_perflexity_data(path)
    plot_all_perflexity_against_average_num_update(path, 'vb_obtm', start_index=0, step=1)
