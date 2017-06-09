from deterministic import greedy_tree_solution
from graph import Graph, Tree
from simulation import simulation
from solvers import run_framework
from visualize import visualize_simulation


# TODO get_burning_nodes is not optimal
# TODO tree generation - improve, unify
# TODO graphs should be generated as connected

def genetic_solution(graph_file, ff_per_step):
    algo_out = run_framework(loggers='',
                             population_size=100,
                             selection='roulette',
                             crossover='injection',
                             mutation='single_swap',
                             succession='best',
                             iters=1000,
                             ffs=ff_per_step,
                             input_file=graph_file)

    graph = Graph.from_file(graph_file)
    return graph, algo_out.best_solution


def deterministic_solution_for_tree(graph_file, ff_per_step):
    tree = Tree.from_file(graph_file)
    solution = greedy_tree_solution(tree, ff_per_step=ff_per_step)
    return tree, solution


if __name__ == '__main__':
    graph_file = 'graphs/tree2.rtree'
    ff_per_step = 2

    genetic = True
    if genetic:
        algorithm = genetic_solution
        msg = "Used genetic algorithm"
    else:
        algorithm = deterministic_solution_for_tree
        msg = "Used deterministic algorithm"

    graph, solution = algorithm(graph_file, ff_per_step)

    transitions, score = simulation(graph, solution, ff_per_step=ff_per_step)
    print msg
    print "Nodes saved: {}\nNodes occupied by ff: {}".format(score.nodes_saved, score.nodes_occupied_by_ff)

    visualize_simulation(graph, transitions, solution)
