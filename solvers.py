
import random
import logging
from simulation import simulation
from visualize import visualize_simulation
from sys import stdin, argv

iter_no = 3
ffs_per_step = 1

def _log(msg, debug_level):
    if(debug_level == 'logging' or debug_level == 'stepping'):
            logging.info("[SOLVER]: " + msg)

def _log_solution(sol, score, debug_level):
    _log("solution: {}, score: {} /smaller-better/".format(sol, score), debug_level)

def _offer_visualization(G, transitions, solution):
    print "Do you want to see visualization of newly computed solution? [y/N]: "
    if stdin.readline().strip().startswith("y"):
        visualize_simulation(G, transitions, solution)

def simple_genetic_crossover(G, init_nodes, debug_level="disabled"):
    population_size = 4
    crossover_count = max(int(population_size*0.5), 1) # split point - how many firefighters are taken from 1st parent, how many from the 2nd
    mutation_count = 1
    crossover_point = 0.5

    if max(crossover_count + 1, mutation_count) > population_size:
        raise Exception("population_size must be >= crossover_count+1 && >= mutation_count")

    def log(msg):
        _log(msg, debug_level)

    def log_solution(sol, score):
        _log_solution(sol, score, debug_level)

    def simulate(solution):
        transitions, iterations, saved_nodes = simulation(G, solution, init_nodes, ffs_per_step)
        if debug_level == 'stepping':
            _offer_visualization(G, transitions, solution)
        return saved_nodes

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
        log("**** ITERATION {} ****".format(i))

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
            log("crossing {} /score {}/ with {} /score {}/, got {} /score {}/".format(parents[0][0], parents[0][1], parents[1][0], parents[1][1], child, score))
            curr_solutions.append((child, score))

        # mutate some individuals
        fittest = curr_solutions[0:mutation_count]
        for sol, score in fittest:
            new_sol, new_score = next_sol(sol)
            log("mutated solution {} /score {}/ built from {} /score {}/".format(new_sol, new_score, sol, score))
            curr_solutions.append((new_sol, new_score))

        # resort
        sort_by_score(curr_solutions)

        # keep only population_size of the strongest
        curr_solutions = curr_solutions[0:population_size]

    return curr_solutions[0]

solvers = {
    "simple_genetic_crossover": simple_genetic_crossover
}

def test_solver(name):
    from graph import Graph
    g2 = Graph()
    g2.from_file(u'graphs/random.txt')
    init_nodes2 = [3]

    solver_func = solvers[name]
    solver_func(g2, init_nodes2, "stepping")

if __name__ == "__main__":
    if len(argv) < 2:
        print "first argument must be name of the algorithm"
        exit(1)

    test_solver(argv[1])