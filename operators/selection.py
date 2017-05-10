import random

from heapq import nlargest


def _tuple_to_score(t):
    ch, algo_score = t
    return algo_score.to_fitness()


def _tuple_to_chromosome(t):
    ch, algoscore = t
    return ch

def _roulette_select(weighted_population, k):
    """ Returns k individual with probability proportional to assigned weights """

    weights_sum = sum(fitness for _, fitness in weighted_population)

    result = list()
    for _ in xrange(k):
        pick = random.uniform(0, weights_sum)
        current = 0
        for p, fitness in weighted_population:
            current += fitness
            if current > pick:
                result.append(p)
                break

    return result


def tournament_selection(population, k, environment):
    """

    :param population: list of tuples (chromosome, AlgoScore)
    :param k: number of individuals to be selected from population
    :param environment: a tuple (graph, init_nodes, ff_per_step) describing environment in which the solution is to be evaluated
    :return:
    """

    result = list()
    for _ in xrange(k):
        # select some random subpopulation
        subpopulation_size = random.randint(1, len(population) - 1)
        random_samples = random.sample(population, subpopulation_size)

        # get the best individual from the subpopulation
        winner = nlargest(1, random_samples, key=_tuple_to_score)
        best_ch, best_score = winner[0]
        result.append(best_ch)

    return result


def roulette_wheel_selection(population, k, environment):
    """

    :param population: list of tuples (chromosome, AlgoScore)
    :param k: number of individuals to be selected from population
    :param environment: a tuple (graph, init_nodes, ff_per_step) describing environment in which the solution is to be evaluated
    :return:
    """

    population_with_fitness_extracted = map(lambda (ch, algoscore): (ch, algoscore.to_fitness()), population)
    return _roulette_select(population_with_fitness_extracted, k)


def rank_selection(population, k, environment):
    """

    :param population: list of chromosomes
    :param k: number of individuals to be selected from population
    :param environment: a tuple (graph, init_nodes, ff_per_step) describing environment in which the solution is to be evaluated
    :return:
    """

    sorted_by_fitness = map(_tuple_to_chromosome, sorted(population, key=_tuple_to_score))
    ranks = xrange(1, len(population) + 1)

    population_with_rank = zip(sorted_by_fitness, ranks)

    return _roulette_select(population_with_rank, k)