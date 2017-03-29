
import random
from simulation import simulation
from visualize import visualize_simulation
from sys import stdin, argv

iter_no = 3
ffs_per_step = 1

def _log(msg, debug_level):
    if(debug_level == 'logging' or debug_level == 'stepping'):
            print "[SOLVER]: " + msg

def _log_solution(sol, score, debug_level):
    _log("solution: {}, score: {} /smaller-better/".format(sol, score), debug_level)

def _offer_visualization(G, transitions, solution):
    print "Do you want to see visualization of newly computed solution? [y/N]: "
    if stdin.readline().strip().startswith("y"):
        visualize_simulation(G, transitions, solution)

def simple(G, init_nodes, debug_level="disabled"):
    '''
    :param G:
    :param init_nodes:
    :param debug_level: one of "disabled"|"logging"|"stepping"
    :return: tuple (winning permutation, score)
    '''

    def log(msg):
        _log(msg, debug_level)

    def log_solution(sol, score):
        _log_solution(sol, score, debug_level)

    def calc_next_solution(current):
        new_solution = list(current)
        random.shuffle(new_solution)
        transitions, new_score = simulation(G, new_solution, init_nodes, ffs_per_step)[0:2]
        log_solution(new_solution, new_score)

        if debug_level == 'stepping':
            _offer_visualization(G, transitions, new_solution)

        return new_solution, new_score

    current_solution, current_score = calc_next_solution(G.get_nodes())

    for i in range(0, iter_no):
        new_solution, new_score = calc_next_solution(current_solution)

        if new_score < current_score:
            current_solution = new_solution
            current_score = new_score
            log("accepted")
        else:
            log("rejected")

    return current_score, current_score

population_size = 4
select_perc = 0.5

# mutation only algorithm
def simple_genetic(G, init_nodes, debug_level="disabled"):

    def log(msg):
        _log(msg, debug_level)

    def log_solution(sol, score):
        _log_solution(sol, score, debug_level)

    # list of 2-tuples (solution, score)
    curr_solutions = []

    # build initial solutions
    def next_sol(base_sol):
        solution = list(base_sol)
        random.shuffle(solution)
        transitions, score = simulation(G, solution, init_nodes, ffs_per_step)[0:2]
        log_solution(solution, score)

        if debug_level == 'stepping':
            _offer_visualization(G, transitions, solution)

        return solution, score

    for i in range(0, population_size):
        solution, score = next_sol(G.get_nodes())
        curr_solutions.append((solution, score))

    # sort list by scores desc
    def sort_by_score(solutions):
        sorted(solutions, key= lambda (sol, score): score)
    sort_by_score(curr_solutions)

    for i in range(0, iter_no):
        # take fittest and mutate them /by permuting/
        fittest_no = max(int(population_size*select_perc), 1)
        fittest = curr_solutions[0:fittest_no]
        log("taking {} fittest with scores {}".format(fittest_no, map(lambda (sol, score): score, fittest)))
        for sol, score in curr_solutions[0:fittest_no]:
            new_sol, new_score = next_sol(sol)
            curr_solutions.append((new_sol, new_score))
            log("got new solution built from {} (was score {})".format(sol, score))

        # resort
        sort_by_score(curr_solutions)

        # keep only population_size of the strongest
        curr_solutions = curr_solutions[0:population_size]

    return curr_solutions[0]

solvers = {
    "simple": simple,
    "simple_genetic": simple_genetic
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