import matplotlib.pyplot as plt
import pandas as pd
from render import format_short, legend_table, plot_series, short_axis, time_axis
from styles import color_clasico
from transforms import alias_by_metric

SERVER = "stats.gauges.artillery-api"
SCENARIO_COUNTS = f"{SERVER}.scenarioCounts."

def generate_scenarios_plot(artillery_dataframe: pd.DataFrame, meta: dict, output_path: str):
    series = [
        (name, color_clasico(i), values)
        for i, (name, values) in enumerate(alias_by_metric(artillery_dataframe, SCENARIO_COUNTS))
    ]

    fig, ax = plt.subplots(figsize=(10, 3))

    for label, color, values in series:
        plot_series(ax, values, meta, label, color)

    time_axis(ax, meta)
    short_axis(ax)
    legend_table(ax, series, format_short)

    ax.set_title("Scenarios Launched")
    ax.grid(True, linestyle="--", alpha=0.3)

    fig.savefig(f"{output_path}/scenarios.pdf", format="pdf", bbox_inches="tight")
    plt.close(fig)
