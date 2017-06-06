
import argparse
import csv
import os
import time
from collections import defaultdict
import multiprocessing

from solvers import run_framework

PROCESS_NUM = multiprocessing.cpu_count() - 1
STATUS_UPDATE_EVERY = 5  # in seconds


def graph_path_to_filename(path):
    filename = os.path.basename(path)
    last_dot_pos = filename.rfind(".")
    fname_without_extension = filename[0:last_dot_pos]
    return fname_without_extension


def build_cfg_filepath(config, cfg_dir):
    graph_fname = graph_path_to_filename(config['input_file'])

    filename = "{}_{}_{}_{}_{}.csv".format(
        config['population_size'],
        config['selection'],
        config['crossover'],
        config['mutation'],
        graph_fname,
    )

    full_path = os.path.join(cfg_dir, filename)
    return full_path


DEFAULT_TEST_SPEC = dict(
    population_size=[10, 20, 50],
    selection=['tournament', 'roulette', 'rank'],
    crossover=['cycle', 'injection', 'multi_injection', 'pmx', 'single_pmx'],
    # 'adjecent_swap' mutation does not perform very well in general, so it is skipped
    mutation=['insertion', 'inversion', 'slide', 'random_swap', 'scramble', 'single_swap'],
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


def calculate_with_config(cfg, iterations, csv_dir):
    csv_file = build_cfg_filepath(cfg, csv_dir)

    results = dict()
    for iteration in xrange(iterations):
        results[iteration] = run_framework(
            loggers='',
            population_size=cfg['population_size'],
            selection=cfg['selection'],
            crossover=cfg['crossover'],
            mutation=cfg['mutation'],
            iters=cfg['iters'],
            ffs=cfg['ffs'],
            input_file=cfg['input_file'],
        )

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

    with stats["finished_configs"].get_lock():
        stats["finished_configs"].value += 1

    return True


class PerProcessData():
    def __init__(self, config, iterations, csv_dir):
        self.config = config
        self.iterations = iterations
        self.csv_dir = csv_dir

def wrapper(ppd):
    calculate_with_config(ppd.config, ppd.iterations, ppd.csv_dir)


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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-fi', '--fiters',
                        type=int,
                        default=10,
                        help='number of times to invoke genetic framework')

    parser.add_argument('-o', '--out',
                        default="results/default_csv",
                        help='directory where generated CSV files are going to be stored')

    args = parser.parse_args()

    if not os.path.exists(args.out):
        print "{} does not exists, creating.".format(args.out)
        os.makedirs(args.out)

    configs = generate_configs()
    init_stats_object()
    configs_count = len(configs)
    iters_count = configs_count * args.fiters
    per_config_data = map(lambda c: PerProcessData(config=c, iterations=args.fiters, csv_dir=args.out), configs)

    chunk_size = len(configs) / PROCESS_NUM
    print("Using {} processes, chunk size is {}".format(PROCESS_NUM, chunk_size))

    start_timestamp = time.time()
    p = multiprocessing.Pool(processes=PROCESS_NUM)
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

            curr_timestamp = time.time()
            ptl = time_prognose(start_timestamp, iters_count, fi)
            print("Finished configs: {}/{}, finished iterations: {}/{}. Prognosed time left: {}"
                  .format(fc, configs_count, fi, iters_count, ptl))

    print("Finished calculations!")
