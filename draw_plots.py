from features import VISUALIZATION_PLOTTING

if VISUALIZATION_PLOTTING:
    import matplotlib.pyplot as plt

import os.path
import numpy as np
from evaluate import build_cfg_filepath, generate_configs, graph_path_to_filename


def avg(values):
    return sum(values) / float(len(values))


def plot_title(config, groupped_by):
    order = ["population_size", "selection", "crossover", "mutation", "input_file"]
    title = ""
    for i in order:
        if i != "input_file":
            if i == groupped_by:
                title += i.upper()
            else:
                title += str(config[i])
        else:
            if i == groupped_by:
                title += "GRAPH"
            else:
                title += graph_path_to_filename(config["input_file"])
        title += "_"
    return title[:-1] if title else title


def plot_path(plot_name, base_dir):
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    return os.path.join(base_dir, plot_name + ".png")


def box_plot_builder(data_and_configs, groupped_by, y_limits, add_conf={}):
    iter_gap = add_conf.get("iter_gap", 100)
    y_min, y_max = y_limits

    plt_height = len(configs) * 8
    fig = plt.figure(figsize=(7, plt_height))
    fig.set_dpi(120)

    for i, (matrix, config) in enumerate(data_and_configs):
        ax = fig.add_subplot(len(data_and_configs), 1, i + 1)
        ax.set_ylim((y_min, y_max))

        xs = range(0, matrix.shape[0], iter_gap)
        ys = matrix[0:-1:iter_gap].tolist()

        ax.boxplot(ys, labels=xs)
        ax.set_xlabel('Iteration')
        ax.set_ylabel('Saved %')
        ax.set_title(config[groupped_by])

    plt_title = plot_title(data_and_configs[0][1], groupped_by)

    fig.tight_layout()
    size_for_fig_title = 0.72
    fig.subplots_adjust(top=1.0 - size_for_fig_title / plt_height)
    fig.suptitle(plt_title)

    return fig, plt_title


def line_plot_builder(data_and_configs, groupped_by, y_limits, add_conf={}):
    y_min, y_max = y_limits

    fig = plt.figure(figsize=(8, 6))
    fig.set_dpi(120)
    ax = fig.add_subplot(1, 1, 1)
    ax.set_ylim((y_min, y_max))

    # labels = []
    for i, (matrix, config) in enumerate(data_and_configs):
        label = config[groupped_by]
        ys = []
        xs = []
        for i in xrange(matrix.shape[0]):
            ys.append(matrix[i].mean())
            xs.append(i + 1)

        ax.plot(xs, ys, label=label)

    plt_title = plot_title(data_and_configs[0][1], groupped_by)
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Saved %')
    ax.legend()
    fig.suptitle(plt_title)

    return fig, plt_title


def draw_plots(configs, plot_builder, groupped_by, csv_dir, plot_png_out, add_conf={}):
    def _load_csv_for(config):
        csv_file = build_cfg_filepath(config, csv_dir)

        if os.path.isfile(csv_file):
            data = np.genfromtxt(csv_file, delimiter=',')
            return data
        else:
            return None

    y_min = float("Inf")
    y_max = -float("Inf")
    for config_set in configs:
        for config in config_set:
            matrix = _load_csv_for(config)
            new_min = matrix.min()
            new_max = matrix.max()
            matrix = None

            if new_max > y_max:
                y_max = new_max
            if new_min < y_min:
                y_min = new_min

    for i, config_set in enumerate(configs):
        print "Drawing plot {} out of {}".format(i + 1, len(configs))

        # take only those for which we have data
        data_and_configs = filter(lambda (d, c): d is not None, map(lambda c: (_load_csv_for(c), c), config_set))

        plt.clf()
        fig, title = plot_builder(data_and_configs, groupped_by, (y_min, y_max), add_conf)

        fig.savefig(plot_path(title, plot_png_out))
        plt.close(fig)


def compare_all():
    cd = "results/80_035_2/csv (copy)/"
    po = "results/80_035_2/plots/"

    for gb in ["mutation", "population_size", "crossover", "selection"]:
        configs = generate_configs({}, group_by=gb)
        draw_plots(configs, line_plot_builder, groupped_by=gb, csv_dir=cd, plot_png_out=po + "l_{}".format(gb))

if __name__ == '__main__':
    compare_all()
