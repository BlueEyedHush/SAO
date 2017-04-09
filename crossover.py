import random


def injection_crossover(parent1, parent2):
    # select distinct points a < b between 0 and len(child1)
    a, b = random.sample(range(len(parent1)), 2)
    if a > b:
        a, b = b, a

    # Make an empty child chromosome of length len(child1)
    result = [None for _ in xrange(len(parent1))]

    # Copy over the genes of child1 from a to (but not including) b into the corresponding genes of the child
    ab = parent1[a:b]
    result[a:b] = ab

    # Fill in the rest of the genes of the child with the genes from child2, in the order in which they appear in child2,
    # making sure not to include alleles that already exist in the child
    remainder = [e for e in parent2 if e not in ab]
    for i in xrange(a):
        result[i] = remainder.pop(0)
    for i in xrange(b, len(parent1)):
        result[i] = remainder.pop(0)

    return result


def pmx_crossover(parent1, parent2):
    raise NotImplementedError()


def cycle_crossover(parent1, parent2):
    """
    A very nice description of the algorithm:
    http://www.rubicite.com/Tutorials/GeneticAlgorithms/CrossoverOperators/CycleCrossoverOperator.aspx

    :param parent1: list, permutation of alleles
    :param parent2: list, permutation of alleles
    :return:
    """

    def all_cycles_found(used_indexes):
        return sum([len(sublist) for sublist in used_indexes]) == len(parent1)

    def first_unused_index(used_indexes):
        flatten_used_indexes = [index for sublist in used_indexes for index in sublist]
        for i in xrange(len(parent1)):
            if i not in flatten_used_indexes:
                return i
        raise ValueError('All indexes seem to be used, there is a bug in the algorithm...')

    def find_all_cycles():
        """ In fact this function returns list of lists of indexes of cycles in parent1 """
        cycles_indexes = list()
        while not all_cycles_found(cycles_indexes):

            first_index = first_unused_index(cycles_indexes)

            current_cycle_indexes = [first_index]
            starting_element = parent1[first_index]
            current_element = parent2[first_index]
            while current_element != starting_element:
                index_in_p1 = parent1.index(current_element)
                current_cycle_indexes.append(index_in_p1)
                current_element = parent2[index_in_p1]

                current_cycle_indexes = sorted(current_cycle_indexes)

            cycles_indexes.append(current_cycle_indexes)

        return cycles_indexes

    child1 = [None for _ in xrange(len(parent1))]
    child2 = [None for _ in xrange(len(parent2))]

    cycles_indexes = find_all_cycles()

    reverse_copy = False
    for cycle_index_list in cycles_indexes:
        if reverse_copy:
            for index in cycle_index_list:
                child1[index] = parent2[index]
                child2[index] = parent1[index]
            reverse_copy = False
        else:
            for index in cycle_index_list:
                child1[index] = parent1[index]
                child2[index] = parent2[index]
            reverse_copy = True

    return child1, child2
