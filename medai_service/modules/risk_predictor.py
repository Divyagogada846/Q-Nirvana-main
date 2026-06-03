
# ─── Risk Thresholds & Weights ────────────────────────────────────────────────

RISK_RULES = {
    "diabetes": {
        "label": "Type 2 diabetes",
        "factors": [
            {"param": "sugar",    "threshold": 126, "weight": 40, "condition": "gt"},
            {"param": "sugar",    "threshold": 100, "weight": 20, "condition": "gt"},
            {"param": "bmi",      "threshold": 30,  "weight": 20, "condition": "gt"},
            {"param": "bmi",      "threshold": 25,  "weight": 10, "condition": "gt"},
            {"param": "family",   "threshold": 1,   "weight": 15, "condition": "gte"},
            {"param": "activity", "threshold": 3,   "weight": 10, "condition": "lt"},
            {"param": "age",      "threshold": 45,  "weight": 10, "condition": "gt"},
        ],
        "growth_rate": 0.28,
        "icon": "D",
        "color": "amber"
    },
    "heart": {
        "label": "Cardiovascular disease",
        "factors": [
            {"param": "bp",       "threshold": 140, "weight": 30, "condition": "gt"},
            {"param": "bp",       "threshold": 120, "weight": 15, "condition": "gt"},
            {"param": "chol",     "threshold": 240, "weight": 25, "condition": "gt"},
            {"param": "chol",     "threshold": 200, "weight": 12, "condition": "gt"},
            {"param": "smoke",    "threshold": 10,  "weight": 25, "condition": "gt"},
            {"param": "smoke",    "threshold": 0,   "weight": 12, "condition": "gt"},
            {"param": "bmi",      "threshold": 30,  "weight": 10, "condition": "gt"},
            {"param": "age",      "threshold": 50,  "weight": 10, "condition": "gt"},
        ],
        "growth_rate": 0.30,
        "icon": "H",
        "color": "red"
    },
    "kidney": {
        "label": "Chronic kidney disease",
        "factors": [
            {"param": "creat",    "threshold": 1.5, "weight": 40, "condition": "gt"},
            {"param": "creat",    "threshold": 1.2, "weight": 20, "condition": "gt"},
            {"param": "sugar",    "threshold": 126, "weight": 20, "condition": "gt"},
            {"param": "bp",       "threshold": 140, "weight": 20, "condition": "gt"},
            {"param": "age",      "threshold": 60,  "weight": 10, "condition": "gt"},
        ],
        "growth_rate": 0.18,
        "icon": "K",
        "color": "teal"
    },
    "anemia": {
        "label": "Iron-deficiency anemia",
        "factors": [
            {"param": "hgb",      "threshold": 11.5,"weight": 50, "condition": "lt"},
            {"param": "hgb",      "threshold": 13.5,"weight": 25, "condition": "lt"},
            {"param": "activity", "threshold": 2,   "weight": 10, "condition": "lt"},
        ],
        "growth_rate": 0.10,
        "icon": "A",
        "color": "purple"
    },
    "stroke": {
        "label": "Stroke / brain attack",
        "factors": [
            {"param": "bp",       "threshold": 160, "weight": 35, "condition": "gt"},
            {"param": "bp",       "threshold": 140, "weight": 20, "condition": "gt"},
            {"param": "smoke",    "threshold": 10,  "weight": 20, "condition": "gt"},
            {"param": "chol",     "threshold": 240, "weight": 15, "condition": "gt"},
            {"param": "age",      "threshold": 55,  "weight": 15, "condition": "gt"},
        ],
        "growth_rate": 0.22,
        "icon": "S",
        "color": "coral"
    }
}

PREVENTION_TIPS = {
    "diabetes": {
        "low":      ["Maintain a healthy weight", "Exercise 5 days/week"],
        "medium":   ["Reduce sugar and carbs", "Check HbA1c annually", "Daily 30-min walk"],
        "high":     ["Consult endocrinologist now", "Start low-carb diet immediately", "Monitor sugar daily"],
        "critical": ["Urgent doctor visit needed", "Medication likely required", "Strict diet and exercise plan"]
    },
    "heart": {
        "low":      ["Stay physically active", "Eat heart-healthy fats"],
        "medium":   ["Reduce sodium intake", "Quit smoking", "Annual ECG recommended"],
        "high":     ["Cardiology consultation needed", "Statins may be prescribed", "Quit smoking immediately"],
        "critical": ["Urgent cardiology review", "Stress test and ECG needed", "Strict BP and cholesterol control"]
    },
    "kidney": {
        "low":      ["Drink 8 glasses of water daily", "Limit excess protein"],
        "medium":   ["Monitor creatinine every 6 months", "Control BP and blood sugar"],
        "high":     ["Nephrology referral required", "Limit salt and protein intake", "Avoid NSAIDs"],
        "critical": ["Urgent nephrology consultation", "Possible dialysis risk if untreated"]
    },
    "anemia": {
        "low":      ["Eat iron-rich foods daily", "Annual hemoglobin check"],
        "medium":   ["Iron and folic acid supplements", "Eat spinach, lentils, red meat"],
        "high":     ["Doctor visit for iron panel", "IV iron therapy may be needed"],
        "critical": ["Urgent blood test required", "Possible transfusion risk"]
    },
    "stroke": {
        "low":      ["Check BP annually", "Stay physically active"],
        "medium":   ["Quit smoking", "Reduce alcohol", "BP medication if elevated"],
        "high":     ["Neurologist visit recommended", "Aspirin therapy possible", "Urgent BP control"],
        "critical": ["Emergency evaluation needed", "Immediate BP management required"]
    }
}


# ─── Scoring Engine ───────────────────────────────────────────────────────────

def _get_risk_level(score: int) -> str:
    if score >= 60: return "critical"
    if score >= 35: return "high"
    if score >= 15: return "medium"
    return "low"


def _score_disease(disease_key: str, params: dict) -> int:
    """Apply rule-based scoring for a single disease"""
    rules = RISK_RULES[disease_key]["factors"]
    total = 0
    applied = set()  # avoid double-counting overlapping thresholds

    for rule in rules:
        p = rule["param"]
        val = params.get(p, 0)
        thr = rule["threshold"]
        cond = rule["condition"]
        key_id = f"{p}_{thr}"

        if key_id in applied:
            continue

        hit = False
        if cond == "gt"  and val > thr:  hit = True
        if cond == "gte" and val >= thr:  hit = True
        if cond == "lt"  and val < thr:   hit = True
        if cond == "lte" and val <= thr:  hit = True

        if hit:
            total += rule["weight"]
            applied.add(key_id)

    return min(total, 95)


def _project_5yr(base_score: int, growth_rate: float) -> list:
    """Generate projected risk for years 0–5"""
    points = []
    for yr in range(6):
        projected = base_score + int(base_score * growth_rate * yr / 5)
        points.append(min(projected, 95))
    return points


# ─── Main Prediction Function ─────────────────────────────────────────────────

def predict_risk(health_data: dict) -> dict:
    """
    Main function called by Flask route /risk
    Input : dict with keys — sugar, bp, chol, hgb, creat, smoke, activity, family, age, bmi, sex
    Output: dict with per-disease risk scores, levels, tips, and 5-year projection
    """
    # Provide safe defaults
    params = {
        "sugar":    float(health_data.get("sugar",    100)),
        "bp":       float(health_data.get("bp",       120)),
        "chol":     float(health_data.get("chol",     180)),
        "hgb":      float(health_data.get("hgb",      14.0)),
        "creat":    float(health_data.get("creat",    0.9)),
        "smoke":    float(health_data.get("smoke",    0)),
        "activity": float(health_data.get("activity", 5)),
        "family":   float(health_data.get("family",   0)),
        "age":      float(health_data.get("age",      30)),
        "bmi":      float(health_data.get("bmi",      22)),
    }

    disease_results = {}
    for key, info in RISK_RULES.items():
        score = _score_disease(key, params)
        level = _get_risk_level(score)
        tips  = PREVENTION_TIPS[key][level]
        projection = _project_5yr(score, info["growth_rate"])

        disease_results[key] = {
            "label":      info["label"],
            "score":      score,
            "level":      level,
            "icon":       info["icon"],
            "color":      info["color"],
            "tips":       tips,
            "projection": projection
        }

    # Overall risk = weighted average
    weights = {"heart": 0.30, "diabetes": 0.25, "stroke": 0.20, "kidney": 0.15, "anemia": 0.10}
    overall = int(sum(disease_results[k]["score"] * w for k, w in weights.items()))
    overall = min(overall, 95)

    high_risk_count = sum(
        1 for v in disease_results.values()
        if v["level"] in ("high", "critical")
    )

    # Sort diseases by score descending for display
    sorted_diseases = sorted(
        disease_results.items(),
        key=lambda x: x[1]["score"],
        reverse=True
    )

    return {
        "status": "success",
        "overall_score": overall,
        "overall_level": _get_risk_level(overall),
        "high_risk_count": high_risk_count,
        "diseases": dict(sorted_diseases),
        "timeline_labels": ["Now", "1 yr", "2 yr", "3 yr", "4 yr", "5 yr"],
        "summary": f"Overall health risk is {_get_risk_level(overall).upper()} at {overall}%. "
                   f"{high_risk_count} condition(s) require attention."
    }
