import pandas as pd


def compute_operational_signals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Operational stress signals
    --------------------------
    Captures service reliability issues
    """

    df["ops_stress"] = df["avg_outage_hours"]

    return df
