import json
from pathlib import Path
from typing import Dict, Any, List

BASE_DIR = Path(__file__).parent.parent

def load_json(filename: str) -> Any:
    path = BASE_DIR / filename
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def get_curriculum() -> Dict[str, Any]:
    return load_json("curriculum.json") or {}

def get_candidates() -> List[Dict[str, Any]]:
    data = load_json("candidates.json")
    if data and "candidates" in data:
        return data["candidates"]
    return []

def get_day_by_id(day_id: int) -> Dict[str, Any]:
    curr = get_curriculum()
    for day in curr.get("days", []):
        if day.get("day") == day_id:
            return day
    return {}
