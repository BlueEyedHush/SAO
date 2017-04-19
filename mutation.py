import random


def insertion_mutation(chromosome):
    raise NotImplementedError()


def inversion_mutation(chromosome):
    """ Inverts randomly selected swath (range) of alleles"""
    max_swath_factor = 0.6
    min_swath_factor = 0.0
    max_swath_size = int(len(chromosome) * max_swath_factor)
    min_swath_size = int(len(chromosome) * min_swath_factor)

    a, b = random.sample(range(len(chromosome)), 2)
    if a > b:
        a, b = b, a
    if (b - a) > max_swath_size:
        b = a + max_swath_size
    if (b - a) < min_swath_size:
        b = a + min_swath_size

    mutated = chromosome[:a] + list(reversed(chromosome[a:b])) + chromosome[b:]
    return mutated


def random_slide_mutation(chromosome):
    raise NotImplementedError()


def random_swap_mutation(chromosome):
    raise NotImplementedError()


def scramble_mutation(chromosome):
    raise NotImplementedError()


def single_swap_mutation(chromosome):
    i, j = random.sample(range(len(chromosome)), 2)
    chromosome[i], chromosome[j] = chromosome[j], chromosome[i]
    return chromosome
