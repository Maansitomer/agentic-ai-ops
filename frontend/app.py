import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# ---------------------------
# CONFIG (UNCHANGED)
# ---------------------------
BACKEND_ASK_URL = "http://127.0.0.1:8000/api/ask"
BACKEND_DEBUG_URL = "http://127.0.0.1:8000/api/debug"

st.set_page_config(
    page_title="Agentic AI Ops Platform",
    layout="wide",
    page_icon="🧠"
)

# ---------------------------
# GLOBAL UI STYLING (VISUAL ONLY)
# ---------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
    }

    .hero-title {
        font-size: 52px;
        font-weight: 800;
        margin-bottom: 0px;
    }

    .hero-subtitle {
        font-size: 18px;
        color: #6b7280;
        margin-top: -6px;
        margin-bottom: 26px;
    }

    .kpi-wrapper {
        background: linear-gradient(135deg, #eef2ff, #ffffff);
        padding: 22px;
        border-radius: 22px;
        margin-bottom: 30px;
    }

    div[data-testid="metric-container"] {
        background: white;
        border-radius: 14px;
        padding: 18px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.06);
        border-left: 6px solid #6366f1;
    }

    .section-card {
        background: white;
        padding: 28px;
        border-radius: 18px;
        box-shadow: 0 8px 26px rgba(0,0,0,0.06);
        margin-bottom: 30px;
    }

    .soft-divider {
        height: 1px;
        background: linear-gradient(to right, transparent, #e5e7eb, transparent);
        margin: 32px 0;
    }

    h2, h3 {
        font-weight: 700;
    }

    .streamlit-expanderHeader {
        font-size: 16px;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.title("🔎 Analysis Control")

query = st.sidebar.text_input(
    "Business Question",
    value="Who needs attention today?"
)

run = st.sidebar.button("🚀 Run Analysis")

# ---------------------------
# RUN ANALYSIS (UNCHANGED LOGIC)
# ---------------------------
if run:
    with st.spinner("Running multi-agent analysis..."):
        response = requests.post(
            BACKEND_ASK_URL,
            json={"query": query}
        )

        if response.status_code != 200:
            st.error("Backend execution failed")
        else:
            meta = response.json()
            debug_file = meta.get("debug_file")

            debug_response = requests.get(
                f"{BACKEND_DEBUG_URL}/{debug_file}"
            )

            if debug_response.status_code != 200:
                st.error("Failed to load agent debug output")
            else:
                st.session_state["meta"] = meta
                st.session_state["result"] = debug_response.json()
                st.success("Analysis completed")

# ---------------------------
# REQUIRE RESULT
# ---------------------------
if "result" not in st.session_state:
    st.info("Run analysis to view results")
    st.stop()

result = st.session_state["result"]

engineered = result.get("engineered_signals", [])
agent_outputs = result.get("agent_outputs", {})
final_decision = result.get("final_decision", {})

# =====================================================
# HERO HEADER
# =====================================================
st.markdown(
    """
    <div>
        <div class="hero-title">🧠 Agentic AI Ops Platform</div>
        <div class="hero-subtitle">
            Autonomous Multi-Agent Risk Intelligence & Decision Engine
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================================
# KPI SECTION (SEPARATED)
# =====================================================
st.markdown('<div class="kpi-wrapper">', unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)

k1.metric("🚨 Overall Status", final_decision.get("overall_status", "").upper())
k2.metric("⚠ Attention Required", str(final_decision.get("attention_required")))
k3.metric("📊 Decision Confidence", final_decision.get("confidence"))
k4.metric("🧭 Primary Drivers", ", ".join(final_decision.get("primary_driver", [])))

st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# TABS
# =====================================================
tabs = st.tabs([
    "📊 Overview",
    "🔥 Customers",
    "🛠 Actions",
    "🧪 Evaluation & LLM"
])

# =====================================================
# OVERVIEW TAB
# =====================================================
with tabs[0]:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("📊 Risk Overview")

    agreement = final_decision.get("agent_agreement", {})
    df = pd.DataFrame({
        "Agent": agreement.keys(),
        "Agreement": agreement.values()
    })

    fig = px.bar(
        df,
        x="Agent",
        y="Agreement",
        color="Agreement",
        title="Agent Agreement Levels"
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# CUSTOMERS TAB
# =====================================================
with tabs[1]:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("🔥 Top Risky Customers")

    if not engineered:
        st.warning("No risky customers detected.")
    else:
        df = pd.DataFrame(engineered)

        fig = px.bar(
            df,
            x="customer_id",
            y="customer_risk_score",
            color="customer_risk_score",
            title="Customer Risk Scores"
        )

        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# ACTIONS TAB
# =====================================================
with tabs[2]:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("🛠 Recommended Actions")

    actions = agent_outputs.get("action_explainability", {}).get("actions", [])

    if not actions:
        st.warning("No actions available.")
    else:
        for a in actions:
            with st.expander(f"🔥 Customer {a['customer_id']} — {a['risk_level']}"):
                st.markdown(f"**Risk Score:** {round(a['risk_score'], 2)}")
                st.markdown(f"**Primary Driver:** {a['primary_driver']}")

                st.markdown("### Why flagged")
                for e in a["explanation"]:
                    st.markdown(f"- {e}")

                st.markdown("### Recommended Actions")
                for r in a["recommended_actions"]:
                    st.markdown(
                        f"- **{r['team']}** → {r['action']} _(Priority {r['priority']})_"
                    )

    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# EVALUATION + LLM TAB
# =====================================================
with tabs[3]:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("🧪 Evaluation & Governance")

    evaluation = agent_outputs.get("evaluation", {})
    llm = agent_outputs.get("llm_explainer", {})

    if evaluation:
        e1, e2, e3 = st.columns(3)
        e1.metric("✅ Verdict", evaluation.get("verdict"))
        e2.metric("🤝 Agreement Level", evaluation.get("agreement_level"))
        e3.metric("📈 Decision Confidence", evaluation.get("decision_confidence"))

        st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

        notes = evaluation.get("notes", {})
        st.markdown("### 🔍 Governance Signals")
        st.markdown(
            f"""
            - **High Severity Agents:** {", ".join(notes.get("high_severity_agents", []))}
            - **Actions Present:** {notes.get("actions_present")}
            - **Data Trust:** {notes.get("data_trust")}
            """
        )

    st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)
    st.subheader("🧠 Executive Summary (LLM)")

    if llm:
        st.markdown(
            f"""
            <div style="
                background:linear-gradient(135deg,#ecfeff,#ffffff);
                padding:24px;
                border-radius:18px;
                font-size:16px;
                line-height:1.7;
            ">
            {llm.get("executive_summary")}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)
