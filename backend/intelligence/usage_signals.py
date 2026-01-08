import numpy as np
import pandas as pd


def compute_usage_signals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Usage behavior signals
    ----------------------
    - Mean usage
    - Usage deviation
    - Volatility (instability indicator)
    """

    df["usage_mean"] = df["monthly_usage_kwh"]

    df["usage_std"] = (df["peak_usage_kwh"] - df["monthly_usage_kwh"]).abs()

    df["usage_volatility"] = df["usage_std"] / (df["usage_mean"] + 1e-6)

    return df
