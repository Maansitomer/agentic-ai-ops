# backend/agents/action_explainability_agent.py

from typing import Dict, List
from backend.utils.state_sanitizer import sanitize_state  # ✅ REQUIRED


def _explain_customer(row: Dict, risk_state: Dict) -> List[str]:
    explanations = []

    if row["usage_volatility"] >= risk_state["usage_volatility"]["p90"]:
        explanations.append(
            f"Usage volatility is extremely high ({row['usage_volatility']:.2f}), "
            "above 90th percentile threshold"
        )

    if row["cx_stress"] >= risk_state["cx_stress"]["p90"]:
        explanations.append("Customer experience stress is critically elevated")

    if row["ops_stress"] >= risk_state["ops_stress"]["p75"]:
        explanations.append("Frequent operational disruptions detected")

    if row["financial_stress"] >= risk_state["financial_stress"]["p90"]:
        explanations.append("Financial exposure exceeds high-risk threshold")

    if row.get("amplification_score", 0) >= 2:
        explanations.append("Multiple risk signals are amplifying overall impact")

    return explanations


def _recommend_actions(primary_driver: str) -> List[Dict]:
    if primary_driver == "cx":
        return [
            {
                "team": "Customer Experience",
                "action": "Immediate proactive outreach by senior support agent",
                "priority": "P0",
            },
            {
                "team": "Retention",
                "action": "Assign retention specialist",
                "priority": "P1",
            },
        ]

    if primary_driver == "operations":
        return [
            {
                "team": "Operations",
                "action": "Investigate recurring service instability",
                "priority": "P0",
            },
            {
                "team": "Engineering",
                "action": "Root cause analysis and remediation",
                "priority": "P1",
            },
        ]

    if primary_driver == "finance":
        return [
            {
                "team": "Finance",
                "action": "Review billing and payment anomalies",
                "priority": "P0",
            },
            {
                "team": "Risk",
                "action": "Assess credit exposure",
                "priority": "P1",
            },
        ]

    return [
        {
            "team": "Monitoring",
            "action": "Continue observation",
            "priority": "P2",
        }
    ]


def action_explainability_agent_node(state: Dict) -> Dict:
    """
    Action & Explainability Agent
    -----------------------------
    Acts ONLY on top prioritized customers.
    """

    customers = state.get("engineered_signals", [])
    risk_state = state.get("risk_state")
    agent_outputs = state.get("agent_outputs", {})

    # Defensive exit (graph-safe)
    if not customers or risk_state is None:
        agent_outputs["action_explainability"] = {
            "agent": "action_explainability",
            "actions": [],
            "confidence": 0,
        }
        state["agent_outputs"] = agent_outputs
        return sanitize_state(state)

    # Determine primary driver (UNCHANGED LOGIC)
    if agent_outputs.get("cx", {}).get("severity") == "high":
        primary_driver = "cx"
    elif agent_outputs.get("operations", {}).get("severity") == "high":
        primary_driver = "operations"
    elif agent_outputs.get("finance", {}).get("severity") == "high":
        primary_driver = "finance"
    else:
        primary_driver = "monitoring"

    action_plan = []

    for row in customers:
        explanations = _explain_customer(row, risk_state)
        actions = _recommend_actions(primary_driver)

        action_plan.append(
            {
                "customer_id": row["customer_id"],
                "risk_score": float(row["customer_risk_score"]),
                "risk_level": (
                    "CRITICAL"
                    if row["customer_risk_score"] >= 6.5
                    else "HIGH"
                ),
                "primary_driver": primary_driver,
                "explanation": explanations,
                "recommended_actions": actions,
                "confidence": round(min(0.95, 0.6 + 0.1 * len(explanations)), 2),
            }
        )

    agent_outputs["action_explainability"] = {
        "agent": "action_explainability",
        "actions": action_plan,
        "confidence": round(
            sum(a["confidence"] for a in action_plan) / len(action_plan), 2
        ),
    }

    state["agent_outputs"] = agent_outputs

    # 🔒 CRITICAL: prevent LangGraph key conflicts
    return sanitize_state(state)
