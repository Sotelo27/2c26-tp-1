import matplotlib.pyplot as plt
import pandas as pd
from render import format_duration_ms, legend_table, ms_axis, plot_series, time_axis
from styles import FIJO_AMARILLO, FIJO_ROJO, FIJO_VERDE

SERVER = "stats.gauges.artillery-api"

def generate_response_time_plot(artillery_dataframe: pd.DataFrame, meta: dict, output_path: str):
    series = [
        ("P99", FIJO_ROJO, artillery_dataframe[f"{SERVER}.scenarioDuration.p99"]),
        ("P95", FIJO_AMARILLO, artillery_dataframe[f"{SERVER}.scenarioDuration.p95"]),
        ("P50", FIJO_VERDE, artillery_dataframe[f"{SERVER}.scenarioDuration.p50"]),
    ]

    fig, ax = plt.subplots(figsize=(10, 3))

    for label, color, values in series:
        plot_series(ax, values, meta, label, color)

    time_axis(ax, meta)
    ms_axis(ax)
    legend_table(ax, series, format_duration_ms)

    ax.set_title("Response Time (client-side)")
    ax.grid(True, linestyle="--", alpha=0.3)

    fig.savefig(f"{output_path}/response_time.pdf", format="pdf", bbox_inches="tight")
    plt.close(fig)
