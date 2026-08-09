import json
from pathlib import Path
from typing import Dict, Any, List, Optional

def get_domain_curriculum(module_number: Optional[int] = None) -> dict:
    curriculum = get_curriculum()
    if not module_number:
        return curriculum

    modules = curriculum.get("modules", [])
    selected_idx = None
    selected_module = None

    for idx, mod in enumerate(modules):
        if mod.get("n") == module_number:
            selected_idx = idx
            selected_module = mod
            break

    if selected_module is None or selected_idx is None:
        return curriculum

    start_day, end_day = selected_module.get("days", [0, 0])
    all_days = curriculum.get("days", [])
    
    module_days = [d for d in all_days if start_day <= d.get("day", 0) <= end_day]

    if len(module_days) < 4:
        if selected_idx < len(modules) - 1:
            adj_module = modules[selected_idx + 1]
        else:
            adj_module = modules[selected_idx - 1]
        
        adj_start, adj_end = adj_module.get("days", [0, 0])
        adj_days = [d for d in all_days if adj_start <= d.get("day", 0) <= adj_end]
        days_to_include = module_days + adj_days
    else:
        days_to_include = module_days

    included_module_numbers = {selected_module.get("n")}
    if len(module_days) < 4:
        included_module_numbers.add(adj_module.get("n"))

    return {
        "cohort": curriculum.get("cohort", ""),
        "modules": [m for m in modules if m.get("n") in included_module_numbers],
        "days": days_to_include
    }


def get_allowed_domain_day_ids(
    module_number: Optional[int], topics_covered: List[int]
) -> List[int]:
    """Return the domain days currently eligible for the next question.

    A short module can borrow only the number of days needed to reach four
    unique topics, and only after every day in the selected module was used.
    """
    if not module_number:
        return [d.get("day") for d in get_curriculum().get("days", [])]

    curriculum = get_curriculum()
    modules = curriculum.get("modules", [])
    selected_idx = next(
        (idx for idx, module in enumerate(modules) if module.get("n") == module_number),
        None,
    )
    if selected_idx is None:
        return [d.get("day") for d in curriculum.get("days", [])]

    selected_module = modules[selected_idx]
    start_day, end_day = selected_module.get("days", [0, 0])
    selected_days = list(range(start_day, end_day + 1))
    covered = set(topics_covered)
    if len(selected_days) >= 4 or not set(selected_days).issubset(covered):
        return selected_days

    adjacent_idx = selected_idx + 1 if selected_idx < len(modules) - 1 else selected_idx - 1
    adjacent_start, adjacent_end = modules[adjacent_idx].get("days", [0, 0])
    needed_days = 4 - len(selected_days)
    return selected_days + list(range(adjacent_start, adjacent_end + 1))[:needed_days]


def get_active_domain_curriculum(
    module_number: Optional[int], topics_covered: List[int]
) -> dict:
    """Return curriculum context limited to days eligible at this turn."""
    scoped_curriculum = get_domain_curriculum(module_number)
    allowed_days = set(get_allowed_domain_day_ids(module_number, topics_covered))
    return {
        **scoped_curriculum,
        "days": [d for d in scoped_curriculum.get("days", []) if d.get("day") in allowed_days],
    }


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

def get_relevant_curriculum(
    curriculum: dict,
    topics_covered: List[int],
    candidate_missions: List[Any]
) -> dict:
    mission_days = set()
    for m in candidate_missions:
        if isinstance(m, dict):
            d = m.get("day")
        else:
            d = getattr(m, "day", None)
        if d is not None:
            mission_days.add(d)

    relevant_days = set(topics_covered).union(mission_days)

    filtered_days = []
    for day_obj in curriculum.get("days", []):
        day_id = day_obj.get("day")
        if day_id in relevant_days:
            filtered_days.append(day_obj)
        else:
            filtered_days.append({
                "day": day_id,
                "title": day_obj.get("title")
            })

    return {
        "cohort": curriculum.get("cohort", ""),
        "modules": curriculum.get("modules", []),
        "days": filtered_days
    }
