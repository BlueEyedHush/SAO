#!/usr/bin/env python

import argparse
import os, sys
import random

from graph import Graph
from itertools import combinations

SCRIPT_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
GRAPHS_DIR = "graphs/"
STARTING_VERTICES = 1

def generate_edges(vertices_num, density):
    # TODO: describe what it does, in particular the density
    max_edges = (vertices_num * (vertices_num - 1)) / 2
    edges_num = int(max_edges * density)

    all_possible_edges = combinations(xrange(vertices_num), 2)

    edges = random.sample(list(all_possible_edges), edges_num)
    return edges_num, edges


def generate_file_data(out_file, vertices_num, density, starting_vertices_num):
    edges_num, edges = generate_edges(vertices_num, density)
    starting_vertices = random.sample(xrange(vertices_num), starting_vertices_num)

    with open(out_file, 'w') as f:
        f.write("{} {}\n".format(vertices_num, edges_num))
        for sv in starting_vertices:
            f.write("{} ".format(sv))
        f.write('\n')
        for e in edges:
            f.write("{} {}\n".format(*e))

def _get_script_dir():
    relative = ""
    if __file__:
        # when loaded as module
        relative = __file__
    else:
        # when run as script
        relative = sys.argv[0]
    return os.path.dirname(os.path.realpath(relative))

def _generate_graph_file_name(vertex_no, density, starting_vertices_no):
    return u"{}_{}_{}.rgraph".format(vertex_no, density, starting_vertices_no)

def load_graph(vertex_no, density, starting_vertices_no = STARTING_VERTICES):
    fname = _generate_graph_file_name(vertex_no, density, starting_vertices_no)
    graph_file_path = os.path.join(_get_script_dir(), GRAPHS_DIR, fname)

    if not os.path.isfile(graph_file_path):
        generate_file_data(graph_file_path, vertex_no, density, starting_vertices_no)

    g = Graph()
    g.from_file(graph_file_path)

    return g

def configure_graph_generation_cli(parser):
    parser.add_argument('--vertices', help='number of vertices in graph', type=int, default=10)
    parser.add_argument('--density', help='edges density; float in range [0..1]', type=float, default=0.2)
    parser.add_argument('--starting_vertices', help='number of starting vertices', type=int, default=1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', help='output file', default=os.path.join('graphs', 'random.txt'))
    configure_graph_generation_cli(parser)
    args = parser.parse_args()

    generate_file_data(out_file=args.out,
                       vertices_num=args.vertices,
                       density=args.density,
                       starting_vertices_num=args.starting_vertices)
