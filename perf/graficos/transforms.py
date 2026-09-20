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