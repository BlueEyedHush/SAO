import random
import time
from operators import CROSSOVER, MUTATION

REPEAT = 500


def bench_crossover(s1, s2, op):
    op(s1, s2)


def bench_mutation(s1, s2, op):
    op(s1)


def gather_results():
    results = {}

    def register_result(specimen_size, operator_name, time):
        if operator_name not in results:
            xs = []
            ys = []
            results[operator_name] = (xs, ys)
        else:
            xs, ys = results[operator_name]

        xs.append(specimen_size)
        ys.append(time)

    def time_op(op_dict, op_runner, prefix):
        for name, op in op_dict.iteritems():
            start = time.clock()
            for i in xrange(REPEAT):
                op_runner(s1, s2, op)
            end = time.clock()
            register_result(specimen_size, prefix + name, end - start)

    specimen_sizes = [10, 50, 100, 250, 500]
    for specimen_size in specimen_sizes:
        s1 = list(xrange(specimen_size))
        s2 = list(s1)
        random.shuffle(s1)
        random.shuffle(s2)

        time_op(CROSSOVER, bench_crossover, "X ")
        time_op(MUTATION, bench_mutation, "MUT ")

    return results


def plot_results(res):
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(16, 8))
    fig.set_dpi(120)
    ax_normal = fig.add_subplot(1, 2, 1)
    ax_log = fig.add_subplot(1, 2, 2)

    for name, (xs, ys) in res.iteritems():
        ax_normal.plot(xs, ys, label=name)
        ax_log.semilogy(xs, ys, label=name)

    for ax in [ax_log, ax_normal]:
        ax.set_xlabel('Specimen size')
        ax.set_ylabel('Execution time')
        ax.legend()

    fig.savefig("results/plot_benchmark.png")


if __name__ == "__main__":
    results = gather_results()
    plot_results(results)
