
import csv
import os
import time
import sys
from collections import defaultdict
import multiprocessing
import traceback

from solvers import run_framework
from visualize import save_solution

MULTIPROCESSING_ENALBED = False
PROCESS_NUM = multiprocessing.cpu_count() - 1
STATUS_UPDATE_EVERY = 5  # in seconds


def graph_path_to_filename(path):
    filename = os.path.basename(path)
    last_dot_pos = filename.rfind(".")
    fname_without_extension = filename[0:last_dot_pos]
    return fname_without_extension


def get_title(config):
    graph_fname = graph_path_to_filename(config['input_file'])

    filename = "{}_{}_{}_{}_{}_{}_{}_{}.csv".format(
        config['population_size'],
        config['selection'],
        config['crossover'],
        config['mutation'],
        config['succession'],
        graph_fname,
        config['iters'],
        config['ffs'],
    )

    return filename


def ensure_directories(prefix):
    for f in ["csv", "sl", "plots"]:
        dir = os.path.join(prefix, f)
        if not os.path.exists(dir):
            os.makedirs(dir)


def build_csv_filepath(config, cfg_dir):
    full_path = os.path.join(cfg_dir, "csv", get_title(config) + ".csv")
    return full_path


def build_result_filepath(config, dir):
    return os.path.join(dir, "sl", get_title(config) + ".sl")


def build_plot_filepath(filename, prefix):
    return os.path.join(prefix, "plots", filename + ".png")


DEFAULT_TEST_SPEC = dict(
    population_size=[10, 20, 50],
    selection=['tournament', 'roulette', 'rank'],
    crossover=['cycle', 'injection', 'multi_injection', 'pmx', 'single_pmx'],
    # 'adjecent_swap' mutation does not perform very well in general, so it is skipped
    mutation=['insertion', 'inversion', 'slide', 'random_swap', 'scramble', 'single_swap'],
    succession=['rank', 'best_then_random', 'best'],
    iters=[2000],
    ffs=[3],
    input_file=["graphs/80_035_2.rgraph"],
)


def generate_configs(user_spec=None, iteration_order=None, group_by=None):
    # generate all possible combinations of defined operators and population size
    spec = DEFAULT_TEST_SPEC.copy()
    if user_spec is not None:
        spec.update(user_spec)

    it_order = iteration_order if iteration_order is not None else []
    # append missing ones to the end
    for k in DEFAULT_TEST_SPEC.keys():
        if k not in it_order:
            it_order.append(k)

    # move groupping feature to the end
    if group_by is not None:
        non_groupping_features = filter(lambda x: x != group_by, it_order)
        final_it_oroder = reversed([group_by] + non_groupping_features)
    else:
        final_it_oroder = reversed(it_order)

    configs = list()
    configs.append({})
    for feature in final_it_oroder:
        # we need to copy previous configuration for each value of our feature
        feature_values = spec[feature]

        def _duplicate_and_add(feature_value):
            new_configs = []
            for c in configs:
                nc = dict(c)
                nc[feature] = feature_value
                new_configs.append(nc)
            return new_configs

        new_configs = map(_duplicate_and_add, feature_values)

        if feature == group_by:
            # last feature that'll be appended
            # new_configs is list of configs, one list for each value
            # but here we need something else - list for each of unique other features
            configs = zip(*new_configs)
        else:
            configs = reduce(lambda l1, l2: l1 + l2, new_configs)

    return configs


# this must be global variable because it's going to be shared across multiple processes
# if you pass it as an argument, it'll be pickled (=copied) and won't work corretly
stats = None


def init_stats_object():
    global stats
    stats = {}
    stats["finished_iters"] = multiprocessing.Value("i", 0)
    stats["finished_configs"] = multiprocessing.Value("i", 0)


def calculate_with_config(cfg, iterations, prefix):
    csv_file = build_csv_filepath(cfg, prefix)

    results = dict()
    for iteration in xrange(iterations):
        results[iteration] = run_framework(
            loggers='',
            population_size=cfg['population_size'],
            selection=cfg['selection'],
            crossover=cfg['crossover'],
            mutation=cfg['mutation'],
            succession=cfg['succession'],
            iters=cfg['iters'],
            ffs=cfg['ffs'],
            input_file=cfg['input_file'],
        )

        if MULTIPROCESSING_ENALBED:
            with stats["finished_iters"].get_lock():
                stats["finished_iters"].value += 1

    iteration_results = defaultdict(list)
    for iteration in results:
        for i in results[iteration].iteration_results:
            iteration_results[i].append(results[iteration].iteration_results[i])

    with open(csv_file, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for i in iteration_results:
            writer.writerow(iteration_results[i])

    r = results.items()
    (r_h_i, r_h_ao), r_t = r[0], r[1:]
    best_solution = r_h_ao.best_solution
    best_fitness = r_h_ao.best_solution_score.to_fitness()
    best_score_i = r_h_i
    for i, algo_out in r_t:
        curr_fitness = algo_out.best_solution_score.to_fitness()
        if curr_fitness > best_fitness:
            best_solution = algo_out.best_solution
            best_fitness = curr_fitness
            best_score_i = i

    save_solution(best_solution, best_score_i, build_result_filepath(cfg, prefix))

    if MULTIPROCESSING_ENALBED:
        with stats["finished_configs"].get_lock():
            stats["finished_configs"].value += 1

    return True


class PerProcessData():
    def __init__(self, config, iterations, prefix):
        self.config = config
        self.iterations = iterations
        self.prefix = prefix

def wrapper(ppd):
    try:
        calculate_with_config(ppd.config, ppd.iterations, ppd.prefix)
    except Exception:
        print "Exception occured for config: {}".format(ppd.config)
        traceback.print_exc()
        raise


def time_prognose(start_timestamp, iters_count, current_iters):
    if current_iters <= 0:
        return "<not yet calculated>"
    else:
        elapsed_seconds = time.time() - start_timestamp
        prognosed_duration = elapsed_seconds * iters_count / current_iters
        prognosed_seconds_left = prognosed_duration - elapsed_seconds

        m, s = divmod(prognosed_seconds_left, 60)
        h, m = divmod(m, 60)
        return "%d:%02d:%02d" % (h, m, s)


def evaluate(configs, prefix, fiters):
    ensure_directories(prefix)

    init_stats_object()
    configs_count = len(configs)
    iters_count = configs_count * fiters

    if MULTIPROCESSING_ENALBED:
        per_config_data = map(lambda c: PerProcessData(config=c, iterations=fiters, prefix=prefix), configs)

        chunk_size = max(len(configs) / PROCESS_NUM, 1)
        print("Using {} processes, chunk size is {}".format(PROCESS_NUM, chunk_size))
        sys.stdout.flush()

        start_timestamp = time.time()
        p = multiprocessing.Pool(processes=max(len(configs), PROCESS_NUM))
        ar = p.map_async(wrapper, per_config_data, chunk_size)

        done = False
        while not done:
            try:
                ar.get(STATUS_UPDATE_EVERY)
                done = True
            except multiprocessing.TimeoutError:
                # print stats
                with stats["finished_configs"].get_lock():
                    fc = stats["finished_configs"].value
                with stats["finished_iters"].get_lock():
                    fi = stats["finished_iters"].value

                ptl = time_prognose(start_timestamp, iters_count, fi)
                print("Finished configs: {}/{}, finished iterations: {}/{}. Prognosed time left: {}"
                      .format(fc, configs_count, fi, iters_count, ptl))
                sys.stdout.flush()

        print("Finished calculations!")

    else:
        counter = 0
        for cfg in configs:
            calculate_with_config(cfg, fiters, prefix)
            counter += 1
            print("Processed {}/{} configs.".format(counter, configs_count))
