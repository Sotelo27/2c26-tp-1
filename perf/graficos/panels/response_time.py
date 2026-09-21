import matplotlib.pyplot as plt
import pandas as pd
from render import connect_nulls, elapsed_seconds, format_ms, legend_table, ms_axis, time_axis
from styles import AMARILLO_GRAFANA, VERDE_GRAFANA

def generate_response_time_plot(artillery_dataframe: pd.DataFrame, meta: dict, output_path: str):
    upper = artillery_dataframe["stats.gauges.artillery-api.scenarioDuration.max"].copy()
    median = artillery_dataframe["stats.gauges.artillery-api.scenarioDuration.median"].copy()

    fig, ax = plt.subplots(figsize=(10, 3))

    for series, label, color in ((upper, "Upper", VERDE_GRAFANA), (median, "Median", AMARILLO_GRAFANA)):
        points = connect_nulls(series)
        seconds = elapsed_seconds(points.index, meta["start"])
        ax.plot(
            seconds,
            points,
            label=label,
            color=color,
            marker="o",
            markersize=4,
            linewidth=1,
        )
        ax.fill_between(seconds, points, color=color, alpha=0.1)

    time_axis(ax, meta)
    ms_axis(ax)
    legend_table(ax, [("Upper", VERDE_GRAFANA, upper), ("Median", AMARILLO_GRAFANA, median)], format_ms)

    ax.set_title("Response time (client-side)")
    ax.grid(True, linestyle="--", alpha=0.3)

    fig.savefig(f"{output_path}/response_time.pdf", format="pdf", bbox_inches="tight")
    plt.close(fig)
