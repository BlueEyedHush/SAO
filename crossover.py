import copy
import random


def cycle_crossover(parent1, parent2):
    """
    A very nice description of the algorithm:
    http://www.rubicite.com/Tutorials/GeneticAlgorithms/CrossoverOperators/CycleCrossoverOperator.aspx

    :param parent1: list, permutation of alleles
    :param parent2: list, permutation of alleles
    :return: child1, child2
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


def injection_crossover(parent1, parent2):
    """ Also called order 1 crossover """

    def get_child(p1, p2):
        # select distinct points a < b between 0 and len(parent1)
        a, b = random.sample(range(len(p1)), 2)
        if a > b:
            a, b = b, a

        # Make an empty child chromosome of length len(child)
        child = [None for _ in xrange(len(p1))]

        # Copy over the genes of child from a to (but not including) b into the corresponding genes of the child
        ab = p1[a:b]
        child[a:b] = ab

        # Fill in the rest of the genes of the child with the genes from child2, in the order in which they appear in child2,
        # making sure not to include alleles that already exist in the child
        remainder = [e for e in p2 if e not in ab]
        for i in xrange(a):
            child[i] = remainder.pop(0)
        for i in xrange(b, len(p1)):
            child[i] = remainder.pop(0)

        return child

    child1 = get_child(parent1, parent2)
    child2 = get_child(parent2, parent1)

    return child1, child2


def pmx_crossover(parent1, parent2):
    """
        Partially mapped crossover.
        Version with swapping chosen swath of alleles, described here:
        http://www.rubicite.com/Tutorials/GeneticAlgorithms/CrossoverOperators/PMXCrossoverOperator.aspx
    """

    def get_child(p1, p2):
        a, b = random.sample(range(len(p1) + 1), 2)
        if a > b:
            a, b = b, a

        child = copy.deepcopy(p1)

        not_used_values = list()
        for v in p2[a:b]:
            if v not in p1[a:b]:
                not_used_values.append(v)

        used_indexes = range(a, b)
        for v in not_used_values:

            inserted = False
            p2_val = v
            while not inserted:
                index_in_p2 = p2.index(p2_val)
                p1_val = p1[index_in_p2]
                new_index_in_p2 = p2.index(p1_val)
                if a <= new_index_in_p2 < b:
                    p2_val = p2[new_index_in_p2]
                else:
                    child[new_index_in_p2] = v
                    used_indexes.append(new_index_in_p2)
                    inserted = True

        for i in range(0, len(p1)):
            if i not in used_indexes:
                child[i] = p2[i]

        return child

    child1 = get_child(parent1, parent2)
    child2 = get_child(parent2, parent1)

    return child1, child2


def pmx_with_single_crossover_point(parent1, parent2):
    """
        Partially mapped crossover.
        Version with a single crossover point, described here:
        http://user.ceng.metu.edu.tr/~ucoluk/research/publications/tspnew.pdf
    """

    def swap(l, index1, index2):
        l[index1], l[index2] = l[index2], l[index1]

    crossover_point = random.randint(0, len(parent1))

    child1 = copy.deepcopy(parent1)
    child2 = copy.deepcopy(parent2)

    for i in xrange(crossover_point):
        element_to_swap = parent2[i]
        swap(child1, i, child1.index(element_to_swap))

    for i in xrange(crossover_point):
        element_to_swap = parent1[i]
        swap(child2, i, child2.index(element_to_swap))

    return child1, child2
