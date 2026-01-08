from langgraph.graph import StateGraph
import numpy as np

from backend.orchestration.state import AgentState
from backend.intelligence.feature_builder import build_features

from backend.agents.ops_agent import ops_agent_node
from backend.agents.finance_agent import finance_agent_node
from backend.agents.cx_agent import cx_agent_node
from backend.agents.data_validation_agent import data_validation_agent_node
from backend.agents.action_explainability_agent import action_explainability_agent_node
from backend.agents.evaluation_agent import evaluation_agent_node
from backend.agents.feedback_agent import feedback_agent_node
from backend.agents.synthesis_agent import synthesis_agent_node
from backend.agents.llm_explainer_agent import llm_explainer_agent_node


# --------------------------------------------------
# Feature Engineering + Prioritization (UNCHANGED)
# --------------------------------------------------
def feature_engineering_node(state: AgentState):
    result = build_features()

    if isinstance(result, tuple) and len(result) == 2:
        features_df, risk_state = result
    elif isinstance(result, tuple) and len(result) == 3:
        features_df, risk_state, _ = result
    else:
        raise ValueError("Unexpected return from build_features()")

    if "customer_risk_score" not in features_df.columns:
        features_df["customer_risk_score"] = (
            0.35 * features_df["usage_volatility"].fillna(0)
            + 0.30 * features_df["ops_stress"].fillna(0)
            + 0.25 * features_df["financial_stress"].fillna(0) / 10000
            + 0.10 * features_df["cx_stress"].fillna(0)
        )

    features_df["customer_risk_score"] = (
        features_df["customer_risk_score"]
        .replace([np.inf, -np.inf], 0)
        .fillna(0)
        .astype(float)
    )

    prioritized_df = (
        features_df
        .sort_values("customer_risk_score", ascending=False)
        .head(10)
    )

    top_customers = prioritized_df.to_dict(orient="records")

    state["engineered_signals"] = top_customers
    state["top_customers"] = top_customers
    state["risk_state"] = risk_state

    # 🔒 HARD BLOCK FULL DF
    state["features_df"] = None

    return state


# --------------------------------------------------
# Graph Builder (FIXED ORDER ONLY)
# --------------------------------------------------
def build_agentic_graph():
    graph = StateGraph(AgentState)

    graph.add_node("feature_engineering", feature_engineering_node)
    graph.add_node("operations", ops_agent_node)
    graph.add_node("finance", finance_agent_node)
    graph.add_node("cx", cx_agent_node)
    graph.add_node("data_validation", data_validation_agent_node)
    graph.add_node("action_explainability", action_explainability_agent_node)
    graph.add_node("evaluation", evaluation_agent_node)

    # 🔑 FINAL DECISION CREATED HERE
    graph.add_node("synthesis", synthesis_agent_node)

    # 🔑 READ-ONLY
    graph.add_node("llm_explainer", llm_explainer_agent_node)

    # 🔑 SNAPSHOT LAST
    graph.add_node("feedback", feedback_agent_node)

    graph.set_entry_point("feature_engineering")

    graph.add_edge("feature_engineering", "operations")
    graph.add_edge("operations", "finance")
    graph.add_edge("finance", "cx")
    graph.add_edge("cx", "data_validation")
    graph.add_edge("data_validation", "action_explainability")
    graph.add_edge("action_explainability", "evaluation")

    graph.add_edge("evaluation", "synthesis")
    graph.add_edge("synthesis", "llm_explainer")
    graph.add_edge("llm_explainer", "feedback")

    return graph.compile()


# --------------------------------------------------
# Runner (UNCHANGED)
# --------------------------------------------------
def run_agentic_graph(query: str, session_id: str = None):
    app = build_agentic_graph()

    state = {
        "query": query,
        "session_id": session_id,
        "agent_outputs": {},
        "final_decision": {},
    }

    return app.invoke(state)
