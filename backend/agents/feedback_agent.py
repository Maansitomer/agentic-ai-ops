# backend/agents/feedback_agent.py

from typing import Dict
from backend.memory.feedback_memory import save_feedback_memory
from backend.utils.state_sanitizer import sanitize_state  # ✅ REQUIRED FIX


def feedback_agent_node(state: Dict) -> Dict:
    """
    Feedback Agent
    --------------
    Captures:
    - Human override (if any)
    - Final decision snapshot
    - Persists feedback memory (append-only)
    """

    agent_outputs = state.get("agent_outputs", {})
    final_decision = state.get("final_decision")

    # Defensive snapshot (UNCHANGED LOGIC)
    final_decision_snapshot = (
        final_decision.copy()
        if isinstance(final_decision, dict) and final_decision
        else {}
    )

    # Placeholder for future human override
    human_override = None

    feedback_payload = {
        "agent": "feedback",
        "human_override": human_override,
        "final_decision_snapshot": final_decision_snapshot,
        "notes": (
            "No human override applied"
            if human_override is None
            else "Human override applied"
        ),
    }

    # 🔒 MEMORY PERSISTENCE (SIDE EFFECT ONLY — NO LOGIC CHANGE)
    save_feedback_memory(feedback_payload)

    # Store in agent outputs
    agent_outputs["feedback"] = feedback_payload
    state["agent_outputs"] = agent_outputs

    # 🔒 CRITICAL: prevent LangGraph concurrent update errors
    return sanitize_state(state)
