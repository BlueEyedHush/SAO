import csv

import matplotlib.pyplot as plt

from solvers import run_framework


def prepare_configs(iters, ffs, graph_desc, input_file):
    population_sizes = [10, 20, 50]
    selection_ops = ['tournament', 'roulette', 'rank']
    crossover_ops = ['cycle', 'injection', 'multi_injection', 'pmx', 'single_pmx']
    mutation_ops = ['adjacent_swap', 'insertion', 'inversion', 'slide', 'random_swap', 'scramble', 'single_swap']

    # generate all possible combinations of defined operators and population size
    configs = list()
    for ps in population_sizes:
        for so in selection_ops:
            for co in crossover_ops:
                for mo in mutation_ops:
                    config = {
                        'population_size': ps,
                        'selection': so,
                        'crossover': co,
                        'mutation': mo,
                        'iters': iters,
                        'ffs': ffs,
                        'graph_desc': graph_desc,
                        'input_file': input_file,
                    }
                    configs.append(config)

    return configs


def calculate_results(configs):
    configs_num = len(configs)
    processed_config_num = 1
    for cfg in configs:
        csv_file = "results/{}_{}_{}_{}_{}.csv".format(cfg['population_size'], cfg['selection'], cfg['crossover'],
                                                       cfg['mutation'], cfg['graph_desc'])
        print "[{}/{}] Calculating {}...".format(processed_config_num, configs_num, csv_file)
        run_framework(
            loggers='',
            population_size=cfg['population_size'],
            selection=cfg['selection'],
            crossover=cfg['crossover'],
            mutation=cfg['mutation'],
            iters=cfg['iters'],
            ffs=cfg['ffs'],
            input_file=cfg['input_file'],
            out_csv_file=csv_file)

        processed_config_num += 1


def draw_plots(configs):
    # x = []
    # y = []
    #
    #     with open(csv_file, 'rb') as csvfile:
    #         plots = csv.DictReader(csvfile, delimiter=',', )
    #         for row in plots:
    #             x.append(int(row['iter_no']))
    #             y.append(float(row['max_saved']))
    #
    #     keys[size] = x
    #     values[size] = y
    #
    # for size in population_sizes:
    #     plt.plot(keys[size], values[size], label=size)
    #
    # plt.xlabel('Iteration')
    # plt.ylabel('Saved %')
    # plt.legend()
    # plt.show()

    pass


if __name__ == '__main__':
    iters = 500
    graph_desc = '80_035_2'
    input_file = 'graphs/80_035_2.rgraph'
    ffs = 3
    configs = prepare_configs(iters, ffs, graph_desc, input_file)
    calculate_results(configs)
