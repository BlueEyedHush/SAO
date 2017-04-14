from sys import stdin
from simulation import simulation
from visualize import visualize_simulation

DEFAULTS = {
    'algo_iter_no': 3,
    'ffs_per_step': 1,
    'vis': False,
    'show_score_every': None,  # don't show
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
        all_node_ids = es.params.G.get_nodes().keys()
        population = []
        for i in xrange(2):
            population.append(all_node_ids)
        return population

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



class AlgoScore():
    def __init__(self, perc_saved_nodes, perc_saved_occupied_by_ff):
        self.perc_saved_nodes = perc_saved_nodes
        self.perc_saved_occupied_by_ff = perc_saved_occupied_by_ff

    def __str__(self):
        return "Saved {} ({} occupied by FFs)".format(self.perc_saved_nodes, self.perc_saved_occupied_by_ff)


class AlgoIn():
    def __init__(self,
                 G,
                 init_nodes,
                 operators=Operators(),
                 vis=DEFAULTS["vis"],
                 iter_no=DEFAULTS["algo_iter_no"],
                 ffs_per_step=DEFAULTS["ffs_per_step"],
                 show_score_every=DEFAULTS["show_score_every"]):
        self.G = G
        self.init_nodes = init_nodes
        self.vis = vis
        self.iter_no = iter_no
        self.ffs_per_step = ffs_per_step
        self.show_score_every = show_score_every

        self.operators = operators


class AlgoOut():
    def __init__(self, best_solution, best_solution_score):
        self.best_solution = best_solution
        self.best_solution_score = best_solution_score


def _offer_visualization(G, transitions, solution, score, comment=""):
    if comment:
        print "New solution ({}), score: {}".format(comment, score)
    print "Show visualization? [y/N]: "
    if stdin.readline().strip().startswith("y"):
        visualize_simulation(G, transitions, solution)


# sort list by scores desc
def _sort_by_score(solutions):
    return sorted(solutions, key=lambda (sol, score): score.perc_saved_nodes)


def _process_new_solution(params, solution, comment=""):
    G = params.G

    transitions, solution_score = simulation(G, solution, params.init_nodes, params.ffs_per_step)
    score = AlgoScore(perc_saved_nodes=float(solution_score.nodes_saved) / len(G.get_nodes()),
                      perc_saved_occupied_by_ff=float(solution_score.nodes_occupied_by_ff) / len(G.get_nodes()))
    if params.vis:
        _offer_visualization(G, transitions, solution, score, comment)
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
    es = ExecutionState(params)

    for specimen in params.operators.population_initialization(es):
        score = _process_new_solution(params, specimen, "initial population")
        es.population.append((specimen, score))
    es.population = _sort_by_score(es.population)

    for i in xrange(params.iter_no):
        es.current_iteration = i

        # crossover
        es.parents_list = params.operators.crossover_selection(es)
        for parents in es.parents_list:
            children = params.operators.crossover(es, parents)
            es.children.extend(children)
            for child in es.children:
                score = _process_new_solution(params, child, "crossover result")
                es.scored_children.append((child, score))

        # mutation
        es.mutation_candidates = params.operators.mutation_selection(es)
        for candidate in es.mutation_candidates:
            specimen_to_mutate = list(candidate)
            mutated_specimen = params.operators.mutation(es, specimen_to_mutate)
            score = _process_new_solution(params, mutated_specimen, "mutation result")
            es.scored_mutated_specimens.append((mutated_specimen, score))

        # add results of crossover & mutation to population
        es.population.extend(es.scored_children)
        es.population.extend(es.scored_mutated_specimens)

        # sucession
        es.population = _sort_by_score(es.population)
        new_population = params.operators.succession(es)
        es.population = _sort_by_score(new_population)

        if params.show_score_every is not None and i % params.show_score_every == 0:
            print "Scores after iteration {}: {}".format(i, map(lambda (_, score): str(score), es.population))

        es.reset_per_iteration_state()

    best_solution, score = es.population[0]
    return AlgoOut(best_solution, score)
