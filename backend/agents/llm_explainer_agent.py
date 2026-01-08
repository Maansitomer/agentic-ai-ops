from typing import Dict
from groq import Groq
import os
import json

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL_NAME = "llama-3.3-70b-versatile"



def llm_explainer_agent_node(state: Dict) -> Dict:
    """
    LLM Explainer Agent (READ-ONLY)
    --------------------------------
    - Generates executive explanation
    - NEVER changes decision logic
    """

    agent_outputs = state.get("agent_outputs", {})
    top_customers = state.get("top_customers", [])
    final_decision = state.get("final_decision", {})

    if not top_customers or not final_decision:
        return state

    prompt = f"""
You are an enterprise risk analyst.

Explain in simple language:
- Why these customers need attention
- Provide a short executive summary

Do NOT invent data.
Do NOT suggest actions.

Top Customers:
{json.dumps(top_customers, indent=2)}

Final Decision:
{json.dumps(final_decision, indent=2)}
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "Generate explanations only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=600,
        )

        explanation = response.choices[0].message.content.strip()

    except Exception as e:
        explanation = f"LLM explanation unavailable: {str(e)}"

    # ✅ WRITE TO TOP-LEVEL STATE (REQUIRED)
    state["llm_explainer"] = {
        "agent": "llm_explainer",
        "executive_summary": explanation,
        "confidence": 0.75,
    }

    # ✅ MIRROR INTO agent_outputs (FOR UI)
    agent_outputs["llm_explainer"] = state["llm_explainer"]
    state["agent_outputs"] = agent_outputs

    return state
