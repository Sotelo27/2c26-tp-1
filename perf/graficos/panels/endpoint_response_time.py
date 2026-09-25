import matplotlib.pyplot as plt
import pandas as pd
from render import format_duration_ms, legend_table, log_ms_axis, plot_series, time_axis
from styles import color_clasico
from transforms import alias_by_node, exclude, remove_below_value

LATENCY = "stats.timers.exchange.latency."
PERCENTIL = ".upper_95"
EXCLUIDO = "accounts_balance"
# Todo aclarar que es P95
def generate_endpoint_response_time_plot(latency_dataframe: pd.DataFrame, meta: dict, output_path: str):
    series = [
        (name, color_clasico(i), values)
        for i, (name, values) in enumerate(
            exclude(alias_by_node(latency_dataframe, LATENCY, PERCENTIL), EXCLUIDO)
        )
    ]

    fig, ax = plt.subplots(figsize=(10, 3))

    for label, color, values in series:
        plot_series(ax, remove_below_value(values, 0), meta, label, color)

    time_axis(ax, meta)
    log_ms_axis(ax)
    legend_table(ax, series, format_duration_ms)

    ax.set_title("Response Time by Endpoint (server-side)")
    ax.grid(True, linestyle="--", alpha=0.3)

    fig.savefig(f"{output_path}/endpoint_response_time.pdf", format="pdf", bbox_inches="tight")
    plt.close(fig)
