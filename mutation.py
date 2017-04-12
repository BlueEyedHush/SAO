import random


def insertion_mutation():
    raise NotImplementedError()


def inversion_mutation():
    raise NotImplementedError()


def random_slide_mutation():
    raise NotImplementedError()


def random_swap_mutation():
    raise NotImplementedError()


def scramble_mutation():
    raise NotImplementedError()


def single_swap_mutation(chromosome):
    i, j = random.sample(range(len(chromosome)), 2)
    chromosome[i], chromosome[j] = chromosome[j], chromosome[i]
    return chromosome
