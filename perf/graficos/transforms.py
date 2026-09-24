import re
import pandas as pd
import numpy as np

def keep_last_value(series: pd.Series, limit: int = 100) -> pd.Series:
    return series.ffill(limit=limit)

def derivative(series: pd.Series) -> pd.Series:
    return series.diff()

def as_percent(series: pd.Series, max_value: float) -> pd.Series:
    return (series / max_value) * 100.0

def remove_below_value(series: pd.Series, threshold: float = 0.0001) -> pd.Series:
    return series.mask(series < threshold, np.nan)

def alias_by_metric(dataframe: pd.DataFrame, prefix: str) -> list[tuple[str, pd.Series]]:
    columns = [
        c for c in dataframe.columns
        if c.startswith(prefix) and "." not in c[len(prefix):]
    ]
    return [(c.rsplit(".", 1)[-1], dataframe[c]) for c in columns]

def sum_matching(dataframe: pd.DataFrame, prefix: str, pattern: str) -> pd.Series:
    columns = [c for c in dataframe.columns if c.startswith(prefix) and re.search(pattern, c)]
    if not columns:
        return pd.Series(dtype=float)
    return dataframe[columns].sum(axis=1, min_count=1)