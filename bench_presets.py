import evaluate as ev
import draw_plots as dp


def eval_compare_all():
    return ev.generate_configs(), "results/80_035_2/csv", 10


def plot_compare_all():
    cd = "results/80_035_2/csv/"
    po = "results/80_035_2/plots/"

    for gb in ["mutation", "population_size", "crossover", "selection"]:
        configs = ev.generate_configs({}, group_by=gb)
        dp.draw_plots(configs, dp.line_plot_builder, groupped_by=gb, csv_dir=cd, plot_png_out=po + "l_{}".format(gb))


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
    return ev.generate_configs(get_compare_succession_spec()), "results/succession_comparison_m/csv", 3


def plot_compare_succession():
    cd = "results/succession_comparison_m/csv/"
    po = "results/succession_comparison_m/plots/"
    gb = "succession"
    configs = ev.generate_configs(get_compare_succession_spec(), group_by=gb)
    dp.draw_plots(configs, dp.line_plot_builder, groupped_by=gb, csv_dir=cd, plot_png_out=po + "l")
    dp.draw_plots(configs, dp.box_plot_builder, groupped_by=gb, csv_dir=cd, plot_png_out=po + "bw")
