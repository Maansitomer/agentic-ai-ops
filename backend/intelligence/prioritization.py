def prioritize_customers(df, top_k=10):
    """
    Selects the most risky customers for immediate attention.
    """

    if "customer_risk_score" not in df.columns:
        raise ValueError("customer_risk_score missing for prioritization")

    prioritized = (
        df.sort_values("customer_risk_score", ascending=False)
          .head(top_k)
          .copy()
    )

    return prioritized
