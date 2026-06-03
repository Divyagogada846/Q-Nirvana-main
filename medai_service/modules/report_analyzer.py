import re
import os

# ─── Normal Reference Ranges ─────────────────────────────────────────────────

LAB_RANGES = {
    # Blood count
    "hemoglobin":       {"min": 13.5, "max": 17.5, "unit": "g/dL",      "label": "Hemoglobin"},
    "wbc":              {"min": 4.5,  "max": 11.0,  "unit": "×10³/µL",  "label": "WBC count"},
    "rbc":              {"min": 4.7,  "max": 6.1,   "unit": "million/µL","label": "RBC count"},
    "platelets":        {"min": 150,  "max": 400,   "unit": "×10³/µL",  "label": "Platelets"},
    "hematocrit":       {"min": 41,   "max": 53,    "unit": "%",         "label": "Hematocrit"},
    # Blood sugar
    "fasting_sugar":    {"min": 70,   "max": 100,   "unit": "mg/dL",    "label": "Fasting blood sugar"},
    "hba1c":            {"min": 4.0,  "max": 5.6,   "unit": "%",        "label": "HbA1c"},
    "postmeal_sugar":   {"min": 70,   "max": 140,   "unit": "mg/dL",    "label": "Post-meal glucose"},
    # Lipids
    "total_cholesterol":{"min": 0,    "max": 200,   "unit": "mg/dL",    "label": "Total cholesterol"},
    "ldl":              {"min": 0,    "max": 100,   "unit": "mg/dL",    "label": "LDL cholesterol"},
    "hdl":              {"min": 40,   "max": 60,    "unit": "mg/dL",    "label": "HDL cholesterol"},
    "triglycerides":    {"min": 0,    "max": 150,   "unit": "mg/dL",    "label": "Triglycerides"},
    # Thyroid
    "tsh":              {"min": 0.4,  "max": 4.0,   "unit": "mIU/L",    "label": "TSH"},
    "t3":               {"min": 0.8,  "max": 2.0,   "unit": "ng/mL",    "label": "T3"},
    "t4":               {"min": 0.8,  "max": 1.8,   "unit": "ng/dL",    "label": "Free T4"},
    # Kidney/Liver
    "creatinine":       {"min": 0.5,  "max": 1.1,   "unit": "mg/dL",    "label": "Creatinine"},
    "urea":             {"min": 7,    "max": 20,    "unit": "mg/dL",    "label": "Blood urea"},
    "sgpt":             {"min": 7,    "max": 40,    "unit": "U/L",      "label": "SGPT (ALT)"},
    "sgot":             {"min": 10,   "max": 40,    "unit": "U/L",      "label": "SGOT (AST)"},
}

# ─── Plain-English explanations for each parameter ───────────────────────────

PLAIN_ENGLISH = {
    "hemoglobin": {
        "low":  "Your hemoglobin is LOW. This means your blood is carrying less oxygen. You may feel tired, dizzy, or short of breath. Eat iron-rich foods like spinach, lentils, and red meat. Doctor may prescribe iron supplements.",
        "high": "Your hemoglobin is HIGH. This can thicken the blood. Drink more water and consult your doctor.",
        "normal": "Your hemoglobin is NORMAL. Your blood is carrying oxygen well."
    },
    "wbc": {
        "low":  "Your white blood cells are LOW. This may weaken your immunity. Avoid crowds and consult your doctor.",
        "high": "Your white blood cells are HIGH. Your body may be fighting an infection or inflammation. See a doctor to find the cause.",
        "normal": "Your white blood cell count is NORMAL. Your immune system is functioning well."
    },
    "fasting_sugar": {
        "low":  "Your blood sugar is TOO LOW (hypoglycemia). Eat something sweet immediately and consult a doctor.",
        "high": "Your fasting sugar is HIGH. Above 125 mg/dL means diabetes. Reduce sugar, exercise daily, and see an endocrinologist.",
        "normal": "Your fasting blood sugar is NORMAL. Your body is regulating glucose well."
    },
    "hba1c": {
        "low":  "Your HbA1c is within normal range.",
        "high": "Your HbA1c is HIGH, showing your average blood sugar over 3 months has been elevated. Target is below 5.7% for normal adults. You need better diet control and possibly medication.",
        "normal": "Your HbA1c is NORMAL. Your blood sugar has been well-controlled over the past 3 months."
    },
    "total_cholesterol": {
        "low":  "Cholesterol is normal range.",
        "high": "Your total cholesterol is HIGH. This increases heart disease risk. Reduce saturated fats, fried foods, and red meat. Eat oats, fish, and nuts.",
        "normal": "Your cholesterol is NORMAL. Keep eating heart-healthy foods."
    },
    "ldl": {
        "low":  "LDL is in normal range.",
        "high": "Your LDL (bad cholesterol) is HIGH. It causes plaque buildup in arteries. Avoid butter, ghee, and processed food. Doctor may prescribe statins.",
        "normal": "Your LDL (bad cholesterol) is NORMAL. Good job keeping it in check."
    },
    "hdl": {
        "low":  "Your HDL (good cholesterol) is LOW. HDL helps remove bad cholesterol. Increase exercise, eat olive oil and avocado, and quit smoking.",
        "high": "Your HDL is HIGH — this is actually good for heart health.",
        "normal": "Your HDL (good cholesterol) is NORMAL. Keep exercising and eating healthy fats."
    },
    "tsh": {
        "low":  "Your TSH is LOW. This may mean your thyroid is overactive (hyperthyroidism). Symptoms: weight loss, rapid heartbeat, anxiety. See an endocrinologist.",
        "high": "Your TSH is HIGH. This means your thyroid may be underactive (hypothyroidism). Symptoms: fatigue, weight gain, feeling cold. Doctor will likely prescribe Levothyroxine.",
        "normal": "Your TSH is NORMAL. Your thyroid is functioning well."
    },
    "creatinine": {
        "low":  "Creatinine is in normal range.",
        "high": "Your creatinine is HIGH. This may indicate your kidneys are not filtering waste properly. Drink more water, reduce protein, and see a nephrologist.",
        "normal": "Your creatinine is NORMAL. Your kidneys are filtering waste efficiently."
    },
    "platelets": {
        "low":  "Your platelet count is LOW (thrombocytopenia). This means your blood may not clot properly. Avoid injury, eat papaya leaf juice, and see a doctor immediately.",
        "high": "Your platelet count is HIGH. This may increase clot risk. Consult your doctor.",
        "normal": "Your platelet count is NORMAL. Your blood can clot and heal wounds properly."
    }
}


# ─── OCR Simulation (replaces pytesseract in real project) ───────────────────

def _simulate_ocr(text_input: str) -> str:
    """
    In production: replace this with pytesseract.image_to_string(image)
    For PDF files use: pdfplumber or PyMuPDF to extract text
    """
    return text_input.strip()


# ─── NLP Parsing: extract numbers from raw report text ───────────────────────

KEYWORD_MAP = {
    "hemoglobin": ["hemoglobin", "hgb", "hb"],
    "wbc": ["wbc", "white blood cell", "leukocyte", "tlc"],
    "rbc": ["rbc", "red blood cell", "erythrocyte"],
    "platelets": ["platelet", "plt", "thrombocyte"],
    "hematocrit": ["hematocrit", "hct", "packed cell"],
    "fasting_sugar": ["fasting blood sugar", "fbs", "fasting glucose", "fasting sugar"],
    "hba1c": ["hba1c", "glycated hemoglobin", "a1c"],
    "postmeal_sugar": ["post meal", "postmeal", "ppbs", "post prandial"],
    "total_cholesterol": ["total cholesterol", "cholesterol"],
    "ldl": ["ldl"],
    "hdl": ["hdl"],
    "triglycerides": ["triglyceride", "tg"],
    "tsh": ["tsh", "thyroid stimulating"],
    "t3": [" t3 ", "triiodothyronine"],
    "t4": ["t4", "thyroxine", "free t4"],
    "creatinine": ["creatinine", "creat"],
    "urea": ["urea", "blood urea", "bun"],
    "sgpt": ["sgpt", "alt ", "alanine"],
    "sgot": ["sgot", "ast ", "aspartate"]
}


def _extract_values(text: str) -> dict:
    """Parse raw OCR text and extract numeric lab values"""
    extracted = {}
    lines = text.lower().split("\n")
    for line in lines:
        for key, keywords in KEYWORD_MAP.items():
            if any(kw in line for kw in keywords):
                numbers = re.findall(r'\d+\.?\d*', line)
                if numbers:
                    try:
                        val = float(numbers[0])
                        # sanity check: ignore obviously wrong values
                        if 0 < val < 10000:
                            extracted[key] = val
                    except ValueError:
                        pass
    return extracted


def _classify_value(key: str, value: float, gender: str = "male") -> str:
    """Return 'low', 'normal', or 'high' for a given parameter"""
    ref = LAB_RANGES.get(key)
    if not ref:
        return "normal"
    # Adjust hemoglobin range for females
    if key == "hemoglobin" and gender == "female":
        ref = {"min": 12.0, "max": 15.5}
    if ref["min"] == 0:
        return "high" if value > ref["max"] else "normal"
    if value < ref["min"]:
        return "low"
    if value > ref["max"]:
        return "high"
    return "normal"


# ─── Main Analysis Function ───────────────────────────────────────────────────

def analyze_report(file_or_text, gender: str = "male") -> dict:
    """
    Main function called by Flask route /analyze
    Input : uploaded file object OR raw text string
    Output: dict with parsed values, statuses, and plain-English explanations
    """
    # Step 1: Extract text (OCR in real project)
    if isinstance(file_or_text, str):
        raw_text = _simulate_ocr(file_or_text)
    else:
        # Real project: use pytesseract or pdfplumber here
        try:
            raw_text = file_or_text.read().decode("utf-8", errors="ignore")
        except Exception:
            raw_text = ""

    if not raw_text.strip():
        return {"status": "error", "message": "Could not extract text from report."}

    # Step 2: Parse values with NLP
    extracted_values = _extract_values(raw_text)

    if not extracted_values:
        return {
            "status": "no_values",
            "message": "No recognizable lab values found. Please ensure the report text is clear.",
            "raw_text": raw_text[:500]
        }

    # Step 3: Classify each value and build results
    results = []
    abnormal_count = 0

    for key, value in extracted_values.items():
        ref = LAB_RANGES.get(key, {})
        status = _classify_value(key, value, gender)
        if status != "normal":
            abnormal_count += 1

        explanation_db = PLAIN_ENGLISH.get(key, {})
        explanation = explanation_db.get(status, f"Value: {value} {ref.get('unit','')}")

        results.append({
            "key": key,
            "label": ref.get("label", key.replace("_", " ").title()),
            "value": value,
            "unit": ref.get("unit", ""),
            "normal_min": ref.get("min", 0),
            "normal_max": ref.get("max", 0),
            "status": status,
            "plain_english": explanation
        })

    # Sort: abnormal first
    results.sort(key=lambda x: (x["status"] == "normal", x["label"]))

    return {
        "status": "success",
        "total_parameters": len(results),
        "abnormal_count": abnormal_count,
        "normal_count": len(results) - abnormal_count,
        "results": results,
        "raw_text": raw_text[:800],
        "summary": f"Found {len(results)} parameters. {abnormal_count} are outside normal range."
    }
