#!/usr/bin/env python

import os, sys, logging
from generate import generate_file_data
from graph import Graph
from solvers import simple_genetic_crossover

SCRIPT_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
GRAPHS_DIR = "graphs/"
STARTING_VERTICES = 1

def _get_script_dir():
    relative = ""
    if __file__:
        # when loaded as module
        relative = __file__
    else:
        # when run as script
        relative = sys.argv[0]
    return os.path.dirname(os.path.realpath(relative))

def _generate_graph_file_name(vertex_no, density):
    return u"{}_{}.graph".format(vertex_no, density)

def _load_graph(vertex_no, density):
    fname = _generate_graph_file_name(vertex_no, density)
    graph_file_path = os.path.join(_get_script_dir(), GRAPHS_DIR, fname)

    if not os.path.isfile(graph_file_path):
        generate_file_data(graph_file_path, vertex_no, density, STARTING_VERTICES)

    g = Graph()
    g.from_file(graph_file_path)

    return g


def benchmark(algorithm, test_configurations):
    '''

    :param algorithm: function taking 2 arguments: 1. graph 2. nodes where fire starts and returning best solution
    :param test_configuration: list of tuples (vertex_no, density, iterations)
    :return:
    '''

    for vertex_no, density, iterations in test_configurations:
        g = _load_graph(vertex_no, density)
        sn = map(lambda v: int(v.id), g.get_starting_nodes())

        print u"VERTEX_NO = {}, DENSITY = {}, ITERATIONS = {}, STARTING_NODES = {}".format(vertex_no, density, iterations, sn)
        for i in xrange(iterations):
            solution, score = algorithm(g, sn)
            print score

if __name__ == "__main__":
    logging.basicConfig(level = logging.WARN)
    benchmark(simple_genetic_crossover, [(10, 0.5, 5)])
