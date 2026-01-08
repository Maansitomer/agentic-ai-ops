def query_understanding_agent(state):
    """
    Query Understanding Agent
    -------------------------
    Purpose:
    - Parse the user's natural language query
    - Extract intent, entity, urgency, and time horizon
    - Update shared state for downstream agents

    This agent:
    - Does NOT access data
    - Does NOT use LLMs
    - Is deterministic and explainable
    """

    query = state["query"].lower()

    intent = "unknown"
    entity = "general"
    urgency = "normal"
    time_horizon = "unspecified"

    # ---- Intent detection ----
    if any(word in query for word in ["why", "reason", "cause"]):
        intent = "explanation"
    elif any(word in query for word in ["who", "which", "list"]):
        intent = "prioritization"
    elif any(word in query for word in ["what should", "what action", "next step"]):
        intent = "recommendation"

    # ---- Entity detection ----
    if any(word in query for word in ["customer", "user", "account"]):
        entity = "customer"
    elif any(word in query for word in ["region", "city", "location"]):
        entity = "region"

    # ---- Time horizon & urgency ----
    if any(word in query for word in ["today", "now", "immediately"]):
        time_horizon = "today"
        urgency = "high"
    elif "week" in query:
        time_horizon = "this_week"

    # Update global state
    state["intent"] = {
        "intent": intent,
        "entity": entity,
        "time_horizon": time_horizon,
        "urgency": urgency,
        "raw_query": state["query"]
    }

    return state
