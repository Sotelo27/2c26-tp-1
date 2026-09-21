import json
import pandas as pd

def load_cadvisor_dataframe(file_path: str) -> pd.DataFrame:
    return load_raw_json_to_dataframe(file_path)

def load_artillery_dataframe(file_path: str) -> pd.DataFrame:
    return load_raw_json_to_dataframe(file_path)

def load_meta(file_path: str) -> dict:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

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
