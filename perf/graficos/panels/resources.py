import matplotlib.pyplot as plt
import pandas as pd
from render import legend_table, percent_axis, plot_series, time_axis
from styles import FIJO_AMARILLO, FIJO_VERDE
from transforms import bucket_max_rate, as_percent

CADVISOR = "stats.gauges.cadvisor"
CONTAINERS = [
    ("exchange-api-1", "resources", "Resources"),
    ("exchange-log-api-1", "resources_log_api", "Resources log-api"),
]
MEMORY_4GB = 4_294_967_296
NS_POR_CORE_SEGUNDO = 1_000_000_000
BUCKET_SEGUNDOS = 10
LEYENDA_X = 1.08

def generate_resources_plot(cadvisor_dataframe: pd.DataFrame, meta: dict, output_path: str):
    for container, file_name, title in CONTAINERS:
        if f"{CADVISOR}.{container}.cpu_cumulative_usage" in cadvisor_dataframe.columns:
            generate_container_resources_plot(cadvisor_dataframe, meta, output_path, container, file_name, title)

def generate_container_resources_plot(cadvisor_dataframe: pd.DataFrame, meta: dict, output_path: str, container: str, file_name: str, title: str):
    cpu = cadvisor_dataframe[f"{CADVISOR}.{container}.cpu_cumulative_usage"].copy()
    memory = cadvisor_dataframe[f"{CADVISOR}.{container}.memory_working_set"].copy()

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

    ax.set_title(title)
    ax.grid(True, linestyle="--", alpha=0.3)

    fig.savefig(f"{output_path}/{file_name}.pdf", format="pdf", bbox_inches="tight")
    plt.close(fig)
