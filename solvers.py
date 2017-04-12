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
        'ffs_per_step': 1,
        'vis': False,
        'show_score_every': None,  # don't show
    }


class AlgoScore():
    def __init__(self, perc_saved_nodes, perc_saved_occupied_by_ff):
        self.perc_saved_nodes = perc_saved_nodes
        self.perc_saved_occupied_by_ff = perc_saved_occupied_by_ff

    def __str__(self):
        return "Saved {} ({} occupied by FFs)".format(self.perc_saved_nodes, self.perc_saved_occupied_by_ff)


class AlgoIn():
    def __init__(self,
                 G,
                 init_nodes,
                 vis=defaults()["vis"],
                 iter_no=defaults()["algo_iter_no"],
                 ffs_per_step=defaults()["ffs_per_step"],
                 show_score_every=defaults()["show_score_every"]):
        self.G = G
        self.init_nodes = init_nodes
        self.vis = vis
        self.iter_no = iter_no
        self.ffs_per_step = ffs_per_step
        self.show_score_every = show_score_every


def _offer_visualization(G, transitions, solution, score, comment=""):
    if comment:
        print "New solution ({}), score: {}".format(comment, score)
    print "Show visualization? [y/N]: "
    if stdin.readline().strip().startswith("y"):
        visualize_simulation(G, transitions, solution)


def simple_genetic_crossover(params):
    G = params.G

    population_size = 4
    crossover_count = max(int(population_size * 0.5),
                          1)  # split point - how many firefighters are taken from 1st parent, how many from the 2nd
    mutation_count = 1
    crossover_point = 0.5

    if max(crossover_count + 1, mutation_count) > population_size:
        raise Exception("population_size must be >= crossover_count+1 && >= mutation_count")

    def process_new_solution(solution, comment=""):
        transitions, solution_score = simulation(G, solution, params.init_nodes, params.ffs_per_step)
        score = AlgoScore(perc_saved_nodes=float(solution_score.nodes_saved) / len(G.get_nodes()),
                          perc_saved_occupied_by_ff=float(solution_score.nodes_occupied_by_ff) / len(G.get_nodes()))
        if params.vis:
            _offer_visualization(G, transitions, solution, score, comment)
        return score

    # list of 2-tuples (solution, score)
    curr_solutions = []

    def new_solution_by_shuffling(base_sol, comment=""):
        solution = list(base_sol)
        random.shuffle(solution)
        score = process_new_solution(solution, comment)
        return solution, score

    # sort list by scores desc
    def sort_by_score(solutions):
        sorted(solutions, key=lambda (sol, score): score.perc_saved_nodes)

    # build initial solutions
    for i in range(0, population_size):
        solution, score = new_solution_by_shuffling(G.get_nodes(), "initial solution")
        curr_solutions.append((solution, score))

    sort_by_score(curr_solutions)

    for i in range(0, params.iter_no):
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

            score = process_new_solution(child, "crossover result")
            curr_solutions.append((child, score))

        # mutate some individuals
        fittest = curr_solutions[0:mutation_count]
        for sol, score in fittest:
            new_sol, new_score = new_solution_by_shuffling(sol, "mutation result")
            curr_solutions.append((new_sol, new_score))

        # resort
        sort_by_score(curr_solutions)

        # keep only population_size of the strongest
        curr_solutions = curr_solutions[0:population_size]

        if params.show_score_every is not None and i % params.show_score_every == 0:
            print "Scores after iteration {}: {}".format(i, map(lambda (_, score): str(score), curr_solutions))

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
                        default=defaults()['vis'])

    args = parser.parse_args()

    g = load_graph(args.vertices, args.density, args.starting_vertices)
    solver_func = solvers[args.algorithm]
    solver_func(AlgoIn(g,
                       map(lambda v: int(v.id), g.get_starting_nodes()),
                       args.visualization,
                       args.iters,
                       args.ffs,
                       show_score_every=1))
