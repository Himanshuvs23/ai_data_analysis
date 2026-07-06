# Import Libraries
import json
import pandas as pd
from typing import Dict

def load_dataset(
    path: str
) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [
        col.lower().strip().replace(" ", "_")
        for col in df.columns
    ]
    return df

def load_col_descriptions(
    path: str
) -> Dict:
    with open(path, "r", encoding = "utf-8") as f:
        return json.load(f)