import matplotlib.pyplot as plt
import pandas as pd
from render import legend_table, percent_axis, plot_series, time_axis
from styles import FIJO_AMARILLO, FIJO_VERDE
from transforms import keep_last_value, derivative, as_percent, remove_below_value

CONTAINER = "stats.gauges.cadvisor.exchange-api-1"
MEMORY_2GB = 2_147_483_648

def generate_resources_plot(cadvisor_dataframe: pd.DataFrame, meta: dict, output_path: str):
    cpu = cadvisor_dataframe[f"{CONTAINER}.cpu_cumulative_usage"].copy()
    memory = cadvisor_dataframe[f"{CONTAINER}.memory_working_set"].copy()

    cpu = keep_last_value(cpu, 100)
    cpu = derivative(cpu)
    cpu = as_percent(cpu, 10_000_000_000)
    cpu = remove_below_value(cpu, 0.0001)

    memory = as_percent(memory, max_value=MEMORY_2GB)

    series = [
        ("CPU", FIJO_VERDE, cpu),
        ("Memory", FIJO_AMARILLO, memory),
    ]

    fig, ax = plt.subplots(figsize=(10, 3))

    for label, color, values in series:
        plot_series(ax, values, meta, label, color)

    time_axis(ax, meta)
    percent_axis(ax)
    legend_table(ax, series)

    ax.set_title("Resources")
    ax.grid(True, linestyle="--", alpha=0.3)

    fig.savefig(f"{output_path}/resources.pdf", format="pdf", bbox_inches="tight")
    plt.close(fig)
