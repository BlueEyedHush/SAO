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
