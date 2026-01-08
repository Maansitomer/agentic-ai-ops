from fastapi import APIRouter, HTTPException
import json
import os

router = APIRouter()

DEBUG_DIR = "."  # same dir where files are saved

@router.get("/api/debug/{filename}")
def get_debug_file(filename: str):
    path = os.path.join(DEBUG_DIR, filename)

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Debug file not found")

    with open(path, "r") as f:
        return json.load(f)
