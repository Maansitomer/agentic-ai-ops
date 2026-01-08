from typing import Dict

LOCKED_KEYS = {
    "query",
    "session_id",
    "engineered_signals",
    "top_customers",
    "risk_state",
}

def sanitize_state(state: Dict) -> Dict:
    """
    Removes read-only / locked keys so LangGraph
    does not treat them as concurrent writes.
    """
    for key in LOCKED_KEYS:
        state.pop(key, None)
    return state
