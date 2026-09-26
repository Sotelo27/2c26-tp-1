import matplotlib.pyplot as plt
import pandas as pd
from render import currency_axis, format_currency, legend_table, plot_stacked_bars, time_axis
from styles import color_clasico
from transforms import alias_by_metric

EXCHANGE = "stats_counts.exchange"
VOLUME = f"{EXCHANGE}.volume."
NET = f"{EXCHANGE}.net."

def generate_currency_plot(currency_dataframe: pd.DataFrame, meta: dict, output_path: str):
    _generate_currency_plot(currency_dataframe, meta, output_path, VOLUME, "Currency (USD)", "currency")

def generate_net_currency_plot(currency_dataframe: pd.DataFrame, meta: dict, output_path: str):
    _generate_currency_plot(currency_dataframe, meta, output_path, NET, "Net Currency (USD)", "net_currency", cero=True)

def _generate_currency_plot(currency_dataframe, meta, output_path, prefix, title, filename, cero=False):
    series = [
        (name, color_clasico(i), values)
        for i, (name, values) in enumerate(alias_by_metric(currency_dataframe, prefix))
    ]

    fig, ax = plt.subplots(figsize=(10, 3))

    plot_stacked_bars(ax, series, meta)

    if cero:
        ax.axhline(0, color="black", linewidth=0.5, alpha=0.4)

    time_axis(ax, meta)
    currency_axis(ax)
    legend_table(ax, series, format_currency, calcs=("sum", "mean", "max"))

    ax.set_title(title)
    ax.set_axisbelow(True)
    ax.grid(True, linestyle="--", alpha=0.3)

    fig.savefig(f"{output_path}/{filename}.pdf", format="pdf", bbox_inches="tight")
    plt.close(fig)
