from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
import json

from backend.orchestration.graph import run_agentic_graph
from backend.utils.json_sanitizer import json_safe

router = APIRouter()


class UserQuery(BaseModel):
    query: str
    session_id: str | None = None


@router.post("/ask")
def ask_ops_ai(payload: UserQuery):
    # Run agentic graph
    result = run_agentic_graph(payload.query, payload.session_id)

    # ----------------------------------------
    # ✅ SAVE FULL RESULT TO FILE (DEBUG SAFE)
    # ----------------------------------------
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"agentic_debug_result_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(
            result,
            f,
            indent=2,
            default=str
        )

    print(f"\n✅ FULL AGENT OUTPUT SAVED TO FILE: {filename}\n")

    # ----------------------------------------
    # ✅ RETURN SMALL, SAFE RESPONSE
    # ----------------------------------------
    return json_safe({
        "status": "EXECUTED",
        "debug_file": filename,
        "agents_ran": list(result.get("agent_outputs", {}).keys()),
        "customers_flagged": len(result.get("engineered_signals", [])),
        "final_decision": result.get("final_decision", {})
    })
