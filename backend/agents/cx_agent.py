def cx_agent_node(state):
    """
    CX Agent (Proximity-Aware)
    -------------------------
    Detects customer frustration and early dissatisfaction.
    """

    signals = state.get("engineered_signals", [])
    risk_state = state.get("risk_state", {})

    cx_p75 = risk_state["cx_stress"]["p75"]

    high_risk = []
    near_risk = []

    for row in signals:
        value = row["cx_stress"]
        if value >= cx_p75:
            high_risk.append(row)
        elif value >= 0.8 * cx_p75:
            near_risk.append(row)

    total = max(len(signals), 1)
    high_ratio = len(high_risk) / total
    near_ratio = len(near_risk) / total

    if high_ratio >= 0.25:
        severity = "high"
        status = "risk_detected"
        diagnosis = "Widespread customer dissatisfaction detected"
        confidence = 0.85
    elif near_ratio >= 0.2:
        severity = "medium"
        status = "early_warning"
        diagnosis = "Early signs of customer frustration emerging"
        confidence = 0.65
    else:
        severity = "low"
        status = "stable"
        diagnosis = "Customer experience remains stable"
        confidence = 0.4

    state["agent_outputs"]["cx"] = {
        "agent": "cx",
        "status": status,
        "severity": severity,
        "confidence": confidence,
        "high_risk_ratio": round(high_ratio, 2),
        "near_risk_ratio": round(near_ratio, 2),
        "diagnosis": diagnosis,
    }

    return state
