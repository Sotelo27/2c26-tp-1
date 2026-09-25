import matplotlib.pyplot as plt
import pandas as pd
from render import legend_table, percent_axis, plot_series, time_axis
from styles import FIJO_AMARILLO, FIJO_VERDE
from transforms import bucket_max_rate, as_percent

CONTAINER = "stats.gauges.cadvisor.exchange-api-1"
MEMORY_4GB = 4_294_967_296
NS_POR_CORE_SEGUNDO = 1_000_000_000
BUCKET_SEGUNDOS = 10
LEYENDA_X = 1.08

def generate_resources_plot(cadvisor_dataframe: pd.DataFrame, meta: dict, output_path: str):
    cpu = cadvisor_dataframe[f"{CONTAINER}.cpu_cumulative_usage"].copy()
    memory = cadvisor_dataframe[f"{CONTAINER}.memory_working_set"].copy()

    cpu = bucket_max_rate(cpu, BUCKET_SEGUNDOS)
    cpu = as_percent(cpu, NS_POR_CORE_SEGUNDO)

    memory = as_percent(memory, max_value=MEMORY_4GB)

    series = [
        ("CPU", FIJO_VERDE, cpu),
        ("Memory", FIJO_AMARILLO, memory),
    ]

    fig, ax = plt.subplots(figsize=(10, 3))
    memory_ax = ax.twinx()

    plot_series(ax, cpu, meta, "CPU", FIJO_VERDE)
    plot_series(memory_ax, memory, meta, "Memory", FIJO_AMARILLO)

    time_axis(ax, meta)
    percent_axis(ax)
    percent_axis(memory_ax)
    legend_table(ax, series, anchor_x=LEYENDA_X)

    ax.set_title("Resources")
    ax.grid(True, linestyle="--", alpha=0.3)

    fig.savefig(f"{output_path}/resources.pdf", format="pdf", bbox_inches="tight")
    plt.close(fig)
