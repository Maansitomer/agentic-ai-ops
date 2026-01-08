import pandas as pd


def compute_financial_signals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Financial stress signals
    ------------------------
    Combines bill size with payment delays
    """

    df["financial_stress"] = df["last_bill_amount"] * (
        1 + df["payment_delay_days"] / 30
    )

    return df
