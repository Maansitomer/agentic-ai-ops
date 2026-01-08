import json
from datetime import datetime
from pathlib import Path
from typing import Dict

MEMORY_PATH = Path("backend/memory/feedback_memory.jsonl")
MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)


def save_feedback_memory(record: Dict):
    """
    Append feedback memory safely.
    Immutable, append-only.
    """

    memory_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "feedback": record
    }

    with open(MEMORY_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(memory_entry) + "\n")
