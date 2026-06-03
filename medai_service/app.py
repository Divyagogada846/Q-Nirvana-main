from flask import Flask, render_template, request, jsonify, session
import os

# ── Import all 5 modules ──────────────────────────────────────────────────────
from modules.symptom_predictor    import predict_disease, get_all_symptoms
from modules.report_analyzer      import analyze_report
from modules.risk_predictor       import predict_risk
from modules.patient_support      import get_support, get_all_diseases
from modules.rare_disease_predictor import (
    predict_rare_disease, get_all_genes, get_disease_categories, get_gene_info
)

app = Flask(__name__)
app.secret_key = "medai_secret_key_change_in_production"


# ══════════════════════════════════════════════════════════════════════════════
# PAGE ROUTES
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/symptom")
def symptom_page():
    symptoms = get_all_symptoms()
    return render_template("symptom.html", symptoms=symptoms)

@app.route("/report")
def report_page():
    return render_template("report.html")

@app.route("/risk")
def risk_page():
    return render_template("risk.html")

@app.route("/support")
def support_page():
    diseases = get_all_diseases()
    return render_template("support.html", diseases=diseases)

@app.route("/rare")
def rare_page():
    """Module 5 — Rare Disease DNA Predictor"""
    gene_list  = get_all_genes()
    categories = get_disease_categories()
    db_size    = 6172   # Orphanet full DB size (our subset is the core genes)
    return render_template(
        "rare.html",
        gene_list=gene_list,
        categories=categories,
        db_size=db_size
    )


# ══════════════════════════════════════════════════════════════════════════════
# API ROUTES — Modules 1–4 (unchanged)
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/api/predict", methods=["POST"])
def api_predict():
    data = request.get_json()
    if not data or "symptoms" not in data:
        return jsonify({"error": "No symptoms provided"}), 400
    result = predict_disease(data["symptoms"])
    if result.get("status") == "success":
        session["last_disease"] = result.get("top_prediction", "")
    return jsonify(result)

@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    gender = "male"
    if request.content_type and "multipart" in request.content_type:
        file = request.files.get("report")
        gender = request.form.get("gender", "male")
        if not file:
            return jsonify({"error": "No file uploaded"}), 400
        result = analyze_report(file, gender)
    else:
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"error": "No report text provided"}), 400
        gender = data.get("gender", "male")
        result = analyze_report(data["text"], gender)
    return jsonify(result)

@app.route("/api/risk", methods=["POST"])
def api_risk():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No health data provided"}), 400
    result = predict_risk(data)
    last_disease = session.get("last_disease", "")
    if last_disease:
        result["from_module1"] = last_disease
    return jsonify(result)

@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "No message provided"}), 400
    message = data.get("message", "")
    disease = data.get("disease", "") or session.get("last_disease", "")
    result = get_support(message, disease)
    return jsonify(result)

@app.route("/api/full_diagnosis", methods=["POST"])
def api_full_diagnosis():
    data = request.get_json()
    if not data or "symptoms" not in data:
        return jsonify({"error": "No symptoms provided"}), 400
    prediction = predict_disease(data["symptoms"])
    if prediction.get("status") != "success":
        return jsonify(prediction)
    top_disease_label = prediction.get("top_prediction", "")
    disease_key_map = {
        "Influenza (Flu)": "flu", "Common Cold": "cold",
        "Malaria": "malaria", "Typhoid Fever": "typhoid",
        "Dengue Fever": "dengue", "Gastroenteritis": "gastro",
        "Type 2 Diabetes": "diabetes", "Pneumonia": "flu",
    }
    support_key = disease_key_map.get(top_disease_label, "")
    support = get_support("full guide", support_key) if support_key else {}
    session["last_disease"] = support_key
    return jsonify({"status": "success", "prediction": prediction, "support": support})


# ══════════════════════════════════════════════════════════════════════════════
# API ROUTES — Module 5: Rare Disease Predictor
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/api/rare", methods=["POST"])
def api_rare():
    """
    Module 5 — Main rare disease prediction endpoint.

    Receives JSON:
    {
        "gene":             "NF1",
        "variant_notation": "p.Arg1947*",
        "variant_type":     "nonsense",
        "allele_freq":      0.0,
        "cadd_score":       38.4,
        "compound_het":     false,
        "additional_genes": ["MEFV", "GLA"]
    }

    Returns: ranked disease candidates with ACMG criteria + confidence
    """
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400

    gene             = data.get("gene", "").strip()
    variant_notation = data.get("variant_notation", "")
    variant_type     = data.get("variant_type", "missense")
    allele_freq      = float(data.get("allele_freq", 0.0))
    cadd_score       = float(data.get("cadd_score", 20.0))
    compound_het     = bool(data.get("compound_het", False))
    additional_genes = data.get("additional_genes", [])

    if not gene:
        return jsonify({"status": "error", "message": "Gene symbol is required"}), 400

    result = predict_rare_disease(
        gene=gene,
        variant_notation=variant_notation,
        variant_type=variant_type,
        allele_freq=allele_freq,
        cadd_score=cadd_score,
        compound_het=compound_het,
        additional_genes=additional_genes
    )

    # Cross-module: store predicted rare disease in session
    if result.get("status") == "success":
        session["last_rare_disease"] = result.get("top_disease", "")

    return jsonify(result)


@app.route("/api/rare/gene/<gene_symbol>")
def api_rare_gene_info(gene_symbol):
    """Quick lookup endpoint — returns full info for one gene."""
    result = get_gene_info(gene_symbol.upper())
    return jsonify(result)


@app.route("/api/rare/genes")
def api_rare_genes():
    """Return all supported gene symbols."""
    return jsonify({
        "genes": get_all_genes(),
        "categories": get_disease_categories(),
        "total": len(get_all_genes())
    })


# ══════════════════════════════════════════════════════════════════════════════
# UTILITY ROUTES
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/api/symptoms_list")
def api_symptoms_list():
    return jsonify({"symptoms": get_all_symptoms()})

@app.route("/api/diseases_list")
def api_diseases_list():
    return jsonify({"diseases": get_all_diseases()})

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Route not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500


# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("\n" + "="*60)
    print("  MedAI — Unified Medical Chatbot")
    print("  All 5 modules loaded successfully")
    print("="*60)
    print("  Module 1: Symptom → Disease Prediction   /api/predict")
    print("  Module 2: Report Analyzer                /api/analyze")
    print("  Module 3: Future Risk Prediction         /api/risk")
    print("  Module 4: Patient Support Chat           /api/chat")
    print("  Module 5: Rare Disease DNA Predictor     /api/rare")
    print("="*60)
    print("  Open browser at: http://localhost:5001\n")
    app.run(debug=True, host="0.0.0.0", port=5001)
