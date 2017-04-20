import random


def insertion_mutation(chromosome):
    """ Performs the following mutation:
         - selects random alleles
         - memorize the position of first selected allele
         - copy to child non-selected alleles, which precede first selected allele in parent
         - copy to child all the selected alleles in order of their presence in parent
         - copy to child all the remaining alleles in order of their presence in parent
    """

    selected = list()
    preceding = list()
    remaining = list()

    allele_selected, allele_non_selected = 1, 0
    choices = (allele_selected, allele_non_selected)
    for allele in chromosome:
        decision = random.choice(choices)
        if decision == allele_selected:
            selected.append(allele)
        elif not selected:
            preceding.append(allele)
        else:
            remaining.append(allele)

    return preceding + selected + remaining


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
    """ Draw a random swath (range) and 'slide' it left or right """

    size = len(chromosome)
    max_swath_factor = 0.6
    swath_size = random.randint(1, int(size * max_swath_factor))

    left = 0
    right = 1
    directions = (left, right)
    slide_direction = random.choice(directions)

    if slide_direction == left:
        # leave at least one position to left-slide
        a = random.randint(1, size - swath_size)
        b = a + swath_size - 1
        slide_length = - random.randint(1, a)
    else:
        # leave at least 1 position to right-slide
        b = random.randint(swath_size - 1, size - 2)
        a = b - swath_size + 1
        slide_length = random.randint(1, size - b - 1)

    # x, y correspond to a, b after slide
    x = a + slide_length
    y = b + slide_length

    # the slide of (a,b) includes a and b
    if slide_direction == left:
        mutated = chromosome[:x] + chromosome[a:b + 1] + chromosome[x:a] + chromosome[b + 1:]
    else:
        mutated = chromosome[:a] + chromosome[b + 1:y + 1] + chromosome[a:b + 1] + chromosome[y + 1:]

    return mutated


def random_swap_mutation(chromosome):
    """ Like single swap, but swaps a random string of consecutive values instead """
    a, b = random.sample(xrange(len(chromosome)), 2)
    if a > b:
        a, b = b, a

    max_swath_size = min(b - a, len(chromosome) - b)
    swath_size = random.randint(0, max_swath_size)

    return chromosome[:a] + chromosome[b:b + swath_size] + chromosome[a + swath_size:b] + \
           chromosome[a:a + swath_size] + chromosome[b + swath_size:]


def scramble_mutation(chromosome):
    raise NotImplementedError()


def single_swap_mutation(chromosome):
    i, j = random.sample(range(len(chromosome)), 2)
    chromosome[i], chromosome[j] = chromosome[j], chromosome[i]
    return chromosome


# TODO: is there an adjacent swap mutation???
