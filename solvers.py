
import random
from simulation import simulation

def test_simple_solver():
    from graph import Graph
    g2 = Graph()
    g2.from_file('graphs/random.txt')
    init_nodes2 = [3]

    simple(g2, init_nodes2, "logging")

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

    iter_no = 10
    ffs_per_step = 1

    def calc_next_solution(current):
        new_solution = list(current)
        random.shuffle(new_solution)
        new_score = simulation(G, new_solution, init_nodes, ffs_per_step)[1]
        return new_solution, new_score

    def log_solution(sol, score):
        log("solution: {}, score: {} /smaller-better/".format(sol, score))

    current_solution, current_score = calc_next_solution(G.get_nodes())
    log_solution(current_solution, current_score)

    for i in range(0, iter_no):
        new_solution, new_score = calc_next_solution(current_solution)
        log_solution(new_solution, new_score)

        if new_score < current_score:
            current_solution = new_solution
            current_score = new_score
            log("accepted")
        else:
            log("rejected")

    return current_score, current_score
