
import random
from simulation import simulation
from visualize import visualize_simulation
from sys import stdin

def test_simple_solver():
    from graph import Graph
    g2 = Graph()
    g2.from_file('graphs/random.txt')
    init_nodes2 = [3]

    simple(g2, init_nodes2, "stepping")

def simple(G, init_nodes, debug_level="disabled"):
    '''
    :param G:
    :param init_nodes:
    :param debug_level: one of "disabled"|"logging"|"stepping"
    :return: tuple (winning permutation, score)
    '''

    def log(msg):
        if(debug_level == 'logging' or debug_level == 'stepping'):
            print msg

    iter_no = 5
    ffs_per_step = 1

    def log_solution(sol, score):
        log("solution: {}, score: {} /smaller-better/".format(sol, score))

    def calc_next_solution(current):
        new_solution = list(current)
        random.shuffle(new_solution)
        transitions, new_score = simulation(G, new_solution, init_nodes, ffs_per_step)[0:2]
        log_solution(new_solution, new_score)

        if debug_level == 'stepping':
            print "Do you want to see visualization of newly computed solution? [y/N]: "
            if stdin.readline().strip().startswith("y"):
                visualize_simulation(G, transitions, new_solution)

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
