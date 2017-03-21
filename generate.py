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


def generate_file_data(out_file, vertices_num, density):
    edges_num, edges = generate_edges(vertices_num, density)

    with open(out_file, 'w') as f:
        f.write("{} {}\n".format(vertices_num, edges_num))
        for e in edges:
            f.write("{} {}\n".format(*e))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', help='output file')

    args = parser.parse_args()

    output_file = args.out
    if not output_file:
        output_file = os.path.join('graphs', 'random.txt')

    # print generate_edges(5, 0.2)
    generate_file_data(out_file=output_file, vertices_num=5, density=0.4)
