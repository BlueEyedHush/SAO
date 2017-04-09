import random


def injection_crossover(child1, child2):
    # select distinct points a < b between 0 and len(child1)
    a, b = random.sample(range(len(child1)), 2)
    if a > b:
        a, b = b, a

    print "{} {}".format(a, b)
    # Make an empty child chromosome of length len(child1)
    result = [None for _ in xrange(len(child1))]

    # Copy over the genes of child1 from a to (but not including) b into the corresponding genes of the child
    ab = child1[a:b]
    result[a:b] = ab

    # Fill in the rest of the genes of the child with the genes from child2, in the order in which they appear in child2,
    # making sure not to include alleles that already exist in the child
    remainder = [e for e in child2 if e not in ab]
    for i in xrange(a):
        result[i] = remainder.pop(0)
    for i in xrange(b, len(child1)):
        result[i] = remainder.pop(0)

    return result
