#!/usr/bin/env python

import os, sys, logging, itertools
from generate import load_graph
from solvers import simple_genetic_crossover

def benchmark(algorithm, test_configurations):
    '''

    :param algorithm: function taking 2 arguments: 1. graph 2. nodes where fire starts and returning best solution
    :param test_configuration: list of tuples (vertex_no, density, iterations)
    :return:
    '''

    for vertex_no, density, iterations in test_configurations:
        g = load_graph(vertex_no, density)
        sn = map(lambda v: int(v.id), g.get_starting_nodes())

        print u"VERTEX_NO = {}, DENSITY = {}, ITERATIONS = {}, STARTING_NODES = {}".format(vertex_no, density, iterations, sn)
        for i in xrange(iterations):
            solution, score = algorithm(g, sn)
            print score

if __name__ == "__main__":
    logging.basicConfig(level = logging.WARN)

    V_NO = [10, 25, 50]
    DENSITIES = [0.1, 0.3, 0.5, 0.7, 0.9]
    ITERS = [5]

    confs = itertools.product(V_NO, DENSITIES, ITERS)

    benchmark(simple_genetic_crossover, confs)
