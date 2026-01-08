import pandas as pd


def strategy_agent_node(state):
    """
    Strategy Agent:
    - Identifies WHO needs attention
    - Ranks customers by risk proximity
    - Produces Ops-ready prioritization
    """

    features_df = state.get("features_df")
    risk_state = state.get("risk_state")
    agent_outputs = state.get("agent_outputs", {})

    # If no customer-level data, fallback gracefully
    if features_df is None or not isinstance(features_df, pd.DataFrame):
        state["final_decision"]["prioritization"] = []
        return state

    df = features_df.copy()

    # --- Thresholds from population risk ---
    ops_threshold = risk_state["ops_stress"]["p90"]
    fin_threshold = risk_state["financial_stress"]["p90"]
    cx_threshold = risk_state["cx_stress"]["p90"]

    # --- Risk proximity (continuous, early warning) ---
    df["ops_proximity"] = df["ops_stress"] / ops_threshold
    df["finance_proximity"] = df["financial_stress"] / fin_threshold
    df["cx_proximity"] = df["cx_stress"] / cx_threshold

    # Cap values for stability
    df[["ops_proximity", "finance_proximity", "cx_proximity"]] = (
        df[["ops_proximity", "finance_proximity", "cx_proximity"]]
        .clip(upper=1.5)
    )

    # --- Priority score ---
    df["priority_score"] = (
        0.45 * df["ops_proximity"] +
        0.35 * df["finance_proximity"] +
        0.20 * df["cx_proximity"]
    )

    # --- Primary driver ---
    def driver(row):
        scores = {
            "operations": row["ops_proximity"],
            "finance": row["finance_proximity"],
            "cx": row["cx_proximity"]
        }
        return max(scores, key=scores.get)

    df["primary_driver"] = df.apply(driver, axis=1)

    # --- Select TOP customers ---
    top_customers = (
        df.sort_values("priority_score", ascending=False)
        .head(5)
        .loc[:, [
            "customer_id",
            "priority_score",
            "primary_driver",
            "ops_stress",
            "financial_stress",
            "cx_stress"
        ]]
        .to_dict(orient="records")
    )

    # --- Attach to final decision ---
    state["final_decision"]["top_customers_today"] = top_customers
    state["final_decision"]["prioritization_logic"] = "risk_proximity_ranking"

    return state
