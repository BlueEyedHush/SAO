import csv
from logging import getLogger, INFO
from sys import stdin

from simulation import simulation
from visualize import visualize_simulation

algo_vis_last_logger = getLogger("algo_vis_last")
new_solution_logger = getLogger("new_solution")
algo_populations_logger = getLogger("algo_populations")
algo_per_iter_stats_logger = getLogger("per_iter_stats")
per_iter_stats_format = "{:>10} {:>10} {:>12} {:>10}"

SHOW_SCORE_EVERY = 1

DEFAULTS = {
    'algo_iter_no': 3,
    'ffs_per_step': 1,
}


class Operators():
    '''
    Shortcuts:
        es - ExecutionState

    Attributes:
        population_initialization: (es) -> list(specimen)
        crossover_selection: (es) -> list(list(specimen))
            executed once per iteration
            returns list of lists, each inner list represents set of parents
        crossover: (es, parents) -> list(specimen)
            executed multiple times per iteration, for each inner list returned by crossover_selection
        mutation_selector: (es) -> list(specimen)
            executed once per iteration
        mutation: (es, specimen) -> specimen
            executed for copy of each specimen returned by mutation_selector
            doesn't need to copy specimen, can modify it in-place
        succession: (es) -> list(specimen)
            executed once per operation
            can expect population to be in sorted state, but doesn't have to return it in sorted state

    Framework makes no assumptions about:
    * population size or that it's constant
    * number of parent sets selected for crossover (crossover_selection output)
    * number of parents in each crossover set or equality of size of different sets
    * number of specimens selected for mutations
    * number of population remaiming after succession
    However, each mutation must product single specimen

    Population state:
    * children from crossover & mutation are appended to population at the end of each iteration (before succession)
    * succession can expect population to be in sorted state
    * lists with children (both from crossover and mutation) are not sorted by score
    * main population is in sorted state at the beginning of each iteration and since it's not modified,
      it remains so for the rest of iteration

    Children are scored as soon as possible. This mean that they are available (with score) for subsequent invocatins
    of crossover & mutation.

    '''

    def __init__(self):
        pass

    def population_initialization(self, es):
        # print "default population initializer called"
        return self._random_population(es, 2)

    def crossover_selection(self, es):
        # print "default selector called"
        return [self._strip_score(es.population[0:2])]

    def crossover(self, es, parents):
        # print "default crossover called"
        return parents

    def mutation_selection(self, es):
        # print "default mutation selector"
        return es.children

    def mutation(self, es, specimen):
        # print "default mutation op"
        return specimen

    def succession(self, es):
        # print "default succession op"
        return es.population

    def _strip_score(self, list):
        return map(lambda (specimen, score): specimen, list)

    def _random_population(self, es, size):
        all_node_ids = es.params.G.get_nodes().keys()
        population = []
        for i in xrange(size):
            population.append(all_node_ids)
        return population


class AlgoScore():
    def __init__(self, perc_saved_nodes, perc_saved_occupied_by_ff):
        self.perc_saved_nodes = perc_saved_nodes
        self.perc_saved_occupied_by_ff = perc_saved_occupied_by_ff

    def to_fitness(self):
        return self.perc_saved_nodes

    def __str__(self):
        return "{}|{}".format(self.perc_saved_nodes, self.perc_saved_occupied_by_ff)


class AlgoIn():
    def __init__(self,
                 G,
                 init_nodes,
                 operators=Operators(),
                 iter_no=DEFAULTS["algo_iter_no"],
                 ffs_per_step=DEFAULTS["ffs_per_step"],
                 csv_file=None,
                 ):
        self.G = G
        self.init_nodes = init_nodes
        self.iter_no = iter_no
        self.ffs_per_step = ffs_per_step
        self.csv_file = csv_file
        self.operators = operators


class AlgoOut():
    def __init__(self, best_solution, best_solution_score):
        self.best_solution = best_solution
        self.best_solution_score = best_solution_score


# sort list by scores desc
def _sort_by_score(solutions):
    return sorted(solutions, key=lambda (sol, score): score.perc_saved_nodes, reverse=True)


def _process_solution(params, solution, comment="", offer_vis=False):
    def _sol_string():
        return "Solution (comment: {}), score: {}".format(comment, score)

    G = params.G

    transitions, solution_score = simulation(G, solution, params.init_nodes, params.ffs_per_step)
    score = AlgoScore(perc_saved_nodes=float(solution_score.nodes_saved) / len(G.get_nodes()),
                      perc_saved_occupied_by_ff=float(solution_score.nodes_occupied_by_ff) / len(G.get_nodes()))

    if offer_vis and algo_vis_last_logger.isEnabledFor(INFO):
        print _sol_string()
        print "Show visualization? [y/N]: "
        if stdin.readline().strip().startswith("y"):
            visualize_simulation(G, transitions, solution)
    elif new_solution_logger.isEnabledFor(INFO):
        new_solution_logger.info(_sol_string())

    return score


class ExecutionState():
    '''
    Specimen - permutation of node ids

    Attributes
        population: list((specimen, AlgoScore))
        parents_list: list(list(specimen))
        children: list(specimen)
        scored_children: list((specimen, AlgoScore))
        mutation_candidates: list(specimen)
        scored_mutated_specimens: list((specimen, AlgoScore))
    '''

    def __init__(self, params):
        self.params = params

        self.population = []
        self.reset_per_iteration_state()

    def reset_per_iteration_state(self):
        self.current_iteration = -1
        self.parents_list = []
        self.children = []
        self.scored_children = []
        self.mutation_candidates = []
        self.scored_mutated_specimens = []


def ga_framework(params):
    algo_per_iter_stats_logger.info(per_iter_stats_format.format("ITER_NO", "MAX_SAVED", "MAX_SAVED_FF", "SCORES_SUM"))

    es = ExecutionState(params)

    for specimen in params.operators.population_initialization(es):
        score = _process_solution(params, specimen, "initial population")
        es.population.append((specimen, score))
    es.population = _sort_by_score(es.population)

    if params.csv_file:
        csvfile = open(params.csv_file, 'wb')
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['iter_no', 'max_saved', 'max_saved_ff', 'scores_sum'])

    for i in xrange(params.iter_no):
        es.current_iteration = i

        # crossover
        es.parents_list = params.operators.crossover_selection(es)
        for parents in es.parents_list:
            children = params.operators.crossover(es, parents)
            es.children.extend(children)
            for child in es.children:
                score = _process_solution(params, child, "crossover result")
                es.scored_children.append((child, score))

        # mutation
        es.mutation_candidates = params.operators.mutation_selection(es)
        for candidate in es.mutation_candidates:
            specimen_to_mutate = list(candidate)
            mutated_specimen = params.operators.mutation(es, specimen_to_mutate)
            score = _process_solution(params, mutated_specimen, "mutation result")
            es.scored_mutated_specimens.append((mutated_specimen, score))

        # add results of crossover & mutation to population
        es.population.extend(es.scored_children)
        es.population.extend(es.scored_mutated_specimens)

        # sucession
        es.population = _sort_by_score(es.population)
        new_population = params.operators.succession(es)
        es.population = _sort_by_score(new_population)

        if i % SHOW_SCORE_EVERY == 0:
            algo_populations_logger.info("Population after iteration {}: {}"
                                         .format(i, map(lambda (_, score): str(score), es.population)))

        if algo_per_iter_stats_logger.isEnabledFor(INFO) or params.csv_file:
            _, max_score = es.population[0]
            max_saved = max_score.perc_saved_nodes
            max_saved_ff = max_score.perc_saved_occupied_by_ff
            sum_scores = sum(map(lambda (_, score): score.perc_saved_nodes, es.population))
            algo_per_iter_stats_logger.info(per_iter_stats_format.format(i, max_saved, max_saved_ff, sum_scores))
            if params.csv_file:
                writer.writerow([i, max_saved, max_saved_ff, sum_scores])

        es.reset_per_iteration_state()

    if params.csv_file:
        csvfile.close()

    best_solution, score = es.population[0]
    # solely to give chance to visualize
    _process_solution(params, best_solution, comment="Best solution", offer_vis=True)
    return AlgoOut(best_solution, score)
