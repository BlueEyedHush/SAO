from graph import Graph
from simulation import simulation
from visualize import visualize_simulation

g = Graph.from_file('graphs/simple.txt')
solution = [1, 0, 2, 4, 3]
init_nodes = [4]

g2 = Graph.from_file('graphs/random.txt')
solution2 = [9, 0, 2, 4, 3, 5, 6, 7, 8, 1]
init_nodes2 = [3]

# pick up here whichever variant you like
p_graph = g2
p_solution = solution2
p_init_nodes = init_nodes2

transitions, _, _, _ = simulation(p_graph, p_solution, init_nodes=p_init_nodes, ff_per_step=1)
visualize_simulation(p_graph, transitions, p_solution)
