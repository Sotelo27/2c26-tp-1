import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D

def connect_nulls(series: pd.Series) -> pd.Series:
    return series.dropna()

def elapsed_seconds(index: pd.DatetimeIndex, start: int) -> np.ndarray:
    t0 = pd.to_datetime(start, unit="s")
    return (index - t0).total_seconds().to_numpy()

def time_axis(ax, meta: dict):
    ax.set_xlim(0, meta["end"] - meta["start"])
    ax.set_xlabel("Tiempo (s)")

def value_axis(ax, tick_format):
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: tick_format(v)))
    ax.set_ylim(bottom=0)

def percent_axis(ax):
    value_axis(ax, lambda v: f"{v:g}%")

def ms_axis(ax):
    value_axis(ax, lambda v: f"{v:g} ms")

def format_percent(value: float) -> str:
    return f"{value:.3g}%"

def format_ms(value: float) -> str:
    return f"{value:#.3g}".rstrip(".") + " ms"

def legend_table(ax, entries: list[tuple[str, str, pd.Series]], formatter=format_percent):
    rows = []
    for name, _, series in entries:
        valid = series.dropna()
        rows.append((
            name,
            formatter(valid.mean()),
            formatter(valid.iloc[-1]),
            formatter(valid.max()),
        ))

    headers = ("Name", "Mean", "Last", "Max")
    widths = [max(len(headers[i]), *(len(row[i]) for row in rows)) for i in range(4)]
    def line(cells):
        return "  ".join(c.ljust(w) for c, w in zip(cells, widths))

    handles = [Line2D([], [], linestyle="none")]
    labels = [line(headers)]
    for (name, color, _), row in zip(entries, rows):
        handles.append(Line2D([], [], color=color, linewidth=2))
        labels.append(line(row))

    ax.legend(
        handles,
        labels,
        loc="upper left",
        bbox_to_anchor=(1.02, 1.0),
        frameon=False,
        handlelength=1.2,
        prop={"family": "monospace", "size": 8},
    )
