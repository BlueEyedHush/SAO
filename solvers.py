
import random
import logging
import argparse
from generate import configure_graph_generation_cli, load_graph
from simulation import simulation
from visualize import visualize_simulation
from sys import stdin, argv

ALGO_ITER_NO = 3
FFS_PER_STEP = 1

def log_solution(sol, score):
    logging.info("solution: {}, score: {} /smaller-better/".format(sol, score))

def _offer_visualization(G, transitions, solution):
    print "Do you want to see visualization of newly computed solution? [y/N]: "
    if stdin.readline().strip().startswith("y"):
        visualize_simulation(G, transitions, solution)

def simple_genetic_crossover(G, init_nodes, vis=False, iter_no = ALGO_ITER_NO, ffs_per_step = FFS_PER_STEP):
    population_size = 4
    crossover_count = max(int(population_size*0.5), 1) # split point - how many firefighters are taken from 1st parent, how many from the 2nd
    mutation_count = 1
    crossover_point = 0.5

    if max(crossover_count + 1, mutation_count) > population_size:
        raise Exception("population_size must be >= crossover_count+1 && >= mutation_count")

    def simulate(solution):
        transitions, iterations, saved_nodes = simulation(G, solution, init_nodes, ffs_per_step)
        if vis:
            _offer_visualization(G, transitions, solution)
        return float(saved_nodes)/len(G.get_nodes())

    # list of 2-tuples (solution, score)
    curr_solutions = []

    # build initial solutions
    def next_sol(base_sol):
        solution = list(base_sol)
        random.shuffle(solution)
        score = simulate(solution)
        log_solution(solution, score)
        return solution, score

    for i in range(0, population_size):
        solution, score = next_sol(G.get_nodes())
        curr_solutions.append((solution, score))

    # sort list by scores desc
    def sort_by_score(solutions):
        sorted(solutions, key= lambda (sol, score): score)
    sort_by_score(curr_solutions)

    for i in range(0, iter_no):
        logging.info("**** ITERATION {} ****".format(i))

        # crossover
        for i in range(0, crossover_count):
            parents = curr_solutions[i:i+2]
            parent1 = parents[0][0]
            parent2 = parents[1][0]

            last_from_1st = max(int(len(parent1)*crossover_point), 1)
            first_part = parent1[0:last_from_1st+1]
            second_part = filter(lambda x: x not in first_part, parent2)

            child = first_part + second_part

            par_len = len(parent1)
            child_len = len(child)
            if(child_len != par_len):
                raise Exception("child has wrong size (child: {} parent: {})!".format(child, parent1))

            if(len(child) != len(set(child))):
                raise Exception("duplicate entries in child genome!")


            score = simulate(child)
            logging.info("crossing {} /score {}/ with {} /score {}/, got {} /score {}/".format(parents[0][0], parents[0][1], parents[1][0], parents[1][1], child, score))
            curr_solutions.append((child, score))

        # mutate some individuals
        fittest = curr_solutions[0:mutation_count]
        for sol, score in fittest:
            new_sol, new_score = next_sol(sol)
            logging.info("mutated solution {} /score {}/ built from {} /score {}/".format(new_sol, new_score, sol, score))
            curr_solutions.append((new_sol, new_score))

        # resort
        sort_by_score(curr_solutions)

        # keep only population_size of the strongest
        curr_solutions = curr_solutions[0:population_size]

    return curr_solutions[0]

solvers = {
    "simple_genetic_crossover": simple_genetic_crossover
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    configure_graph_generation_cli(parser)
    parser.add_argument('--algorithm', help='algorithm name', default='simple_genetic_crossover')
    parser.add_argument('--iters', help='number of algorithm iterations', type=int, default=ALGO_ITER_NO)
    parser.add_argument('--ffs', help='number of firefighters per step', type=int, default=FFS_PER_STEP)

    args = parser.parse_args()

    logging.basicConfig(level = logging.INFO)

    g = load_graph(args.vertices, args.density, args.starting_vertices)
    solver_func = solvers[args.algorithm]
    solver_func(g, map(lambda v: int(v.id), g.get_starting_nodes()), True, args.iters, args.ffs)