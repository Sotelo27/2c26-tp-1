import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

MARKER_SIZE = 4
LINE_WIDTH = 1
FILL_ALPHA = 0.1
BAR_WIDTH = 0.6

def connect_nulls(series: pd.Series) -> pd.Series:
    return series.dropna()

def elapsed_seconds(index: pd.DatetimeIndex, start: int) -> np.ndarray:
    t0 = pd.to_datetime(start, unit="s")
    return (index - t0).total_seconds().to_numpy()

def plot_series(ax, series: pd.Series, meta: dict, label: str, color: str):
    points = connect_nulls(series)
    if points.empty:
        return
    seconds = elapsed_seconds(points.index, meta["start"])
    ax.plot(
        seconds,
        points,
        label=label,
        color=color,
        marker="o",
        markersize=MARKER_SIZE,
        linewidth=LINE_WIDTH,
    )
    ax.fill_between(seconds, points, color=color, alpha=FILL_ALPHA)

def plot_stacked_bars(ax, entries: list[tuple[str, str, pd.Series]], meta: dict):
    index = None
    for _, _, series in entries:
        index = series.index if index is None else index.union(series.index)
    if index is None or index.empty:
        return

    seconds = elapsed_seconds(index, meta["start"])
    arriba = np.zeros(len(index))
    abajo = np.zeros(len(index))

    for _, color, series in entries:
        values = series.reindex(index).fillna(0.0).to_numpy(dtype=float)
        positivos = np.where(values > 0, values, 0.0)
        negativos = np.where(values < 0, values, 0.0)
        for altura, base in ((positivos, arriba), (negativos, abajo)):
            ax.bar(
                seconds,
                altura,
                bottom=base,
                width=BAR_WIDTH,
                align="center",
                color=color,
                linewidth=0,
            )
        arriba = arriba + positivos
        abajo = abajo + negativos

def time_axis(ax, meta: dict):
    ax.set_xlim(0, meta["end"] - meta["start"])
    ax.set_xlabel("Tiempo (s)")

def value_axis(ax, tick_format, bottom=0):
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: tick_format(v)))
    if bottom is not None:
        ax.set_ylim(bottom=bottom)

def percent_axis(ax):
    value_axis(ax, lambda v: f"{v:g}%")

def ms_axis(ax):
    value_axis(ax, lambda v: f"{v:g} ms")

def short_axis(ax):
    value_axis(ax, lambda v: f"{v:g}")

def currency_axis(ax):
    value_axis(ax, format_currency, bottom=None)

def format_percent(value: float) -> str:
    return f"{value:#.3g}".rstrip(".") + "%"

def format_ms(value: float) -> str:
    return f"{value:#.3g}".rstrip(".") + " ms"

def format_short(value: float) -> str:
    return f"{value:.3g}"

def format_currency(value: float) -> str:
    signo = "-" if value < 0 else ""
    magnitud = abs(value)
    if magnitud >= 1_000_000:
        return f"{signo}${magnitud / 1e6:g}M"
    if magnitud >= 1_000:
        return f"{signo}${magnitud / 1e3:g}K"
    return f"{signo}${magnitud:g}"

def legend_table(ax, entries: list[tuple[str, str, pd.Series]], formatter=format_percent):
    visible = [(name, color, series.dropna()) for name, color, series in entries]
    visible = [entry for entry in visible if not entry[2].empty]
    if not visible:
        return

    rows = []
    for name, _, valid in visible:
        rows.append((
            name,
            formatter(valid.mean()),
            formatter(valid.iloc[-1]),
            formatter(valid.max()),
        ))

    headers = ("Name", "Mean", "Last *", "Max")
    widths = [max(len(headers[i]), *(len(row[i]) for row in rows)) for i in range(4)]
    def line(cells):
        return "  ".join(c.ljust(w) for c, w in zip(cells, widths))

    handles = [Line2D([], [], linestyle="none")]
    labels = [line(headers)]
    for (name, color, _), row in zip(visible, rows):
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

def legend_list(ax, entries: list[tuple[str, str, pd.Series]]):
    if not entries:
        return
    ax.legend(
        [Patch(color=color) for _, color, _ in entries],
        [name for name, _, _ in entries],
        loc="upper center",
        bbox_to_anchor=(0.5, -0.2),
        ncol=len(entries),
        frameon=False,
        prop={"size": 8},
    )
