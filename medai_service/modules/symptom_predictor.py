import numpy as np
import pickle
import os

# ─── Symptom & Disease Definitions ───────────────────────────────────────────

ALL_SYMPTOMS = [
    "fever", "cough", "fatigue", "headache", "body_ache", "chills",
    "sore_throat", "runny_nose", "sneezing", "congestion", "nausea",
    "vomiting", "diarrhea", "stomach_pain", "loss_of_appetite",
    "weakness", "joint_pain", "rash", "eye_pain", "sweating",
    "frequent_urination", "excessive_thirst", "blurry_vision",
    "slow_healing", "weight_loss", "chest_pain", "shortness_of_breath"
]

DISEASE_DATA = {
    "Influenza (Flu)": {
        "symptoms": ["fever", "cough", "fatigue", "headache", "body_ache", "chills", "sore_throat"],
        "severity": "medium",
        "medicines": ["Paracetamol 500mg (every 6 hrs)", "Oseltamivir/Tamiflu (75mg twice daily × 5 days)", "Cetirizine 10mg (at night)"],
        "precautions": ["Rest for 3–5 days", "Drink 2–3L warm fluids daily", "Avoid contact with others", "Wash hands frequently"],
        "diet": ["Warm soups and broths", "Ginger tea with honey", "Citrus fruits (Vitamin C)", "Avoid cold food and drinks"]
    },
    "Common Cold": {
        "symptoms": ["runny_nose", "cough", "sore_throat", "sneezing", "fever", "congestion"],
        "severity": "low",
        "medicines": ["Cetirizine 10mg (at night)", "Pseudoephedrine 60mg (decongestant)", "Vitamin C 1000mg (daily)"],
        "precautions": ["Steam inhalation twice daily", "Warm saline gargle", "Sleep with head elevated", "Stay warm"],
        "diet": ["Honey + ginger tea", "Warm turmeric milk", "Avoid dairy and cold drinks", "Eat light meals"]
    },
    "Malaria": {
        "symptoms": ["fever", "chills", "sweating", "headache", "vomiting", "fatigue", "body_ache"],
        "severity": "high",
        "medicines": ["Artemether-Lumefantrine (4 tabs twice daily × 3 days)", "Chloroquine 250mg (as per weight)", "Paracetamol for fever"],
        "precautions": ["Complete the full medicine course", "Use mosquito nets", "Apply DEET repellent", "See doctor if no improvement in 48 hrs"],
        "diet": ["ORS for hydration", "Light easy-to-digest meals", "Plenty of fluids", "Avoid spicy food"]
    },
    "Typhoid Fever": {
        "symptoms": ["fever", "weakness", "stomach_pain", "headache", "loss_of_appetite", "nausea"],
        "severity": "high",
        "medicines": ["Ciprofloxacin 500mg (twice daily × 7–14 days)", "Azithromycin 500mg (once daily)", "Paracetamol for fever"],
        "precautions": ["Drink only purified water", "Avoid street food", "Maintain hand hygiene", "Complete antibiotic course"],
        "diet": ["Boiled rice and dal", "Bananas and boiled potatoes", "Avoid raw vegetables", "Drink boiled water only"]
    },
    "Dengue Fever": {
        "symptoms": ["fever", "headache", "eye_pain", "joint_pain", "rash", "vomiting", "fatigue"],
        "severity": "high",
        "medicines": ["Paracetamol only (NO aspirin/ibuprofen)", "IV fluids if hospitalised", "Platelet transfusion if needed"],
        "precautions": ["Remove stagnant water near home", "Wear full-sleeve clothes", "Use mosquito nets", "Monitor platelet count daily"],
        "diet": ["Papaya leaf juice (boosts platelets)", "Coconut water", "Pomegranate juice", "High-protein soft foods"]
    },
    "Gastroenteritis": {
        "symptoms": ["vomiting", "diarrhea", "stomach_pain", "nausea", "fever", "weakness"],
        "severity": "medium",
        "medicines": ["ORS (1 sachet per litre, sip every 10 min)", "Ondansetron 4mg (for vomiting)", "Loperamide 2mg (after each loose stool)"],
        "precautions": ["Hydration is top priority", "Start BRAT diet (banana/rice/applesauce/toast)", "Wash hands before meals", "Avoid sharing utensils"],
        "diet": ["Banana, boiled rice, toast", "ORS or coconut water", "Avoid dairy for 48 hrs", "No spicy or fatty food"]
    },
    "Type 2 Diabetes": {
        "symptoms": ["frequent_urination", "excessive_thirst", "fatigue", "blurry_vision", "slow_healing", "weight_loss"],
        "severity": "medium",
        "medicines": ["Metformin 500mg (twice daily with meals)", "Glipizide 5mg (before breakfast)", "Empagliflozin 10mg (once daily)"],
        "precautions": ["Check blood sugar daily", "Exercise 30 mins daily", "Annual HbA1c and eye checkup", "Carry glucose tablets for hypoglycemia"],
        "diet": ["Low glycemic index foods", "Oats, legumes, green vegetables", "Avoid white rice, bread, sugar", "Small frequent meals"]
    },
    "Pneumonia": {
        "symptoms": ["fever", "cough", "chest_pain", "shortness_of_breath", "fatigue", "chills"],
        "severity": "high",
        "medicines": ["Amoxicillin 500mg (three times daily × 7 days)", "Azithromycin 500mg (once daily)", "Paracetamol for fever"],
        "precautions": ["Rest completely", "Deep breathing exercises", "Stay hydrated", "Seek hospital care if breathless"],
        "diet": ["Warm soups", "Honey and ginger", "High-protein foods", "Avoid cold drinks and smoking"]
    }
}


# ─── Simple ML-style Matching Engine ─────────────────────────────────────────

def _score_diseases(symptom_list):
    """Score each disease by symptom overlap — mimics ML predict_proba()"""
    results = []
    for disease, info in DISEASE_DATA.items():
        matched = [s for s in symptom_list if s in info["symptoms"]]
        if not matched:
            continue
        # Jaccard-style score weighted toward precision
        score = len(matched) / max(len(info["symptoms"]), len(symptom_list))
        results.append({
            "disease": disease,
            "confidence": round(score * 100),
            "matched_symptoms": matched,
            "severity": info["severity"],
            "medicines": info["medicines"],
            "precautions": info["precautions"],
            "diet": info["diet"]
        })
    results.sort(key=lambda x: x["confidence"], reverse=True)
    return results


def predict_disease(symptoms: list) -> dict:
    """
    Main function called by Flask route /predict
    Input : list of symptom strings  e.g. ["fever", "cough", "fatigue"]
    Output: dict with top predictions + medicines + precautions
    """
    if not symptoms:
        return {"error": "No symptoms provided", "predictions": []}

    # Normalise input (strip spaces, lowercase, replace spaces with _)
    clean = [s.strip().lower().replace(" ", "_") for s in symptoms]

    predictions = _score_diseases(clean)

    if not predictions:
        return {
            "status": "no_match",
            "message": "No matching disease found. Please consult a doctor.",
            "predictions": []
        }

    top = predictions[0]

    return {
        "status": "success",
        "top_prediction": top["disease"],
        "confidence": top["confidence"],
        "severity": top["severity"],
        "matched_symptoms": top["matched_symptoms"],
        "medicines": top["medicines"],
        "precautions": top["precautions"],
        "diet": top["diet"],
        "all_predictions": predictions[:3]   # top 3 for display
    }


def get_all_symptoms() -> list:
    """Return full symptom list for the frontend checkbox grid"""
    return ALL_SYMPTOMS
