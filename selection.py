import random

from simulation import simulation


def evaluate(chromosome, environment):
    graph, init_nodes, ff_per_step = environment
    return simulation(graph, chromosome, init_nodes, ff_per_step)


def tournament_selection(population, k, environment):
    """

    :param population: list of chromosomes
    :param k: number of individuals to be selected from population
    :param environment: a tuple (graph, init_nodes, ff_per_step) describing environment in which the solution is to be evaluated
    :return:
    """
    random_k_samples = sorted(random.sample(population, k), key=lambda p: evaluate(p, environment))

    print random_k_samples


def roulette_wheel_selection(population, k, environment):
    """

    :param population: list of chromosomes
    :param k: number of individuals to be selected from population
    :param environment: a tuple (graph, init_nodes, ff_per_step) describing environment in which the solution is to be evaluated
    :return:
    """
    raise NotImplementedError()


def rank_selection(population, k, environment):
    """

    :param population: list of chromosomes
    :param k: number of individuals to be selected from population
    :param environment: a tuple (graph, init_nodes, ff_per_step) describing environment in which the solution is to be evaluated
    :return:
    """
    raise NotImplementedError()
