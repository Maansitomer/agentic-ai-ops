def finance_agent_node(state):
    """
    Finance Agent (Proximity-Aware)
    -------------------------------
    Detects billing/payment stress and early financial drift.
    """

    signals = state.get("engineered_signals", [])
    risk_state = state.get("risk_state", {})

    fin_p75 = risk_state["financial_stress"]["p75"]

    high_risk = []
    near_risk = []

    for row in signals:
        value = row["financial_stress"]
        if value >= fin_p75:
            high_risk.append(row)
        elif value >= 0.8 * fin_p75:
            near_risk.append(row)

    total = max(len(signals), 1)
    high_ratio = len(high_risk) / total
    near_ratio = len(near_risk) / total

    if high_ratio >= 0.25:
        severity = "high"
        status = "risk_detected"
        diagnosis = "Significant billing or payment stress detected"
        confidence = 0.9
    elif near_ratio >= 0.2:
        severity = "medium"
        status = "early_warning"
        diagnosis = "Customers drifting toward financial stress"
        confidence = 0.7
    else:
        severity = "low"
        status = "stable"
        diagnosis = "Financial metrics within normal range"
        confidence = 0.4

    state["agent_outputs"]["finance"] = {
        "agent": "finance",
        "status": status,
        "severity": severity,
        "confidence": confidence,
        "high_risk_ratio": round(high_ratio, 2),
        "near_risk_ratio": round(near_ratio, 2),
        "diagnosis": diagnosis,
    }

    return state
