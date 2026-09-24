import matplotlib.pyplot as plt
import pandas as pd
from render import format_short, legend_table, plot_series, short_axis, time_axis
from styles import FIJO_AMARILLO, FIJO_AZUL, FIJO_ROJO, FIJO_VERDE
from transforms import sum_matching

SERVER = "stats.gauges.artillery-api"
CODES = f"{SERVER}.codes."

def generate_requests_state_plot(artillery_dataframe: pd.DataFrame, meta: dict, output_path: str):
    pending = artillery_dataframe.get(f"{SERVER}.pendingRequests", pd.Series(dtype=float))
    izq = [
        ("Completed", FIJO_VERDE, sum_matching(artillery_dataframe, CODES, r"\.[1-3][0-9]{2}$")),
        ("Limited", FIJO_AMARILLO, sum_matching(artillery_dataframe, CODES, r"\.4[0-9]{2}$")),
        ("Failed", FIJO_ROJO, sum_matching(artillery_dataframe, CODES, r"\.5[0-9]{2}$")),
    ]

    fig, ax = plt.subplots(figsize=(10, 3))

    for label, color, values in izq:
        plot_series(ax, values, meta, label, color)

    if not pending.dropna().empty:
        derecha = ax.twinx()
        plot_series(derecha, pending, meta, "Pending", FIJO_AZUL)
        short_axis(derecha)
        ax.set_zorder(derecha.get_zorder() + 1)
        ax.patch.set_visible(False)

    time_axis(ax, meta)
    short_axis(ax)
    legend_table(ax, [("Pending", FIJO_AZUL, pending)] + izq, format_short)

    ax.set_title("Requests State")
    ax.grid(True, linestyle="--", alpha=0.3)

    fig.savefig(f"{output_path}/requests_state.pdf", format="pdf", bbox_inches="tight")
    plt.close(fig)
