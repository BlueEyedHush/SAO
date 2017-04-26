import argparse
from frameworks import Operators, AlgoIn, ga_framework, DEFAULTS
from generate import load_graph
from logging_configs import configure_logging
from operator_adapter import wrap_crossover, wrap_mutation, wrap_selection
from operators import SELECTION, CROSSOVER, MUTATION

class ConfigurableSimpleSolver(object, Operators):
    def __init__(self, population_size=4, selection_op=None, crossover_op=None, mutation_op=None):
        super(ConfigurableSimpleSolver, self).__init__()
        self.population_size = population_size
        if selection_op is not None:
            self.crossover_selection = wrap_selection(selection_op, 1, 2)
        if crossover_op is not None:
            self.crossover = wrap_crossover(crossover_op)
        if mutation_op is not None:
            self.mutation = wrap_mutation(mutation_op)

    def population_initialization(self, es):
        return Operators._random_population(self, es, self.population_size)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

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

    parser.add_argument('-os', '--selection',
                        help='selection operator',
                        choices=SELECTION.keys(),
                        default=SELECTION.keys()[0])
    parser.add_argument('-oc', '--crossover',
                        help='crossover operator',
                        choices=CROSSOVER.keys(),
                        default=CROSSOVER.keys()[0])
    parser.add_argument('-om', '--mutation',
                        help='mutation operator',
                        choices=MUTATION.keys(),
                        default=MUTATION.keys()[0])

    args = parser.parse_args()

    configure_logging(args.loggers)

    g = load_graph(args.vertices, args.density, args.starting_vertices)

    operators = ConfigurableSimpleSolver(
        selection_op=SELECTION[args.selection],
        crossover_op=CROSSOVER[args.crossover],
        mutation_op=MUTATION[args.mutation],
    )

    ga_framework(AlgoIn(g,
                        map(lambda v: int(v.id), g.get_starting_nodes()),
                        operators=operators,
                        iter_no=args.iters,
                        ffs_per_step=args.ffs,
                        ))
