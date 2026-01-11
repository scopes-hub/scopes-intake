import json
import os
from typing import Dict, Tuple

_RULES_CACHE = None
RULES_PATH = os.getenv("SCORING_RULES_PATH", "config/scoring_rules.json")


def load_rules(force_reload: bool = False) -> Dict:
    global _RULES_CACHE
    if _RULES_CACHE is None or force_reload:
        with open(RULES_PATH, "r", encoding="utf-8") as f:
            _RULES_CACHE = json.load(f)
    return _RULES_CACHE


def _normalize(value: str) -> str:
    return value.strip().lower()


def _weight(weights: Dict[str, int], key: str) -> int:
    if not key:
        return weights.get("default", 0)
    return weights.get(key, weights.get("default", 0))


def score_lead(payload: Dict, rules: Dict) -> Tuple[int, str]:
    industry = _normalize(payload.get("industry", ""))
    company_size = _normalize(payload.get("company_size", ""))
    region = _normalize(payload.get("region", ""))
    email = _normalize(payload.get("email", ""))
    domain = email.split("@", 1)[1] if "@" in email else ""

    score = 0
    score += _weight(rules.get("industry_weights", {}), industry)
    score += _weight(rules.get("company_size_weights", {}), company_size)
    score += _weight(rules.get("email_domain_weights", {}), domain)
    score += _weight(rules.get("region_weights", {}), region)

    routes = sorted(rules.get("routes", []), key=lambda r: r.get("min_score", 0), reverse=True)
    route = "Support"
    for entry in routes:
        if score >= entry.get("min_score", 0):
            route = entry.get("team", route)
            break

    return score, route
