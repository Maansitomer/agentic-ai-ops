# backend/agents/evaluation_agent.py

from typing import Dict
from backend.utils.state_sanitizer import sanitize_state  # ✅ REQUIRED


def evaluation_agent_node(state: Dict) -> Dict:
    """
    Evaluation Agent
    ----------------
    Evaluates reliability of the final decision based on:
    - Cross-agent agreement
    - Presence of actions
    - Data validation trust
    """

    agent_outputs = state.get("agent_outputs", {})
    final_decision = state.get("final_decision", {})

    # ----------------------------
    # 1. Identify high severity agents
    # ----------------------------
    high_severity_agents = [
        name
        for name, output in agent_outputs.items()
        if isinstance(output, dict)
        and output.get("severity") == "high"
    ]

    agreement_score = len(high_severity_agents)

    if agreement_score >= 2:
        agreement_level = "high"
    elif agreement_score == 1:
        agreement_level = "medium"
    else:
        agreement_level = "low"

    # ----------------------------
    # 2. Actions present check
    # ----------------------------
    action_agent = agent_outputs.get("action_explainability", {})
    actions_present = bool(
        isinstance(action_agent, dict) and action_agent.get("actions")
    )

    # ----------------------------
    # 3. Data trust
    # ----------------------------
    data_validation = agent_outputs.get("data_validation", {})
    data_trust = (
        data_validation.get("data_trust")
        if isinstance(data_validation, dict)
        else "unknown"
    )

    # ----------------------------
    # 4. Decision confidence (UNCHANGED LOGIC)
    # ----------------------------
    decision_confidence = round(
        min(
            0.95,
            0.4
            + 0.2 * agreement_score
            + (0.2 if actions_present else 0)
            + (0.1 if data_trust == "high" else 0),
        ),
        2,
    )

    # ----------------------------
    # 5. Verdict (UNCHANGED LOGIC)
    # ----------------------------
    if agreement_level == "high" and actions_present:
        verdict = "RELIABLE"
    elif agreement_level in {"medium", "high"}:
        verdict = "RELIABLE_WITH_CAUTION"
    else:
        verdict = "NEEDS_REVIEW"

    # ----------------------------
    # 6. Store output (SAFE)
    # ----------------------------
    agent_outputs["evaluation"] = {
        "agent": "evaluation",
        "agreement_score": agreement_score,
        "agreement_level": agreement_level,
        "decision_confidence": decision_confidence,
        "verdict": verdict,
        "notes": {
            "high_severity_agents": high_severity_agents,
            "actions_present": actions_present,
            "data_trust": data_trust,
        },
    }

    state["agent_outputs"] = agent_outputs

    # 🔒 CRITICAL: prevent LangGraph concurrent key updates
    return sanitize_state(state)
