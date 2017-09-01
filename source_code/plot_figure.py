import sys, os, shutil
import logging
FORMAT = "%(levelname)s> In %(module)s.%(funcName)s line %(lineno)d at %(asctime)-s> %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)
from utils import results

all_dataset_dir = 'dataset'
# all_dataset = ['fullnyt', 'tweet', 'largepub']
all_dataset = ['nyt', 'twitter', 'yahoo']
all_modes = {'tp': 'topics', 'mw': 'mstep_words', 'td': 'topics_docs'}
drop_name = 'Drop'
model_folder_names = 'vb_twitter'
all_methods = ['OnlineVB', 'MLVB', 'OnlineOPE', 'MLOPE', 'OnlineFW', 'MLFW', 'OnlineCGS', 'OnlineCVB0']
out_file_types = ['_docs.png', '_time.png', '_updates.png']
starts = {'nyt' : 0, 'twitter': 0, 'yahoo' : 0}
step = 1
figure = 'figure/'


def plot_a_dataset_method_mode(dataset, method, mode):
    try:
        start = starts[dataset]
        # name
        out_name = method + all_modes[mode] + dataset
        out_files = [figure + out_name + out_file_type for out_file_type in out_file_types]
        title = ' '.join([method, drop_name, all_modes[mode], dataset])
        # method dir in this data set
        dataset_model_folder = os.path.join(all_dataset_dir, dataset, model_folder_names)

        all_method_name = os.listdir(dataset_model_folder)
        method_names = [x for x in all_method_name if method in x]
        origin_name = [x for x in method_names if drop_name not in x][0:1]
        method_names = [x for x in method_names if mode in x]
        method_names.sort()
        method_names = origin_name + method_names

        method_dirs = [os.path.join(dataset_model_folder, method_name) for method_name in method_names]
        if len(method_dirs) > 1:
            fig0 = results.plot_all_perflexity_against_docs(method_dirs, title, start, step)
            fig0.savefig(out_files[0])
            fig0.clear()
            del fig0
            fig1 = results.plot_all_perflexity_against_time(method_dirs, title, start, step)
            fig1.savefig(out_files[1])
            fig1.clear()
            fig2 = results.plot_all_perflexity_against_average_num_update(method_dirs, title, start, step)
            fig2.savefig(out_files[2])
            fig2.clear()
    except Exception as ex:
        logging.error(ex)


def plot_all():
    if not os.path.exists(figure):
        os.mkdir(figure)
    for dataset in all_dataset:
        for method in all_methods:
            for mode in all_modes:
                plot_a_dataset_method_mode(dataset, method, mode)


if __name__ == '__main__':
    plot_all()