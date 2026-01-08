from backend.utils.state_sanitizer import sanitize_state 
def synthesis_agent_node(state):
    """
    Synthesis Agent
    ----------------
    Responsibilities:
    - Combine Ops, Finance, and CX agent outputs
    - Detect agreement or conflict
    - Produce a final, business-readable decision
    """

    agent_outputs = state.get("agent_outputs", {})

    ops = agent_outputs.get("operations", {})
    fin = agent_outputs.get("finance", {})
    cx = agent_outputs.get("cx", {})

    # Default final decision
    final_decision = {
        "overall_status": "unknown",
        "attention_required": False,
        "primary_driver": None,
        "summary": "Insufficient information to make a decision.",
        "confidence": 0.0
    }

    # Extract severities
    severities = {
        "operations": ops.get("severity"),
        "finance": fin.get("severity"),
        "cx": cx.get("severity")
    }

    # Count severities
    high_count = list(severities.values()).count("high")
    medium_count = list(severities.values()).count("medium")

    # Decision logic
    if high_count >= 1:
        final_decision = {
            "overall_status": "critical",
            "attention_required": True,
            "primary_driver": [
                k for k, v in severities.items() if v == "high"
            ],
            "summary": "Critical risk detected requiring immediate attention.",
            "confidence": 0.9
        }

    elif medium_count >= 1:
        final_decision = {
            "overall_status": "warning",
            "attention_required": True,
            "primary_driver": [
                k for k, v in severities.items() if v == "medium"
            ],
            "summary": "Early warning signals detected. Proactive attention recommended.",
            "confidence": 0.7
        }

    else:
        final_decision = {
            "overall_status": "stable",
            "attention_required": False,
            "primary_driver": None,
            "summary": (
                "Operations, finance, and customer experience signals "
                "are within normal ranges today. No immediate attention required."
            ),
            "confidence": 0.85
        }

    # Attach agent agreement snapshot (important for explainability)
    final_decision["agent_agreement"] = severities

    state["final_decision"] = final_decision
    return sanitize_state(state)
