import matplotlib.pyplot as plt
import pandas as pd
from render import format_short, legend_table, plot_series, short_axis, time_axis
from styles import FIJO_AMARILLO, FIJO_AZUL, FIJO_ROJO, FIJO_VERDE
from transforms import integral, sum_matching

SERVER = "stats.gauges.artillery-api"
CODES = f"{SERVER}.codes."
ERRORS = f"{SERVER}.errors."

def generate_requests_state_plot(artillery_dataframe: pd.DataFrame, meta: dict, output_path: str):
    errors = sum_matching(artillery_dataframe, ERRORS, r".*")
    failed = _add(sum_matching(artillery_dataframe, CODES, r"\.5[0-9]{2}$"), errors)
    salidas = _add(
        artillery_dataframe[f"{SERVER}.scenariosCompleted"],
        artillery_dataframe[f"{SERVER}.scenariosAvoided"],
        errors,
    )
    pending = integral(artillery_dataframe[f"{SERVER}.scenariosCreated"]) - integral(salidas)

    izq = [
        ("Pending", FIJO_AZUL, pending),
        ("Completed", FIJO_VERDE, sum_matching(artillery_dataframe, CODES, r"\.[1-3][0-9]{2}$")),
        ("Limited", FIJO_AMARILLO, sum_matching(artillery_dataframe, CODES, r"\.4[0-9]{2}$")),
        ("Failed", FIJO_ROJO, failed),
    ]

    fig, ax = plt.subplots(figsize=(10, 3))

    for label, color, values in izq:
        plot_series(ax, values, meta, label, color)

    time_axis(ax, meta)
    short_axis(ax)
    legend_table(ax, izq, format_short)

    ax.set_title("Requests State")
    ax.grid(True, linestyle="--", alpha=0.3)

    fig.savefig(f"{output_path}/requests_state.pdf", format="pdf", bbox_inches="tight")
    plt.close(fig)

def _add(*series: pd.Series) -> pd.Series:
    return pd.concat(series, axis=1).sum(axis=1, min_count=1)
