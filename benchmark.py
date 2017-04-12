#!/usr/bin/env python

import itertools
import logging
from generate import load_graph
from solvers import simple_genetic_crossover, AlgoIn


def benchmark(algorithm, test_configurations, iterations=1, header=True):
    """

    :param algorithm: function taking 2 arguments: 1. graph 2. nodes where fire starts and returning best solution
    :param test_configuration: list of tuples (vertex_no, graph_density, ffs_per_step, algo_iters)
    :param iterations: how many times whole algorithm will be repeated with identical parameters
        average value & relative stddev value'll be reported
    :return:
    """
    f = "{:>8} {:>8} {:>8} {:>8} {:>8} {:>8} {:>8}"
    if header:
        print f.format("#VERTEX", "DENSITY", "ORIGINS", "FFSSTEP", "ITERS", "SAVED", "SAVED_FF")

    for vertex_no, density, ffs_per_step, algo_iters in test_configurations:
        def _print_result(score):
            print f.format(vertex_no, density, len(sn), ffs_per_step, algo_iters,
                           score.perc_saved_nodes, score.perc_saved_occupied_by_ff)

        g = load_graph(vertex_no, density)
        sn = map(lambda v: v.id, g.get_starting_nodes())

        for i in xrange(iterations):
            solution, score = algorithm(AlgoIn(g, sn, iter_no=algo_iters, ffs_per_step=ffs_per_step))
            _print_result(score)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)

    V_NO = [10, 25, 50]
    DENSITIES = [0.1, 0.5, 0.9]
    ALGO_ITERS = [5, 50, 100]
    FFS_PER_STEP = [1, 3, 5]

    confs = itertools.product(V_NO, DENSITIES, FFS_PER_STEP, ALGO_ITERS)

    benchmark(simple_genetic_crossover, confs, 5)
