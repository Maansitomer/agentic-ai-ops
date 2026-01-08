import pandas as pd
import numpy as np


def _to_python(value):
    """
    Convert numpy scalars to native Python types
    """
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    return value


def compute_customer_risk_scores(df: pd.DataFrame, risk_state: dict) -> pd.DataFrame:
    """
    Compute continuous risk proximity scores for each customer
    """

    df = df.copy()

    df["ops_risk_score"] = df["ops_stress"] / risk_state["ops_stress"]["p75"]
    df["fin_risk_score"] = df["financial_stress"] / risk_state["financial_stress"]["p75"]
    df["cx_risk_score"] = df["cx_stress"] / risk_state["cx_stress"]["p75"]

    df["overall_risk_score"] = (
        0.4 * df["ops_risk_score"]
        + 0.35 * df["fin_risk_score"]
        + 0.25 * df["cx_risk_score"]
    )

    return df


def build_watchlist(df: pd.DataFrame, top_n: int = 5) -> list:
    """
    Build Top-N customer watchlist (JSON safe)
    """

    watchlist_df = (
        df.sort_values("overall_risk_score", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )

    records = watchlist_df[
        [
            "customer_id",
            "overall_risk_score",
            "ops_stress",
            "financial_stress",
            "cx_stress",
            "amplification_score",
        ]
    ].to_dict(orient="records")

    # 🔥 CRITICAL: convert numpy types to Python types
    safe_records = []
    for row in records:
        safe_row = {k: _to_python(v) for k, v in row.items()}
        safe_records.append(safe_row)

    return safe_records
