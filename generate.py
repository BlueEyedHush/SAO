#!/usr/bin/env python

import argparse
import os
import random

from itertools import combinations


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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', help='output file')
    parser.add_argument('--vertices', help='number of vertices in graph', type=int)
    parser.add_argument('--density', help='edges density; float in range [0..1]', type=float)
    parser.add_argument('--starting_vertices', help='number of starting vertices', type=int)
    args = parser.parse_args()

    defaults = {
        'output_file': os.path.join('graphs', 'random.txt'),
        'vertices_num': 10,
        'density': 0.2,
        'starting_vertices_num': 1
    }

    output_file = args.out or defaults['output_file']
    vertices_num = args.vertices or defaults['vertices_num']
    density = args.density or defaults['density']
    starting_vertices_num = args.starting_vertices or defaults['starting_vertices_num']

    generate_file_data(out_file=output_file, vertices_num=vertices_num, density=density,
                       starting_vertices_num=starting_vertices_num)
