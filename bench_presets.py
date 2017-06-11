import evaluate as ev
import draw_plots as dp


def eval_compare_all():
    return ev.generate_configs(), "results/80_035_2/", 10


def plot_compare_all():
    cd = "results/80_035_2/"

    for gb in ["mutation", "population_size", "crossover", "selection"]:
        configs = ev.generate_configs({}, group_by=gb)
        dp.draw_plots(configs, dp.line_plot_builder, groupped_by=gb, prefix=cd)


def get_compare_succession_spec():
    return {
        "population_size": [10, 50, 100],
        "selection": ["roulette"],
        "mutation": ["single_swap"],
        "crossover": ["injection"],
        "succession": ["best", "rank", "best_then_random"],
        "iters": [5000],
    }


def eval_compare_succession():
    return ev.generate_configs(get_compare_succession_spec()), "results/succession_comparison_m/", 3


def plot_compare_succession():
    cd = "results/succession_comparison_m/"
    gb = "succession"
    configs = ev.generate_configs(get_compare_succession_spec(), group_by=gb)
    dp.draw_plots(configs, dp.line_plot_builder, groupped_by=gb, prefix=cd)
    dp.draw_plots(configs, dp.box_plot_builder, groupped_by=gb, prefix=cd)


def get_v320_spec():
    return {
        "population_size": [100],
        "selection": ["roulette"],
        "mutation": ["single_swap"],
        "crossover": ["injection"],
        "succession": ["best", "best_then_random"],
        "iters": [5000],
        "input_file": ["graphs/320_0.009_1.rgraph"],
    }


def v320_eval():
    prefix = "results/320_009_1/"
    tries = 1

    ev.evaluate(ev.generate_configs(get_v320_spec()), prefix, tries)


def v320_plot():
    prefix = "results/320_009_1/"
    gb = "succession"
    configs = ev.generate_configs(get_v320_spec(), group_by=gb)
    dp.draw_plots(configs, dp.line_plot_builder, groupped_by=gb, prefix=prefix)
    dp.draw_plots(configs, dp.box_plot_builder, groupped_by=gb, prefix=prefix)


def get_v320_spec_compare_all():
    return {
        "population_size": [100],
        "iters": [10000],
        "input_file": ["graphs/320_0.009_1.rgraph"],
    }


def v320_eval_compare_all():
    prefix = "results/320_009_1_compare_all/"
    tries = 1
    spec = get_v320_spec_compare_all()

    ev.evaluate(ev.generate_configs(spec), prefix, tries)


def get_wc_spec():
    return dict(
        population_size=[100],
        selection=['roulette'],
        crossover=['injection', 'noop'],
        # 'adjecent_swap' mutation does not perform very well in general, so it is skipped
        mutation=['single_swap'],
        succession=['best_then_random'],
        iters=[15000],
        ffs=[3],
        input_file=["graphs/80_035_2.rgraph"],
    )


def without_crossover_eval():
    prefix = "results/no_crossover1/"
    spec = get_wc_spec()
    tries = 3

    ev.evaluate(ev.generate_configs(spec), prefix, tries)


def wc_plot():
    prefix = "results/no_crossover/"
    spec = get_wc_spec()
    gb = "crossover"

    configs = ev.generate_configs(spec, group_by=gb)
    dp.draw_plots(configs, dp.line_plot_builder, groupped_by=gb, prefix=prefix)
    dp.draw_plots(configs, dp.box_plot_builder, groupped_by=gb, prefix=prefix)


def get_v320_spec_no_cross():
    return {
        "population_size": [100],
        "selection": ["roulette"],
        "mutation": ["single_swap"],
        "crossover": ["noop"],
        "succession": ["best_then_random"],
        "iters": [15000],
        "input_file": ["graphs/320_0.009_1.rgraph"],
    }


def v320_no_cross_eval():
    prefix = "results/320_009_1_no_cross/"
    tries = 1
    spec = get_v320_spec_no_cross()

    ev.evaluate(ev.generate_configs(spec), prefix, tries)


def v320_no_cross_plot():
    prefix = "results/320_009_1_no_cross/"
    spec = get_v320_spec_no_cross()
    gb = "crossover"

    configs = ev.generate_configs(spec, group_by=gb)
    dp.draw_plots(configs, dp.line_plot_builder, groupped_by=gb, prefix=prefix)
    dp.draw_plots(configs, dp.box_plot_builder, groupped_by=gb, prefix=prefix)


def get_v180():
    return {
        "population_size": [100],
        "selection": ["roulette"],
        "mutation": ["single_swap"],
        "crossover": ["single_pmx"],
        "succession": ["best_then_random"],
        "iters": [20000],
        "input_file": ["graphs/180_0.018_2.rgraph"],
    }


def v180_eval():
    prefix = "results/180_0018_2/"
    tries = 1
    spec = get_v180()

    ev.evaluate(ev.generate_configs(spec), prefix, tries)


def v180_plot():
    prefix = "results/180_0018_2/"
    spec = get_v180()
    gb = "crossover"

    configs = ev.generate_configs(spec, group_by=gb)
    dp.draw_plots(configs, dp.line_plot_builder, groupped_by=gb, prefix=prefix)
    dp.draw_plots(configs, dp.box_plot_builder, groupped_by=gb, prefix=prefix)


def tree_config():
    return {
        "population_size": [100],
        "selection": ["roulette"],
        "mutation": ["single_swap"],
        "crossover": ["multi_injection"],
        "succession": ["best_then_random"],
        "iters": [5000],
        "ffs": [4],
        "input_file": ["graphs/tree.rtree"],
    }


def tree_eval():
    prefix = "results/150_tree/"
    spec = tree_config()
    fiters = 10

    ev.evaluate(ev.generate_configs(spec), prefix, fiters)


def tree_plot(gb="crossover"):
    prefix = "results/150_tree/"
    spec = tree_config()

    configs = ev.generate_configs(spec, group_by=gb)
    dp.draw_plots(configs, dp.line_plot_builder, groupped_by=gb, prefix=prefix)
    dp.draw_plots(configs, dp.box_plot_builder, groupped_by=gb, prefix=prefix)

if __name__ == "__main__":
    pass
