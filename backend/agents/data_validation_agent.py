def data_validation_agent_node(state):
    """
    Data Validation Agent
    ---------------------
    Responsibilities:
    - Validate reliability of engineered signals
    - Detect abnormal distributions or missing data
    - Adjust system trust level
    """

    risk_state = state.get("risk_state", {})
    engineered_signals = state.get("engineered_signals", [])

    validation_output = {
        "agent": "data_validation",
        "data_trust": "high",
        "issues_detected": False,
        "confidence_adjustment": 1.0,
        "notes": "Data appears consistent and reliable."
    }

    # Safety check
    if not risk_state or not engineered_signals:
        validation_output.update({
            "data_trust": "low",
            "issues_detected": True,
            "confidence_adjustment": 0.5,
            "notes": "Insufficient data available for validation."
        })
        state["agent_outputs"]["data_validation"] = validation_output
        return state

    # Simple distribution sanity checks
    anomalies = []

    for feature, stats in risk_state.items():
        mean = stats.get("mean", 0)
        p90 = stats.get("p90", 0)
        max_val = stats.get("max", 0)

        # Detect suspiciously extreme max
        if p90 > 0 and max_val > 3 * p90:
            anomalies.append(feature)

    if anomalies:
        validation_output.update({
            "data_trust": "medium",
            "issues_detected": True,
            "confidence_adjustment": 0.75,
            "notes": f"Potential distribution anomalies detected in: {anomalies}"
        })

    state["agent_outputs"]["data_validation"] = validation_output
    return state
