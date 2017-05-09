import csv

import matplotlib.pyplot as plt

from solvers import run_framework

cfg = {
    'population_size': 50,
    'selection': 'tournament',
    'crossover': 'pmx',
    'mutation': 'scramble',
    'iters': 100,
    'ffs': 3,
    'input_file': 'graphs/30.txt',
    'csv': 'stats.csv',
}

result = run_framework(
    loggers='',
    population_size=cfg['population_size'],
    selection=cfg['selection'],
    crossover=cfg['crossover'],
    mutation=cfg['mutation'],
    iters=cfg['iters'],
    ffs=cfg['ffs'],
    input_file=cfg['input_file'],
    out_csv_file=cfg['csv'])

x = []
y = []
with open(cfg['csv'], 'rb') as csvfile:
    plots = csv.DictReader(csvfile, delimiter=',', )
    for row in plots:
        x.append(int(row['iter_no']))
        y.append(float(row['max_saved']))

plt.plot(x, y, label=cfg['input_file'])
plt.xlabel('iteration')
plt.ylabel('Saved %')
plt.legend()
plt.show()
