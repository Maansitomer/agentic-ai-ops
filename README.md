# 🧠 Agentic AI Ops Platform

**Autonomous Multi-Agent Risk Intelligence & Decision System**

🔗 **Live Demo:**
👉 (https://agentic-ai-ops-frontend.onrender.com)

🔗 **Backend API:**
👉 (https://agentic-ai-ops-backend.onrender.com)

---

## 📌 Project Overview

The **Agentic AI Ops Platform** is an end-to-end system that uses **multiple autonomous AI agents** to:

* Detect risky customers
* Analyze operational, financial, and CX stress
* Recommend actions
* Evaluate decision reliability
* Generate executive summaries using LLMs

The system is built with:

* **FastAPI** for backend orchestration
* **LangGraph** for agent workflow
* **Groq LLM** for explanations
* **Streamlit** for an interactive frontend dashboard
* **Render** for cloud deployment

---

## 🏗️ System Architecture

```
User (Streamlit UI)
        |
        v
FastAPI Backend (/api/ask)
        |
        v
LangGraph Agent Workflow
        |
        v
Agents → Final Decision → LLM → Feedback
        |
        v
Debug JSON (stored + fetched by frontend)
```

---

## 🧩 Backend Architecture (FastAPI + LangGraph)

The backend is designed as an **agentic pipeline**, where each agent has a **single responsibility** and **never overwrites others’ logic**.

### 🔁 Agent Execution Flow

1. **Feature Engineering**
2. **Operations Agent**
3. **Finance Agent**
4. **Customer Experience (CX) Agent**
5. **Data Validation Agent**
6. **Action & Explainability Agent**
7. **Evaluation Agent**
8. **LLM Explainer Agent**
9. **Feedback Agent**

---

## 🤖 Backend Agents Explained

### 1️⃣ Feature Engineering Node

* Builds customer-level signals:

  * Usage volatility
  * Ops stress
  * Financial stress
  * CX stress
* Computes a **customer risk score**
* Selects **Top 10 risky customers**
* Stores `engineered_signals` safely

---

### 2️⃣ Operations Agent

* Detects operational instability
* Classifies severity (`high / low`)
* Outputs confidence & diagnosis

---

### 3️⃣ Finance Agent

* Analyzes financial exposure & anomalies
* Determines if finance is a primary risk driver

---

### 4️⃣ CX Agent

* Detects customer dissatisfaction
* Flags high-risk CX patterns
* Often acts as a **primary driver**

---

### 5️⃣ Data Validation Agent

* Audits data reliability
* Flags distribution anomalies
* Assigns **data trust level** (`high / medium / low`)

---

### 6️⃣ Action & Explainability Agent

* Works on **top risky customers only**
* For each customer:

  * Explains *why* they are risky
  * Suggests **team-specific actions**
  * Assigns priority (P0, P1, etc.)

Example:

```json
{
  "customer_id": "C04732",
  "risk_level": "CRITICAL",
  "primary_driver": "cx",
  "recommended_actions": [
    {"team": "Customer Experience", "priority": "P0"},
    {"team": "Retention", "priority": "P1"}
  ]
}
```

---

### 7️⃣ Evaluation Agent (Governance Layer)

* Measures:

  * Cross-agent agreement
  * Action presence
  * Data trust
* Produces:

  * Verdict: `RELIABLE / NEEDS_REVIEW`
  * Decision confidence score

This ensures **responsible AI decision-making**.

---

### 8️⃣ LLM Explainer Agent (Groq)

* Uses **Groq LLM**
* Generates:

  * Executive summary
  * Plain-language explanation
* **Read-only agent**
* Never alters decisions

---

### 9️⃣ Feedback Agent

* Captures:

  * Final decision snapshot
  * Human override placeholder
* Persists feedback (append-only)
* Enables future learning loops

---

## 🌐 Backend API Endpoints

### `POST /api/ask`

Triggers full agent execution.

**Input**

```json
{
  "query": "Who needs attention today?"
}
```

**Output (metadata)**

```json
{
  "status": "EXECUTED",
  "debug_file": "agentic_debug_result_XXXX.json",
  "customers_flagged": 10,
  "final_decision": {...}
}
```

---

### `GET /api/debug/{file}`

Returns the **full agent execution JSON**, including:

* All agents’ outputs
* Customer risk details
* Actions
* Evaluation
* LLM summary

This design avoids large synchronous responses and improves reliability.

---

## 🎨 Frontend (Streamlit Dashboard)

The frontend is built using **Streamlit** for rapid, interactive visualization and demo readiness.

### Why Streamlit?

* Fast to iterate
* Ideal for PoC & investor demos
* Native charts & layout
* Easy backend integration

---

## 🖥️ Frontend Features

### 🔎 Analysis Control

* Business question input
* “Run Analysis” trigger

---

### 📊 KPI Header (Global)

* Overall Status
* Attention Required
* Decision Confidence
* Primary Drivers

Styled as **clean KPI cards**.

---

### 📊 Overview Tab

* Agent agreement visualization
* Risk context summary

---

### 🔥 Customers Tab

* Top risky customers
* Risk score bar chart (Plotly)
* Interactive data table

---

### 🛠 Actions Tab

* Customer-level expanders
* Risk explanation
* Team-wise recommended actions

---

### 🧪 Evaluation & LLM Tab

* Governance verdict
* Agreement level
* Decision confidence
* High-severity agents
* **LLM executive summary embedded directly**

This keeps **human trust + explainability** in one place.

---

## ☁️ Deployment (Render)

### Backend

* Deployed as **FastAPI Web Service**
* Uses:

  * `uvicorn`
  * Environment variable: `GROQ_API_KEY`
* Stateless execution
* Debug JSON stored & served

---

### Frontend

* Deployed as **Streamlit Web Service**
* Connects to backend via public API
* No secrets required
* Lightweight & scalable

---

## 🔐 Security & Best Practices

* API keys stored as **Render environment variables**
* No secrets in GitHub
* Read-only LLM agent
* No destructive writes
* Explicit agent boundaries

---

## 🚀 What This Project Demonstrates

✅ Agentic AI architecture
✅ Multi-agent orchestration (LangGraph)
✅ Responsible AI governance
✅ LLM explainability
✅ Full-stack deployment
✅ Real-world decision system design

---

## 🏁 Conclusion

This project is a **complete Agentic AI system**, not just a model or dashboard.

It shows how autonomous agents can:

* Analyze complex signals
* Agree or disagree
* Recommend actions
* Justify decisions
* Remain auditable & explainable


