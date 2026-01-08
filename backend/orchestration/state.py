from typing import TypedDict, Dict, List, Any


class AgentState(TypedDict, total=False):
    query: str
    session_id: str

    engineered_signals: List[Dict]
    top_customers: List[Dict]
    risk_state: Dict
    features_df: Dict | None

    agent_outputs: Dict[str, Any]

    final_decision: Dict

    # ✅ REQUIRED — OTHERWISE LLM OUTPUT IS DROPPED
    llm_explainer: Dict
