import pandas as pd


def compute_cx_stress(df: pd.DataFrame) -> pd.DataFrame:
    """
    Customer experience stress
    --------------------------
    Combines complaints with unstable behavior
    """

    df["cx_stress"] = df["service_tickets"] * df["usage_volatility"]
    return df


def build_risk_state(df: pd.DataFrame, columns: list) -> dict:
    """
    Global risk distribution
    ------------------------
    Provides statistical context for agents
    """

    risk_state = {}

    for col in columns:
        risk_state[col] = {
            "mean": float(df[col].mean()),
            "p75": float(df[col].quantile(0.75)),
            "p90": float(df[col].quantile(0.90)),
            "max": float(df[col].max()),
        }

    return risk_state


def compute_amplification_score(
    df: pd.DataFrame, risk_state: dict
) -> pd.DataFrame:
    """
    Multi-stress amplification indicator
    -----------------------------------
    Counts how many stress dimensions exceed p75
    """

    df["amplification_score"] = (
        (df["ops_stress"] > risk_state["ops_stress"]["p75"]).astype(int)
        + (df["financial_stress"] > risk_state["financial_stress"]["p75"]).astype(int)
        + (df["cx_stress"] > risk_state["cx_stress"]["p75"]).astype(int)
    )

    return df
