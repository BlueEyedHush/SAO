import csv

import matplotlib.pyplot as plt

from solvers import run_framework

population_sizes = [10, 20, 50]
selection_ops = ['tournament', 'roulette', 'rank']
crossover_ops = ['cycle', 'injection', 'multi_injection', 'pmx', 'single_pmx']
mutation_ops = ['adjacent_swap', 'insertion', 'inversion', 'slide', 'random_swap', 'scramble', 'single_swap']

config_template = {
    'iters': 5000,
    'ffs': 3,
    'input_file': '80_035_2',
}

configs = list()
# generate configs with all combination of defined operators and population sizes
for ps in population_sizes:
    for so in selection_ops:
        for co in crossover_ops:
            for mo in mutation_ops:
                config = {
                    'population_size': ps,
                    'selection': so,
                    'crossover': co,
                    'mutation': mo,
                    'iters': 500,
                    'ffs': 3,
                    'input_file': '80_035_2',
                    'input_file_path': 'graphs/80_035_2.rgraph'
                }
                configs.append(config)

for cfg in configs:
    csv_file = "results/{}_{}_{}_{}_{}.csv".format(cfg['population_size'], cfg['selection'], cfg['crossover'],
                                                   cfg['mutation'], cfg['input_file'])
    print "Processing {}...".format(csv_file)
    result = run_framework(
        loggers='',
        population_size=cfg['population_size'],
        selection=cfg['selection'],
        crossover=cfg['crossover'],
        mutation=cfg['mutation'],
        iters=cfg['iters'],
        ffs=cfg['ffs'],
        input_file=cfg['input_file_path'],
        out_csv_file=csv_file)

# TODO: plots part should be moved somewhere else now
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
