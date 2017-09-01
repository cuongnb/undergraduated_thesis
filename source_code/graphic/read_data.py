import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

styles = ['k', 'r', 'g', 'b', 'y', 'c', 'r-.', 'g-.', 'b-.', 'y-.', 'r--', 'g--', 'b--', 'y--', 'r:', 'g:', 'b:', 'y:']
x = np.array([0, 1, 3, 5, 6, 9])


def read_perflexity_dataframe(model_folder):
    try:
        perflexity_df = pd.read_csv(model_folder + '/perplexities_pairs.csv', header=-1,
                                    names=['average_perflexity', 'none'], usecols=['average_perflexity'])
        return perflexity_df
    except Exception:
        None


def read_NPMI_dataframe(model_folder):
    try:
        # csv.reader(csvfile, delimiter=',', quotechar='|')
        read_csv = pd.read_csv(model_folder + '/mean-NPMI-coherence-top20.csv', delimiter=',')
        per_file_name = '%s/mean-NPMI-coherence-top20_reformat.csv' % (model_folder)
        f = open(per_file_name, 'w')
        for n in read_csv:
            if not 'Unnamed:' in n:
                f.write('%f,\n' % float(n))
        f.close()

        perflexity_df = pd.read_csv(
            model_folder + '/mean-NPMI-coherence-top20_reformat.csv', header=-1, names=['average_npmi', 'none'],
            usecols=['average_npmi'])
        print 'coc'
        return perflexity_df
    except Exception:
        print 'fail'
        None


def read_all_perflexity_dataframe(path):
    # all_perflexity_dfs = dict()
    all_perflexity_dfs = list()
    # path = '/home/cuongnb/PycharmProjects/online_vb_obtm/result/gibb_twitter/100tp0'
    # num_folder = 10
    model_folder_list = list()
    for i in x:
        model_folder_list.append(path + str(i))
    for model_folder in model_folder_list:
        df = read_perflexity_dataframe(model_folder)
        # # if df is not None:
        all_perflexity_dfs.append(df)
        print df
    return all_perflexity_dfs


def read_all_NPMI_dataframe(path):
    # all_perflexity_dfs = dict()
    all_perflexity_dfs = list()
    # path = '/home/cuongnb/PycharmProjects/online_vb_obtm/result/gibb_twitter/100tp0'
    # num_folder = 10
    model_folder_list = list()
    for i in x:
        model_folder_list.append(path + str(i))
    for model_folder in model_folder_list:
        df = read_NPMI_dataframe(model_folder)
        # # if df is not None:
        all_perflexity_dfs.append(df)
        print df
    return all_perflexity_dfs




def read_perplexity_origin_vn_gibb(K):
    # all_perflexity_dfs = dict()
    all_perflexity_dfs = list()
    path_gibb = '/home/cuongnb/PycharmProjects/online_vb_obtm/result/gibbs_nyt/' + str(K) + 'tp00'
    path_vb = '/home/cuongnb/PycharmProjects/online_vb_obtm/result/vb_nyt/' + str(K) + '_00'
    model_folder_list = list()
    model_folder_list.append(path_gibb)
    model_folder_list.append(path_vb)
    # print 'model_folder_list' + str(model_folder_list)
    for model_folder in model_folder_list:
        df = read_perflexity_dataframe(model_folder)
        # # if df is not None:
        all_perflexity_dfs.append(df)
        print df
    return all_perflexity_dfs


def read_origin_NPMI_dataframe(K):
    # all_perflexity_dfs = dict()
    all_perflexity_dfs = list()
    path_gibb = '/home/cuongnb/PycharmProjects/online_vb_obtm/result/gibbs_yahoo/' + str(K) + 'tp00'
    path_vb = '/home/cuongnb/PycharmProjects/online_vb_obtm/result/vb_yahoo/' + str(K) + '_00'
    model_folder_list = list()
    model_folder_list.append(path_gibb)
    model_folder_list.append(path_vb)
    for model_folder in model_folder_list:
        df = read_NPMI_dataframe(model_folder)
        # # if df is not None:
        all_perflexity_dfs.append(df)
        print df
    return all_perflexity_dfs


def plot_origin_perflexity_against_time(title, num_topics):
    # styles = ['r:', 'g:', 'b:', 'y:', 'r-.', 'g-.', 'b-.', 'y-.', 'r--', 'g--', 'b--', 'y--', 'r', 'g', 'b', 'y']
    fig = plt.figure(1)
    all_perflexity_dfs = read_perplexity_origin_vn_gibb(num_topics)
    max_pers = [df.max()['average_perflexity'] for df in all_perflexity_dfs]
    max_per = max(max_pers)
    max_per = int(max_per * 2) / 2. - 0.15
    min_per = max_per - 3.
    axes = plt.gca()
    axes.set_ylim([min_per, max_per])
    # for idx, model in enumerate(model_folder_list):
    #     df = all_perflexity_dfs[idx]
    #     if df is not None:
    #         temp = df[start_index::step].set_index('time')['average_perflexity']
    #         label = os.path.split(model)[-1]
    #         plt.plot(temp.index, temp.values, styles[idx], label=label)

    print '-------------------------------------------------'
    for idx in range(len(all_perflexity_dfs)):
        df = all_perflexity_dfs[idx]
        if df is not None:
            plt.plot(df, styles[idx])

    plt.title(title)
    plt.xlabel('Documents seem (x10^6)')
    plt.ylabel('Log Predictive Probability')
    # plt.legend(loc='lower right', prop={'size': 2})
    # plt.show()
    return fig


def plot_origin_npmi_against_time(title, num_topics):
    # styles = ['r:', 'g:', 'b:', 'y:', 'r-.', 'g-.', 'b-.', 'y-.', 'r--', 'g--', 'b--', 'y--', 'r', 'g', 'b', 'y']
    fig = plt.figure(1)
    all_npmi_dfs = read_origin_NPMI_dataframe(num_topics)
    max_pers = [df.max()['average_npmi'] for df in all_npmi_dfs]
    max_per = max(max_pers)
    max_per = int(max_per * 2) / 2 + 3.
    min_per = max_per - 10.
    axes = plt.gca()
    axes.set_ylim([min_per, max_per])
    # for idx, model in enumerate(model_folder_list):
    #     df = all_perflexity_dfs[idx]
    #     if df is not None:
    #         temp = df[start_index::step].set_index('time')['average_perflexity']
    #         label = os.path.split(model)[-1]
    #         plt.plot(temp.index, temp.values, styles[idx], label=label)

    for idx in range(len(all_npmi_dfs)):
        df = all_npmi_dfs[idx]
        if df is not None:
            plt.plot(df, styles[idx])

    plt.title(title)
    plt.xlabel('number minibatch(x50)')
    plt.ylabel('Log Predictive Probability')
    # plt.legend(loc='lower right', prop={'size': 10})
    # plt.show()
    return fig
def plot_all_perflexity_against_time(model_folder_list, title, start_index=0, step=1):
    # styles = ['r:', 'g:', 'b:', 'y:', 'r-.', 'g-.', 'b-.', 'y-.', 'r--', 'g--', 'b--', 'y--', 'r', 'g', 'b', 'y']
    fig = plt.figure(1)
    all_perflexity_dfs = read_all_perflexity_dataframe(model_folder_list)
    max_pers = [df.max()['average_perflexity'] for df in all_perflexity_dfs]
    max_per = max(max_pers)
    # max_per = int(max_per * 2) / 2. - 0.4
    # min_per = max_per - 0.2

    max_per = int(max_per * 2) / 2. - 0.2
    min_per = max_per - 0.4

    axes = plt.gca()
    axes.set_ylim([min_per, max_per])
    # for idx, model in enumerate(model_folder_list):
    #     df = all_perflexity_dfs[idx]
    #     if df is not None:
    #         temp = df[start_index::step].set_index('time')['average_perflexity']
    #         label = os.path.split(model)[-1]
    #         plt.plot(temp.index, temp.values, styles[idx], label=label)

    for idx in range(len(all_perflexity_dfs)):
        df = all_perflexity_dfs[idx]
        if df is not None:
            plt.plot(df, styles[idx])

    # plt.title(title)
    plt.xlabel('number minibatch(x50)')
    plt.ylabel('Log Predictive Probability')
    plt.legend(loc='lower right', prop={'size': 10})
    # plt.show()
    return fig




def plot_all_npmi_against_time(model_folder_list, title, start_index=0, step=1):
    # styles = ['r:', 'g:', 'b:', 'y:', 'r-.', 'g-.', 'b-.', 'y-.', 'r--', 'g--', 'b--', 'y--', 'r', 'g', 'b', 'y']
    fig = plt.figure(1)
    all_npmi_dfs = read_all_NPMI_dataframe(model_folder_list)
    max_pers = [df.max()['average_npmi'] for df in all_npmi_dfs]
    max_per = max(max_pers)
    # max_per = int(max_per * 2) / 2 + 4.
    # min_per = max_per - 25.

    max_per = int(max_per * 2) / 2 +4
    min_per = max_per - 14.

    axes = plt.gca()
    axes.set_ylim([min_per, max_per])
    # for idx, model in enumerate(model_folder_list):
    #     df = all_perflexity_dfs[idx]
    #     if df is not None:
    #         temp = df[start_index::step].set_index('time')['average_perflexity']
    #         label = os.path.split(model)[-1]
    #         plt.plot(temp.index, temp.values, styles[idx], label=label)

    for idx in range(len(all_npmi_dfs)):
        df = all_npmi_dfs[idx]
        if df is not None:
            plt.plot(df, styles[idx])

    # plt.title(title)
    plt.xlabel('number minibatch (x10)')
    plt.ylabel('Normalized Pointwise Mutual Information')
    plt.legend(loc='lower right', prop={'size': 10})
    # plt.show()
    return fig


if __name__ == '__main__':
    topics = list()
    topics.append(50)
    # topics.append(100)
    # topics.append(150)
    # topics.append(200)
    types = list()
    # types.append('Per')
    types.append('NPMI')
    output = '/home/cuongnb/PycharmProjects/online_vb_obtm/coc/'

    for K in topics:
        for type_learn in types:
            # path1 = '/home/cuongnb/PycharmProjects/online_vb_obtm/result/gibb_twitter/' + str(K) + 'tp0'
            path2 = '/home/cuongnb/PycharmProjects/online_vb_obtm/result/vb_twitter/' + str(K) + '_0'
            output1 = output + 'twitter' + type_learn + str(K) + 'gibb'
            output2 = output + 'twitter' + type_learn + str(K) + 'vb'
            output_origin = output + 'origin' + 'GibbVb' + str(K) + type_learn
            path = list()
            # path.append(path1)
            path.append(path2)
            dir_file_ouput = list()
            dir_file_ouput.append(output1)
            dir_file_ouput.append(output2)
            for n in range(len(path)):
                if type_learn == 'NPMI':
                    fig = plot_all_npmi_against_time(path[n], type_learn + str(K), start_index=0, step=1)
                else:
                    fig = plot_all_perflexity_against_time(path[n], type_learn + str(K), start_index=0, step=1)
                fig.savefig(dir_file_ouput[1])
                # if type_learn == 'Per':
                #     fig_origin = plot_origin_perflexity_against_time('origin' + str(K), K)
                # else:
                #     fig_origin = plot_origin_npmi_against_time('origin' + str(K), K)
                # fig_origin.savefig(output_origin)
