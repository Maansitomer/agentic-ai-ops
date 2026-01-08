import pandas as pd


def compute_amplification(df: pd.DataFrame) -> pd.DataFrame:
    """
    Captures stress amplification effects.
    """

    df_amp = pd.DataFrame(index=df.index)

    stress_cols = [
        col for col in df.columns
        if "stress" in col.lower() or "volatility" in col.lower()
    ]

    if not stress_cols:
        return df_amp

    df_amp["stress_count"] = (df[stress_cols] > 0).sum(axis=1)
    df_amp["amplification_score"] = df_amp["stress_count"] ** 2

    return df_amp
