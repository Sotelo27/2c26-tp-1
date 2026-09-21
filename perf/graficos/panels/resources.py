import matplotlib.pyplot as plt
import pandas as pd
from render import connect_nulls, elapsed_seconds, legend_table, percent_axis, time_axis
from styles import AMARILLO, VERDE_GRAFANA
from transforms import keep_last_value, derivative, as_percent, remove_below_value

MEMORY_32GB = 34_359_738_368

def generate_resources_plot(cadvisor_dataframe: pd.DataFrame, meta: dict, output_path: str):
    cpu = cadvisor_dataframe["stats.gauges.cadvisor.exchange-api-1.cpu_cumulative_usage"].copy()
    memory = cadvisor_dataframe["stats.gauges.cadvisor.exchange-api-1.memory_working_set"].copy()

    cpu = keep_last_value(cpu, 100)
    cpu = derivative(cpu)
    cpu = as_percent(cpu, 10_000_000_000)
    cpu = remove_below_value(cpu, 0.0001)

    memory = as_percent(memory, max_value=MEMORY_32GB)

    fig, ax = plt.subplots(figsize=(10, 3))

    for series, label, color in ((cpu, "CPU", VERDE_GRAFANA), (memory, "Memory", AMARILLO)):
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
    percent_axis(ax)
    legend_table(ax, [("CPU", VERDE_GRAFANA, cpu), ("Memory", AMARILLO, memory)])

    ax.set_title("Resources")
    ax.grid(True, linestyle="--", alpha=0.3)

    fig.savefig(f"{output_path}/resources.pdf", format="pdf", bbox_inches="tight")
    plt.close(fig)
