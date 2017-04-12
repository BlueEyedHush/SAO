import argparse
import logging
import random
from sys import stdin

from generate import load_graph
from simulation import simulation
from visualize import visualize_simulation


def defaults():
    return {
        'algo_iter_no': 3,
        'ffs_per_step': 1
    }


def log_solution(sol, score):
    logging.info("solution: {}, score: {} /smaller-better/".format(sol, score))


def _offer_visualization(G, transitions, solution, score, comment=""):
    if comment:
        print "New solution ({}), score: {}".format(comment, score)
    print "Show visualization? [y/N]: "
    if stdin.readline().strip().startswith("y"):
        visualize_simulation(G, transitions, solution)


def simple_genetic_crossover(G, init_nodes, vis=False, iter_no=defaults()['algo_iter_no'],
                             ffs_per_step=defaults()['ffs_per_step'], show_score_every=None):
    population_size = 4
    crossover_count = max(int(population_size * 0.5),
                          1)  # split point - how many firefighters are taken from 1st parent, how many from the 2nd
    mutation_count = 1
    crossover_point = 0.5

    if max(crossover_count + 1, mutation_count) > population_size:
        raise Exception("population_size must be >= crossover_count+1 && >= mutation_count")

    def simulate(solution, comment=""):
        transitions, iterations, saved_nodes = simulation(G, solution, init_nodes, ffs_per_step)
        score = float(saved_nodes) / len(G.get_nodes())
        if vis:
            _offer_visualization(G, transitions, solution, score, comment)
        return score

    # list of 2-tuples (solution, score)
    curr_solutions = []

    def next_sol(base_sol, comment=""):
        solution = list(base_sol)
        random.shuffle(solution)
        score = simulate(solution, comment)
        log_solution(solution, score)
        return solution, score

    # build initial solutions
    for i in range(0, population_size):
        solution, score = next_sol(G.get_nodes(), "initial solution")
        curr_solutions.append((solution, score))

    # sort list by scores desc
    def sort_by_score(solutions):
        sorted(solutions, key=lambda (sol, score): score)

    sort_by_score(curr_solutions)

    for i in range(0, iter_no):
        logging.info("**** ITERATION {} ****".format(i))

        # crossover
        for j in range(0, crossover_count):
            parents = curr_solutions[j:j + 2]
            parent1 = parents[0][0]
            parent2 = parents[1][0]

            last_from_1st = max(int(len(parent1) * crossover_point), 1)
            first_part = parent1[0:last_from_1st + 1]
            second_part = filter(lambda x: x not in first_part, parent2)

            child = first_part + second_part

            par_len = len(parent1)
            child_len = len(child)
            if child_len != par_len:
                raise Exception("child has wrong size (child: {} parent: {})!".format(child, parent1))

            if len(child) != len(set(child)):
                raise Exception("duplicate entries in child genome!")

            score = simulate(child, "crossover result")
            logging.info(
                "crossing {} /score {}/ with {} /score {}/, got {} /score {}/".format(parents[0][0], parents[0][1],
                                                                                      parents[1][0], parents[1][1],
                                                                                      child, score))
            curr_solutions.append((child, score))

        # mutate some individuals
        fittest = curr_solutions[0:mutation_count]
        for sol, score in fittest:
            new_sol, new_score = next_sol(sol, "mutation result")
            logging.info(
                "mutated solution {} /score {}/ built from {} /score {}/".format(new_sol, new_score, sol, score))
            curr_solutions.append((new_sol, new_score))

        # resort
        sort_by_score(curr_solutions)

        # keep only population_size of the strongest
        curr_solutions = curr_solutions[0:population_size]

        if show_score_every is not None and i % show_score_every == 0:
            print "Scores after iteration {}: {}".format(i, map(lambda (_, score): score, curr_solutions))

    return curr_solutions[0]


solvers = {
    "simple_genetic_crossover": simple_genetic_crossover
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-a', '--algorithm',
                        help='algorithm name',
                        choices=['simple_genetic_crossover'],
                        default='simple_genetic_crossover')
    parser.add_argument('-d', '--density',
                        help='edges density; float in range [0..1]',
                        type=float,
                        default=0.2)
    parser.add_argument('-f', '--ffs',
                        help='number of firefighters per step',
                        type=int,
                        default=defaults()['ffs_per_step'])
    parser.add_argument('-i', '--iters',
                        help='number of algorithm iterations',
                        type=int,
                        default=defaults()['algo_iter_no'])
    parser.add_argument('-s', '--starting_vertices',
                        help='number of starting vertices',
                        type=int,
                        default=1)
    parser.add_argument('-v', '--vertices',
                        help='number of vertices in graph',
                        type=int,
                        default=10)
    parser.add_argument('-z', '--visualization',
                        help='enables visualization for solutions',
                        action='store_true',
                        default=False)

    args = parser.parse_args()

    logging.basicConfig(level=logging.WARN)

    g = load_graph(args.vertices, args.density, args.starting_vertices)
    solver_func = solvers[args.algorithm]
    solver_func(g, map(lambda v: int(v.id), g.get_starting_nodes()), vis=args.visualization, iter_no=args.iters,
                ffs_per_step=args.ffs, show_score_every=1)
