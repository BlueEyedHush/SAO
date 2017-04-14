import random
import argparse
from frameworks import Operators, AlgoIn, ga_framework, DEFAULTS
from generate import load_graph
from logging_configs import configure_logging

class SimpleGeneticCrossover(object, Operators):
    population_size = 4

    def __init__(self):
        Operators.__init__(self)

    def population_initialization(self, es):
        all_node_ids = es.params.G.get_nodes().keys()
        population = []
        for i in xrange(SimpleGeneticCrossover.population_size):
            specimen = list(all_node_ids)
            random.shuffle(specimen)
            population.append(specimen)
        return population

    def crossover_selection(self, es):
        return [self._strip_score(es.population[0:2])]

    def crossover(self, es, parents):
        crossover_point = 0.5

        last_from_1st = max(int(len(parents[0]) * crossover_point), 1)
        first_part = parents[0][0:last_from_1st + 1]
        second_part = filter(lambda x: x not in first_part, parents[1])

        child = first_part + second_part
        return [child]

    def mutation_selection(self, es):
        return self._strip_score(es.population[0:1])

    def mutation(self, es, specimen):
        i, j = random.sample(xrange(len(specimen)), 2)
        tmp = specimen[i]
        specimen[i] = specimen[j]
        specimen[j] = tmp
        return specimen

    def succession(self, es):
        return es.population[0:SimpleGeneticCrossover.population_size]


solvers = {
    "defaults": Operators(),
    "simple_genetic_crossover": SimpleGeneticCrossover(),
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-a', '--algorithm',
                        help='algorithm name',
                        choices=solvers.keys(),
                        default='simple_genetic_crossover')
    parser.add_argument('-d', '--density',
                        help='edges density; float in range [0..1]',
                        type=float,
                        default=0.2)
    parser.add_argument('-f', '--ffs',
                        help='number of firefighters per step',
                        type=int,
                        default=DEFAULTS['ffs_per_step'])
    parser.add_argument('-i', '--iters',
                        help='number of algorithm iterations',
                        type=int,
                        default=DEFAULTS['algo_iter_no'])
    parser.add_argument('-s', '--starting_vertices',
                        help='number of starting vertices',
                        type=int,
                        default=1)
    parser.add_argument('-v', '--vertices',
                        help='number of vertices in graph',
                        type=int,
                        default=10)
    parser.add_argument('-l', '--loggers',
                        help='configuration of loggers (i.e. graph_printing=info,benchmark_results=info)',
                        default='')

    args = parser.parse_args()

    configure_logging(args.loggers)

    g = load_graph(args.vertices, args.density, args.starting_vertices)
    operators = solvers[args.algorithm]
    ga_framework(AlgoIn(g,
                        map(lambda v: int(v.id), g.get_starting_nodes()),
                        operators=operators,
                        iter_no=args.iters,
                        ffs_per_step=args.ffs,
                        ))
