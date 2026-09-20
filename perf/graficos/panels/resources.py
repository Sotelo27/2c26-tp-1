import matplotlib.pyplot as plt
import pandas as pd
from transforms import keep_last_value, derivative, as_percent, remove_below_value

MEMORY_32GB = 34_359_738_368

def generate_resources_plot(cadvisor_dataframe: pd.DataFrame, output_path: str):
    cpu = cadvisor_dataframe["stats.gauges.cadvisor.exchange-api-1.cpu_cumulative_usage"].copy()
    memory = cadvisor_dataframe["stats.gauges.cadvisor.exchange-api-1.memory_working_set"].copy()

    cpu = keep_last_value(cpu, 100)
    cpu = derivative(cpu)
    cpu = as_percent(cpu, 10_000_000_000)
    cpu = remove_below_value(cpu, 0.0001)

    memory = as_percent(memory, max_value=MEMORY_32GB)

    fig, ax = plt.subplots(figsize=(8, 3))

    ax.plot(
        cpu.index,
        cpu,
        label="CPU",
        color="#73BF69",
        marker="o",
        markersize=2,
        linewidth=1,
    )
    ax.plot(
        memory.index,
        memory,
        label="Memory",
        color="#F2C94C",
        marker="o",
        markersize=2,
        linewidth=1,
    )

    ax.fill_between(cpu.index, cpu, color="#73BF69", alpha=0.15)
    ax.fill_between(memory.index, memory, color="#F2C94C", alpha=0.15)

    ax.set_xlabel("Time Stamp")
    ax.set_ylabel("Resources (%)")
    ax.legend(loc="upper right")

    ax.set_title("Resources")
    ax.grid(True, linestyle="--", alpha=0.3)

    fig.savefig(f"{output_path}/resources.pdf", format="pdf", bbox_inches="tight")
    plt.close(fig)
