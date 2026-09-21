import matplotlib.pyplot as plt
import pandas as pd
from render import elapsed_seconds, format_short, legend_table, short_axis, time_axis
from styles import AMARILLO_LIMITED, AZUL_GRAFANA, ROJO_GRAFANA, VERDE_COMPLETED
from transforms import sum_series

SERVER = "stats.gauges.artillery-api"

def generate_requests_state_plot(artillery_dataframe: pd.DataFrame, meta: dict, output_path: str):
    targets = [
        ("Errored", ROJO_GRAFANA, sum_series(artillery_dataframe, f"{SERVER}.errors.")),
        ("Completed", VERDE_COMPLETED, artillery_dataframe.get(f"{SERVER}.codes.200")),
        ("Pending", AZUL_GRAFANA, artillery_dataframe.get(f"{SERVER}.pendingRequests")),
        ("Limited", AMARILLO_LIMITED, artillery_dataframe.get(f"{SERVER}.codes.429")),
    ]
    series = [(label, color, s) for label, color, s in targets if s is not None and not s.empty]

    frame = pd.DataFrame({label: s for label, _, s in series}).dropna(how="all")
    levels = frame.fillna(0).cumsum(axis=1)
    seconds = elapsed_seconds(levels.index, meta["start"])

    fig, ax = plt.subplots(figsize=(10, 3))

    lower = 0.0
    for label, color, _ in series:
        upper = levels[label]
        ax.fill_between(seconds, lower, upper, color=color, alpha=0.7)
        ax.plot(
            seconds,
            upper,
            label=label,
            color=color,
            marker="o",
            markersize=4,
            linewidth=1,
        )
        lower = upper

    time_axis(ax, meta)
    short_axis(ax)
    legend_table(ax, [(label, color, frame[label]) for label, color, _ in series], format_short)

    ax.set_title("Requests state (stacked)")
    ax.grid(True, linestyle="--", alpha=0.3)

    fig.savefig(f"{output_path}/requests_state.pdf", format="pdf", bbox_inches="tight")
    plt.close(fig)
