from backend.data.loader import load_customer_data
from backend.intelligence.risk_proximity import compute_customer_risk_scores
from backend.intelligence.usage_signals import compute_usage_signals
from backend.intelligence.operational_signals import compute_operational_signals
from backend.intelligence.financial_signals import compute_financial_signals
from backend.intelligence.risk_representation import (
    compute_cx_stress,
    build_risk_state,
    compute_amplification_score,
)


def build_features():
    """
    Feature Builder (Orchestrator)
    ------------------------------
    Coordinates all signal modules and returns:
    - Engineered customer-level features
    - Global risk state for agent reasoning
    """

    # Load raw data
    df = load_customer_data()

    # Signal computation
    df = compute_usage_signals(df)
    df = compute_operational_signals(df)
    df = compute_financial_signals(df)
    df = compute_cx_stress(df)

    # Columns used for global risk context
    risk_columns = [
        "usage_mean",
        "usage_std",
        "usage_volatility",
        "ops_stress",
        "financial_stress",
        "cx_stress",
    ]

    # Global risk statistics
    risk_state = build_risk_state(df, risk_columns)

    # Amplification logic
    df = compute_amplification_score(df, risk_state)

    df = compute_customer_risk_scores(df, risk_state)
    
    required_columns = [
    "customer_id",
    "usage_mean",
    "usage_std",
    "usage_volatility",
    "ops_stress",
    "financial_stress",
    "cx_stress",
    "amplification_score",
    ]

# Include customer_risk_score ONLY if it exists
    if "customer_risk_score" in df.columns:
        required_columns.append("customer_risk_score")

    features_df = df[required_columns].copy()

    return features_df, risk_state

    
