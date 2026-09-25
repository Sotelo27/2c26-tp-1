import math
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from decimal import Decimal, ROUND_HALF_UP
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

MARKER_SIZE = 4
LINE_WIDTH = 1
FILL_ALPHA = 0.1
BAR_WIDTH = 0.6

PASOS_TIEMPO = (
    1, 2, 5, 10, 15, 30,
    60, 120, 300, 600, 900, 1800,
    3600, 7200, 21600, 43200, 86400,
)
TICKS_TIEMPO = 8

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

def paso_tiempo(span: float) -> int:
    for paso in PASOS_TIEMPO:
        if span / paso <= TICKS_TIEMPO:
            return paso
    return PASOS_TIEMPO[-1]

def format_elapsed(seconds: float, span: float) -> str:
    entero = int(round(seconds))
    if span < 60:
        return f"{entero}"
    if span < 3600:
        return f"{entero // 60}:{entero % 60:02d}"
    return f"{entero // 3600}:{entero // 60 % 60:02d}:{entero % 60:02d}"

def time_axis(ax, meta: dict):
    span = meta["end"] - meta["start"]
    if span < 60:
        etiqueta = "Tiempo (s)"
    elif span < 3600:
        etiqueta = "Tiempo (min:s)"
    else:
        etiqueta = "Tiempo (h:min:s)"

    ax.set_xlim(0, span)
    ax.xaxis.set_major_locator(mticker.MultipleLocator(paso_tiempo(span)))
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: format_elapsed(v, span)))
    ax.set_xlabel(etiqueta)

SUFIJOS_CORTOS = ("", " K", " Mil", " Bil", " Tri")

ESCALAS_DURACION = (
    (1.0, " ms"),
    (1_000.0, " s"),
    (60_000.0, " min"),
    (3_600_000.0, " hour"),
)

def format_number(value: float) -> str:
    if not np.isfinite(value):
        return "-"
    decimales = 0 if value % 1 == 0 else max(0, 2 - math.floor(math.log10(abs(value))))
    paso = Decimal(1).scaleb(-decimales)
    return f"{Decimal(value).quantize(paso, rounding=ROUND_HALF_UP):.{decimales}f}"

def format_percent(value: float) -> str:
    return format_number(value) + "%"

def format_short(value: float) -> str:
    magnitud = abs(value)
    escala = 0
    while magnitud >= 1000 and escala < len(SUFIJOS_CORTOS) - 1:
        magnitud /= 1000.0
        escala += 1
    signo = "-" if value < 0 else ""
    return f"{signo}{format_number(magnitud)}{SUFIJOS_CORTOS[escala]}"

def format_duration_ms(value: float) -> str:
    magnitud = abs(value)
    divisor, sufijo = ESCALAS_DURACION[0]
    for candidato, unidad in ESCALAS_DURACION:
        if magnitud >= candidato:
            divisor, sufijo = candidato, unidad
    signo = "-" if value < 0 else ""
    return f"{signo}{format_number(magnitud / divisor)}{sufijo}"

def format_currency(value: float) -> str:
    signo = "-" if value < 0 else ""
    magnitud = abs(value)
    if magnitud >= 1_000_000:
        return f"{signo}${format_number(magnitud / 1e6)}M"
    if magnitud >= 1_000:
        return f"{signo}${format_number(magnitud / 1e3)}K"
    return f"{signo}${format_number(magnitud)}"

def value_axis(ax, tick_format, bottom=0):
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: tick_format(v)))
    if bottom is not None:
        ax.set_ylim(bottom=bottom)

def percent_axis(ax):
    value_axis(ax, format_percent)

def ms_axis(ax):
    value_axis(ax, format_duration_ms)

def short_axis(ax):
    value_axis(ax, format_short)

def log_axis(ax, tick_format):
    ax.set_yscale("log")
    ax.yaxis.set_major_locator(mticker.LogLocator(base=10))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: tick_format(v)))
    ax.yaxis.set_minor_formatter(mticker.NullFormatter())

def log_ms_axis(ax):
    log_axis(ax, format_duration_ms)

def currency_axis(ax):
    value_axis(ax, format_currency, bottom=None)

def legend_table(ax, entries: list[tuple[str, str, pd.Series]], formatter=format_percent, anchor_x=1.02):
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
        bbox_to_anchor=(anchor_x, 1.0),
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
