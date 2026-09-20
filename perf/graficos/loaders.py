import json
import numpy as np
import pandas as pd

def load_cadvisor_dataframe(file_path: str) -> pd.DataFrame:
    df_raw = load_raw_json_to_dataframe(file_path)
    df_clean = apply_null_policies(df_raw, CADVISOR_METRIC_POLICIES, default_policy="ffill")
    return df_clean

NULL_POLICIES = {
    "zero": lambda s: s.fillna(0),
    "ffill": lambda s: s.ffill(),
    "gap": lambda s: s.replace({None: np.nan}),
}

CADVISOR_METRIC_POLICIES = {
    # Métricas de consumo de recursos (Gauges -> ffill para mantener continuidad)
    "cpu_usage": "ffill",
    "memory_usage": "ffill",
    "memory_working_set": "ffill",
    "fs_usage": "ffill",
    # Métricas de tráfico/operaciones (Counters / Rates -> zero si hay caída puntual)
    "rx_bytes": "zero",
    "tx_bytes": "zero",
    "network_errors": "zero",
}

def load_raw_json_to_dataframe(file_path: str) -> pd.DataFrame:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    series_dict = {}
    for entry in data:
        name = entry.get("target", "value")
        datapoints = entry.get("datapoints", [])
        if datapoints:
            temp_df = pd.DataFrame(datapoints, columns=[name, "timestamp"])
            temp_df["timestamp"] = pd.to_datetime(temp_df["timestamp"], unit="s")
            temp_df.set_index("timestamp", inplace=True)
            series_dict[name] = temp_df[name]
    return pd.DataFrame(series_dict)

def apply_null_policies(df: pd.DataFrame, policy_map: dict[str, str], default_policy: str = "gap") -> pd.DataFrame:
    df_clean = df.copy()
    for col in df_clean.columns:
        policy_key = policy_map.get(col, default_policy)
        if policy_key in NULL_POLICIES:
            df_clean[col] = NULL_POLICIES[policy_key](df_clean[col])
    return df_clean