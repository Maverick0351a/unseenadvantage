import pandas as pd

def load_events_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # required columns: event_id, ts, asset, text
    required = {"event_id","ts","asset","text"}
    missing = required - set(df.columns.str.lower())
    # normalize casing
    df.columns = [c.lower() for c in df.columns]
    missing = {c for c in required if c not in set(df.columns)}
    if missing:
        raise ValueError(f"events.csv missing columns: {missing}")
    return df

def load_prices_csv(path: str) -> pd.DataFrame:
    # optional for demo
    return pd.read_csv(path)
