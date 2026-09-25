import re
import pandas as pd

def bucket_max_rate(series: pd.Series, seconds: int = 10) -> pd.Series:
    return series.dropna().resample(f"{seconds}s").max().diff() / seconds

def integral(series: pd.Series) -> pd.Series:
    return series.fillna(0.0).cumsum().where(series.notna())

def as_percent(series: pd.Series, max_value: float) -> pd.Series:
    return (series / max_value) * 100.0

def alias_by_metric(dataframe: pd.DataFrame, prefix: str) -> list[tuple[str, pd.Series]]:
    columns = [
        c for c in dataframe.columns
        if c.startswith(prefix) and "." not in c[len(prefix):]
    ]
    return [(c.rsplit(".", 1)[-1], dataframe[c]) for c in columns]

def alias_by_node(dataframe: pd.DataFrame, prefix: str, suffix: str) -> list[tuple[str, pd.Series]]:
    columns = [
        c for c in dataframe.columns
        if c.startswith(prefix) and c.endswith(suffix) and "." not in c[len(prefix):-len(suffix)]
    ]
    return [(c[len(prefix):-len(suffix)], dataframe[c]) for c in columns]

def exclude(entries: list[tuple[str, pd.Series]], pattern: str) -> list[tuple[str, pd.Series]]:
    return [(name, series) for name, series in entries if not re.search(pattern, name)]

def remove_below_value(series: pd.Series, value: float) -> pd.Series:
    return series.where(series > value)

def sum_matching(dataframe: pd.DataFrame, prefix: str, pattern: str) -> pd.Series:
    columns = [c for c in dataframe.columns if c.startswith(prefix) and re.search(pattern, c)]
    if not columns:
        return pd.Series(dtype=float)
    return dataframe[columns].sum(axis=1, min_count=1)