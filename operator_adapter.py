from frameworks import Operators


# ToDo
# * population sorting not needed (maybe expose helper function)
# * use AlgoScore in operators (provide function for decomposing population)
# * prepare configurable adapter

def wrap_crossover(operator):
    def _wrapper(es, parents):
        parent1, parent2 = parents
        child1, child2 = operator(parent1, parent2)
        return [child1, child2]

    return _wrapper


def wrap_mutation(operator):
    def _wrapper(es, specimen):
        return operator(specimen)

    return _wrapper


def wrap_selection(operator, parent_sets_count, specimen_count):
    def _wrapper(es):
        parent_sets = []

        for i in xrange(parent_sets_count):
            parents = operator(es.population, specimen_count,
                               (es.params.G, es.params.init_nodes, es.params.ffs_per_step))
            parent_sets.append(parents)

        return parent_sets

    return _wrapper
