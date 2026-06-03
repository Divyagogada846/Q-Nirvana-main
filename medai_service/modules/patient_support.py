import re

# ─── Medicine & Precaution Database ──────────────────────────────────────────

SUPPORT_DB = {
    "flu": {
        "aliases": ["flu", "influenza", "fever cough", "body ache", "chills fever"],
        "medicines": [
            {"name": "Paracetamol 500mg",    "dose": "Every 6 hrs",           "note": "For fever and body pain"},
            {"name": "Oseltamivir (Tamiflu)","dose": "75mg twice daily × 5 days", "note": "Antiviral — start within 48 hrs"},
            {"name": "Cetirizine 10mg",      "dose": "Once at night",         "note": "For runny nose and sneezing"},
        ],
        "precautions": [
            "Rest completely for at least 3–5 days",
            "Drink 2–3 litres of warm fluids daily",
            "Avoid contact with elderly, infants, and pregnant women",
            "Wash hands frequently with soap for 20 seconds",
            "Wear a mask to prevent spreading the virus"
        ],
        "diet": ["Warm chicken or vegetable soup", "Ginger and honey tea", "Citrus fruits rich in Vitamin C", "Avoid cold food and beverages"],
        "warning": "See a doctor immediately if fever exceeds 104°F (40°C) or lasts more than 3 days.",
        "follow_up": "Flu usually resolves in 7–10 days. If breathlessness occurs, go to emergency."
    },
    "cold": {
        "aliases": ["cold", "runny nose", "sneezing", "common cold", "congestion", "blocked nose"],
        "medicines": [
            {"name": "Cetirizine 10mg",      "dose": "Once at night",          "note": "Reduces sneezing and itching"},
            {"name": "Pseudoephedrine 60mg", "dose": "Every 4–6 hrs",          "note": "Nasal decongestant"},
            {"name": "Vitamin C 1000mg",     "dose": "Once daily with meals",  "note": "Boosts immune response"},
        ],
        "precautions": [
            "Steam inhalation with eucalyptus oil twice daily",
            "Gargle with warm saline water 3 times a day",
            "Sleep with head slightly elevated",
            "Stay warm and avoid air conditioning",
            "Blow nose gently — do not sniff hard"
        ],
        "diet": ["Honey and ginger tea", "Warm turmeric milk (haldi doodh)", "Avoid dairy and cold drinks", "Eat light, warm meals"],
        "warning": "If cold persists beyond 10 days or develops into ear pain or sinus pressure, see a doctor.",
        "follow_up": "Common cold is viral — antibiotics will NOT help. Focus on rest and fluids."
    },
    "diabetes": {
        "aliases": ["diabetes", "blood sugar", "sugar level", "glucose high", "diabetic", "metformin", "insulin"],
        "medicines": [
            {"name": "Metformin 500mg",      "dose": "Twice daily with meals",  "note": "First-line type 2 diabetes drug"},
            {"name": "Glipizide 5mg",        "dose": "30 min before breakfast", "note": "Stimulates insulin release"},
            {"name": "Empagliflozin 10mg",   "dose": "Once daily",              "note": "Reduces blood sugar and heart risk"},
        ],
        "precautions": [
            "Check fasting and post-meal blood sugar every day",
            "Exercise for 30 minutes daily — walking or yoga is best",
            "Never skip meals when taking diabetes medication",
            "Get HbA1c tested every 3 months",
            "Carry glucose tablets in case of hypoglycemia (low sugar)"
        ],
        "diet": [
            "Low glycemic index foods: oats, legumes, brown rice",
            "Avoid white rice, white bread, sugar, sweets, and soft drinks",
            "Eat small frequent meals instead of large ones",
            "Include bitter gourd (karela) — natural blood sugar reducer"
        ],
        "warning": "If blood sugar drops below 70 mg/dL, eat something sweet immediately and call your doctor.",
        "follow_up": "Annual eye checkup, kidney function test, and foot examination are mandatory for diabetics."
    },
    "hypertension": {
        "aliases": ["blood pressure", "bp high", "hypertension", "high bp", "amlodipine", "bp medicine"],
        "medicines": [
            {"name": "Amlodipine 5mg",          "dose": "Once daily in the morning", "note": "Calcium channel blocker"},
            {"name": "Losartan 50mg",            "dose": "Once daily",               "note": "ARB — also protects kidneys"},
            {"name": "Hydrochlorothiazide 12.5mg","dose": "Once daily",              "note": "Diuretic — reduces fluid load"},
        ],
        "precautions": [
            "Monitor blood pressure at home twice daily (morning and evening)",
            "Reduce daily salt intake to less than 5 grams",
            "Never stop BP medication without doctor's advice — even if BP feels normal",
            "Manage stress with deep breathing and meditation",
            "Walk 30–45 minutes every day"
        ],
        "diet": [
            "DASH diet: fruits, vegetables, whole grains, low-fat dairy",
            "Avoid pickles, papads, namkeen, sauces, and processed meats",
            "Limit caffeine (max 1 cup coffee per day)",
            "Eat potassium-rich foods: banana, sweet potato, spinach"
        ],
        "warning": "If BP exceeds 180/120 mmHg, this is a hypertensive crisis — go to emergency immediately.",
        "follow_up": "Regular ECG and kidney function tests are recommended for long-term BP management."
    },
    "malaria": {
        "aliases": ["malaria", "mosquito", "chills fever", "plasmodium", "anti malarial"],
        "medicines": [
            {"name": "Artemether-Lumefantrine", "dose": "4 tabs twice daily × 3 days", "note": "First-line treatment"},
            {"name": "Chloroquine 250mg",        "dose": "As per body weight",          "note": "For P. vivax strain"},
            {"name": "Paracetamol 500mg",        "dose": "Every 6 hrs for fever",       "note": "Symptomatic relief only"},
        ],
        "precautions": [
            "Complete the FULL course of antimalarials even if you feel better",
            "Sleep under insecticide-treated mosquito nets",
            "Drain stagnant water near your home",
            "Apply DEET-based repellent on exposed skin",
            "Wear full-sleeve clothes after sunset"
        ],
        "diet": [
            "ORS (oral rehydration salts) for hydration",
            "Light easy-to-digest meals: khichdi, dal, rice",
            "Avoid spicy and oily food during treatment",
            "Papaya leaf juice to boost platelet count"
        ],
        "warning": "If no improvement within 48 hours, or if unconsciousness occurs, go to hospital IMMEDIATELY — severe malaria is life-threatening.",
        "follow_up": "Repeat blood test after 7 days to confirm parasite clearance."
    },
    "gastro": {
        "aliases": ["diarrhea", "vomiting", "stomach", "gastroenteritis", "loose motion", "nausea", "stomach ache"],
        "medicines": [
            {"name": "ORS (Oral Rehydration Salts)", "dose": "1 sachet in 1 litre, sip every 10–15 min", "note": "Most critical treatment"},
            {"name": "Ondansetron 4mg",              "dose": "Every 8 hrs for vomiting",                 "note": "Anti-nausea"},
            {"name": "Loperamide 2mg",               "dose": "After each loose stool (max 8mg/day)",     "note": "Reduces diarrhea"},
        ],
        "precautions": [
            "Hydration is the number one priority — ORS is better than plain water",
            "Start BRAT diet: Banana, Rice, Applesauce, Toast",
            "Avoid solid food for the first 6–8 hours",
            "Wash hands thoroughly before eating and after toilet",
            "Do not share utensils or food during illness"
        ],
        "diet": [
            "BRAT diet: banana, boiled rice, toast, applesauce",
            "ORS or coconut water to replace electrolytes",
            "Avoid dairy, spicy food, and fruit juices for 48 hrs",
            "Gradually reintroduce bland foods after 12 hours"
        ],
        "warning": "See a doctor if there is blood in stool, fever above 103°F, or if child shows signs of dehydration (sunken eyes, no urination).",
        "follow_up": "Most cases resolve in 3–5 days. If lasting longer, stool culture test recommended."
    },
    "thyroid": {
        "aliases": ["thyroid", "hypothyroidism", "tsh high", "levothyroxine", "tired weight gain", "underactive thyroid"],
        "medicines": [
            {"name": "Levothyroxine 50mcg",  "dose": "Once daily on empty stomach, 30 min before breakfast", "note": "Thyroid hormone replacement"},
            {"name": "Selenium 200mcg",      "dose": "Once daily with meals",                                 "note": "Supports thyroid gland function"},
        ],
        "precautions": [
            "Take Levothyroxine on EMPTY stomach — no food or drink (except water) for 30 minutes after",
            "Get TSH levels checked every 6 months",
            "Never skip doses — consistency is critical for thyroid health",
            "Inform ALL doctors you are on Levothyroxine — many drugs interact",
            "Avoid self-adjusting the dose based on symptoms"
        ],
        "diet": [
            "Iodine-rich foods: fish, eggs, dairy, iodised salt",
            "Selenium-rich foods: Brazil nuts, sunflower seeds",
            "Avoid soy products within 4 hours of taking your tablet",
            "Limit raw cruciferous vegetables in large amounts (cabbage, broccoli)"
        ],
        "warning": "Symptoms improve slowly over 4–6 weeks. Do not stop medicine if you feel better — hypothyroidism is lifelong.",
        "follow_up": "Annual thyroid panel (TSH, T3, T4) and anti-TPO antibody test recommended."
    },
    "anemia": {
        "aliases": ["anemia", "hemoglobin low", "tired weakness", "iron deficiency", "ferrous", "low hb"],
        "medicines": [
            {"name": "Ferrous Sulfate 200mg",  "dose": "Once daily with Vitamin C / orange juice", "note": "Iron supplement — improves with Vit C"},
            {"name": "Folic Acid 5mg",         "dose": "Once daily",                              "note": "Supports red blood cell production"},
            {"name": "Vitamin B12 500mcg",     "dose": "Once daily",                              "note": "If B12 deficiency is confirmed"},
        ],
        "precautions": [
            "Take iron supplements with orange juice — Vitamin C doubles absorption",
            "Do NOT take iron within 1 hour of tea, coffee, or calcium supplements",
            "Eat iron-rich foods: spinach, lentils, red meat, fortified cereals",
            "Check hemoglobin every 3 months until it normalises",
            "Rest adequately — anemia causes significant fatigue"
        ],
        "diet": [
            "Spinach, lentils (dal), kidney beans, and chickpeas",
            "Lean red meat, chicken, and fish",
            "Fortified breakfast cereals",
            "Pair iron foods with Vitamin C (lemon, orange) for better absorption"
        ],
        "warning": "If hemoglobin falls below 8 g/dL, hospitalisation and possible blood transfusion may be needed.",
        "follow_up": "Iron stores (serum ferritin) take 3–6 months to fully replenish even after hemoglobin normalises."
    },

    "dengue": {
        "aliases": ["dengue", "dengue fever", "platelet low", "platelet drop", "aedes", "bone break fever"],
        "medicines": [
            {"name": "Paracetamol 500mg",         "dose": "Every 6 hrs for fever",           "note": "ONLY fever reducer — DO NOT use Aspirin or Ibuprofen"},
            {"name": "ORS (Oral Rehydration Salts)","dose": "Sip continuously throughout day", "note": "Prevents dangerous dehydration"},
            {"name": "Papaya leaf extract",         "dose": "30ml juice twice daily",          "note": "Helps raise platelet count — consult doctor first"},
        ],
        "precautions": [
            "Monitor platelet count DAILY — hospitalise if below 50,000/µL",
            "Watch for danger signs: bleeding gums, blood in urine/stool, severe abdominal pain",
            "Complete bed rest — even mild exertion can cause internal bleeding",
            "NEVER take Aspirin, Ibuprofen, or Diclofenac — they increase bleeding risk",
            "Use mosquito nets and repellents to prevent re-infection",
            "Drink minimum 2.5 litres of fluid per day"
        ],
        "diet": [
            "Papaya leaf juice — natural platelet booster",
            "Pomegranate juice and kiwi for immune support",
            "Coconut water to restore electrolytes",
            "Soft foods: khichdi, boiled rice, dal",
            "Avoid spicy, oily, and raw foods completely"
        ],
        "warning": "Go to hospital IMMEDIATELY if platelet count falls below 50,000, or if you notice any bleeding, severe vomiting, or severe abdominal pain.",
        "follow_up": "Platelet count usually recovers by day 7–10. Follow-up blood test is essential."
    },

    "asthma": {
        "aliases": ["asthma", "wheezing", "breathless", "breathing difficulty", "inhaler", "bronchial", "chest tightness"],
        "medicines": [
            {"name": "Salbutamol inhaler (Ventolin)", "dose": "2 puffs every 4–6 hrs as needed",    "note": "Reliever — use during attacks"},
            {"name": "Budesonide inhaler",             "dose": "1–2 puffs twice daily",              "note": "Controller — reduces inflammation; use daily"},
            {"name": "Montelukast 10mg",               "dose": "Once at night",                      "note": "Long-term control; reduces airway inflammation"},
        ],
        "precautions": [
            "Always carry your reliever inhaler (Salbutamol) wherever you go",
            "Rinse mouth with water after using steroid inhaler to prevent oral thrush",
            "Identify and avoid triggers: dust, smoke, pollen, cold air, pet dander",
            "Use a peak flow meter to monitor lung function daily",
            "Never stop controller inhaler without doctor's advice, even if feeling well",
            "Get annual influenza vaccine — flu can trigger severe asthma attacks"
        ],
        "diet": [
            "Anti-inflammatory foods: turmeric, ginger, omega-3 rich fish (salmon, mackerel)",
            "Fruits high in antioxidants: apple, berries, pomegranate",
            "Avoid sulphite-containing foods: wine, dried fruits, pickles",
            "Avoid cold drinks, ice cream — cold can trigger bronchospasm",
            "Maintain healthy weight — obesity worsens asthma significantly"
        ],
        "warning": "If reliever inhaler provides no relief within 20 minutes or you cannot speak in full sentences, call 108 immediately — this is a severe attack.",
        "follow_up": "Review with pulmonologist every 3–6 months. Spirometry test to assess lung function annually."
    },

    "covid": {
        "aliases": ["covid", "covid-19", "coronavirus", "corona", "sars-cov", "covid fever", "covid cough", "loss of smell", "loss of taste"],
        "medicines": [
            {"name": "Paracetamol 500–650mg", "dose": "Every 6 hrs for fever/pain",          "note": "Primary symptomatic treatment"},
            {"name": "Zinc 50mg + Vitamin C 500mg", "dose": "Once daily with meals",         "note": "Immune support supplements"},
            {"name": "Vitamin D3 60,000 IU",  "dose": "Once weekly for 4 weeks",             "note": "Corrects deficiency; supports immunity"},
            {"name": "Dexamethasone 6mg",     "dose": "Once daily × 10 days (hospital only)","note": "For severe/critical COVID with oxygen support"},
        ],
        "precautions": [
            "Isolate for minimum 7 days from symptom onset or positive test",
            "Monitor SpO2 with pulse oximeter every 4 hrs — seek help if below 94%",
            "Lie in prone position (on stomach) to improve oxygen levels",
            "Seek emergency care if: breathlessness, SpO2 below 93%, confusion, or chest pain",
            "Wear N95 mask; ventilate rooms well",
            "Avoid self-prescribing steroids — they are only for severe cases"
        ],
        "diet": [
            "Warm ginger-tulsi-clove kadha twice daily",
            "High protein: eggs, dal, paneer, chicken (for recovery)",
            "Amla, citrus fruits, guava — rich in Vitamin C",
            "Stay very well hydrated: 3+ litres of warm fluids daily",
            "Avoid junk food, alcohol, and smoking completely"
        ],
        "warning": "Emergency signs: SpO2 below 93%, severe breathlessness, persistent chest pain, confusion, blue lips. Call 108 immediately.",
        "follow_up": "Post-COVID fatigue and breathlessness can last weeks. Pulmonary rehab exercises help. Get 6-minute walk test if breathlessness persists."
    },

    "typhoid": {
        "aliases": ["typhoid", "typhoid fever", "enteric fever", "salmonella", "azithromycin fever", "high fever week"],
        "medicines": [
            {"name": "Azithromycin 500mg",    "dose": "Once daily × 7 days",                "note": "First-line oral antibiotic"},
            {"name": "Ciprofloxacin 500mg",   "dose": "Twice daily × 10–14 days",            "note": "Alternative if Azithromycin resistance"},
            {"name": "Ceftriaxone 2g IV",     "dose": "Once daily (hospital — severe cases)","note": "Intravenous for complicated typhoid"},
            {"name": "Paracetamol 500mg",     "dose": "Every 6 hrs",                         "note": "Fever and discomfort relief"},
        ],
        "precautions": [
            "COMPLETE the full antibiotic course — stopping early causes relapse",
            "Strict hand hygiene: wash hands after toilet and before every meal",
            "Drink only boiled or bottled water throughout treatment",
            "Avoid street food, raw vegetables, and unpeeled fruits",
            "Report back immediately if fever does not subside within 5 days of antibiotics",
            "Get Widal test and blood culture to confirm diagnosis"
        ],
        "diet": [
            "Soft, easily digestible foods: khichdi, idli, boiled rice, banana",
            "Boiled or steamed vegetables only",
            "Coconut water, ORS, and buttermilk for hydration",
            "Avoid raw salads, high-fibre foods, spicy curries, and milk during fever",
            "Gradually reintroduce normal food only after fever fully breaks"
        ],
        "warning": "Seek urgent care if: abdomen becomes very rigid and painful (risk of perforation), or fever exceeds 104°F for more than 3 days.",
        "follow_up": "Stool culture test after treatment completion to confirm full clearance. Typhoid vaccine recommended for prevention."
    },

    "chickenpox": {
        "aliases": ["chickenpox", "chicken pox", "varicella", "pox", "itchy blisters", "blister rash", "pox rash"],
        "medicines": [
            {"name": "Acyclovir 800mg",      "dose": "5 times daily × 7 days (start within 24 hrs of rash)", "note": "Antiviral — shortens duration and severity"},
            {"name": "Calamine lotion",      "dose": "Apply to rashes 3–4 times daily",                     "note": "Soothes itching and dries blisters"},
            {"name": "Cetirizine 10mg",      "dose": "Once at night",                                        "note": "Controls intense itching"},
            {"name": "Paracetamol 500mg",    "dose": "Every 6 hrs for fever",                               "note": "NEVER give Aspirin to children with chickenpox"},
        ],
        "precautions": [
            "Strict isolation for 7 days or until all blisters have crusted over",
            "Trim fingernails short and wear cotton gloves at night to prevent scratching",
            "Do NOT scratch — causes permanent scars and secondary bacterial infection",
            "Bathe with neem water or oatmeal bath to soothe skin",
            "Wash clothes and bedding daily in hot water",
            "Keep away from pregnant women, newborns, and immunocompromised people"
        ],
        "diet": [
            "Soft, cool foods: yogurt, banana, rice, boiled vegetables",
            "Plenty of fluids: water, coconut water, diluted fruit juices",
            "Neem leaves boiled water bath — antiviral and anti-itch",
            "Avoid spicy, salty, and acidic foods (worsen mouth sores)",
            "Avoid non-veg food until fully recovered"
        ],
        "warning": "See doctor immediately if: blisters become very red and painful (bacterial infection), high fever (above 104°F), stiff neck, or severe headache.",
        "follow_up": "Varicella vaccine prevents future infection. Shingles (herpes zoster) can occur years later from the same virus."
    },

    "migraine": {
        "aliases": ["migraine", "severe headache", "one side headache", "throbbing headache", "headache nausea", "migraine attack", "aura headache"],
        "medicines": [
            {"name": "Sumatriptan 50mg",           "dose": "At onset of headache — repeat after 2 hrs if needed", "note": "Triptan — most effective; do NOT use with ergotamines"},
            {"name": "Ibuprofen 400mg",            "dose": "At onset, with food",                                 "note": "OTC option for mild to moderate migraines"},
            {"name": "Domperidone 10mg",           "dose": "30 min before pain reliever",                        "note": "Controls nausea and improves absorption"},
            {"name": "Propranolol 40mg (preventive)","dose": "Twice daily (prescribed for frequent migraines)",   "note": "Reduces frequency — not for acute attacks"},
        ],
        "precautions": [
            "Maintain a headache diary — note triggers, duration, severity",
            "Stick to consistent sleep and wake times — irregular sleep is a top trigger",
            "Stay hydrated — dehydration is a very common migraine trigger",
            "Dim lights and reduce noise during an attack; rest in dark quiet room",
            "Apply ice pack to forehead and hot pack to neck/shoulders",
            "Do not overuse pain relievers — more than 10 days/month causes rebound headaches"
        ],
        "diet": [
            "Magnesium-rich foods: almonds, spinach, pumpkin seeds, dark chocolate",
            "Stay hydrated with water and coconut water throughout day",
            "Avoid common triggers: red wine, aged cheese, MSG, processed meats, artificial sweeteners",
            "Never skip meals — fasting is a major migraine trigger",
            "Limit caffeine to 1 cup/day; abrupt caffeine withdrawal also triggers migraines"
        ],
        "warning": "Seek emergency care for: worst headache of your life (thunderclap headache), headache with fever + stiff neck, or headache following head injury.",
        "follow_up": "Neurologist consultation recommended if migraines occur more than 4 times/month. CGRP inhibitors are a newer preventive option."
    },

    "uti": {
        "aliases": ["uti", "urinary infection", "burning urination", "frequent urination", "urine infection", "painful urination", "bladder infection"],
        "medicines": [
            {"name": "Nitrofurantoin 100mg",       "dose": "Twice daily × 5 days",   "note": "First-line for uncomplicated UTI"},
            {"name": "Trimethoprim-Sulfamethoxazole","dose": "Twice daily × 3 days", "note": "Alternative first-line; check local resistance"},
            {"name": "Fosfomycin 3g",              "dose": "Single dose",             "note": "Single-dose option — convenient"},
            {"name": "Phenazopyridine 200mg",      "dose": "3 times daily after meals","note": "Relieves burning sensation — NOT an antibiotic"},
        ],
        "precautions": [
            "Drink 2.5–3 litres of water daily to flush bacteria",
            "Urinate immediately after sexual intercourse",
            "Always wipe from front to back after using the toilet",
            "Do not hold urine for long periods",
            "Wear breathable cotton underwear; avoid tight synthetic clothing",
            "Complete the full antibiotic course even if symptoms improve early"
        ],
        "diet": [
            "Unsweetened cranberry juice — prevents bacteria from sticking to bladder wall",
            "Plenty of water and coconut water throughout the day",
            "Probiotics: yogurt and buttermilk to restore gut-urinary microbiome",
            "Vitamin C foods: amla, lemon, guava (acidifies urine, inhibits bacterial growth)",
            "Avoid alcohol, caffeine, spicy foods, and carbonated drinks — they irritate the bladder"
        ],
        "warning": "See a doctor urgently if you develop fever above 101°F, back/flank pain, or vomiting — this suggests kidney infection (pyelonephritis).",
        "follow_up": "Urine culture after treatment confirms clearance. Recurrent UTIs (3+ per year) need urological evaluation."
    },

    "arthritis": {
        "aliases": ["arthritis", "joint pain", "knee pain", "swollen joints", "rheumatoid", "osteoarthritis", "gout", "joint swelling", "joint stiffness"],
        "medicines": [
            {"name": "Ibuprofen 400mg",           "dose": "3 times daily with food",                         "note": "NSAID — reduces pain and inflammation"},
            {"name": "Diclofenac gel 1%",         "dose": "Apply to affected joint 3–4 times daily",         "note": "Topical — fewer side effects"},
            {"name": "Hydroxychloroquine 200mg",  "dose": "Twice daily (for Rheumatoid Arthritis)",          "note": "Disease modifier — needs doctor prescription"},
            {"name": "Calcium 500mg + Vit D3",    "dose": "Twice daily with meals",                          "note": "Protects bones and reduces joint deterioration"},
        ],
        "precautions": [
            "Do low-impact daily exercise: swimming, cycling, yoga — rest worsens stiffness",
            "Apply warm compress for morning stiffness; cold pack for acute swelling",
            "Maintain healthy weight — every 1 kg loss reduces knee load by 4 kg",
            "Use ergonomic support: proper footwear, knee braces if needed",
            "Physical therapy is as effective as medication for many arthritis types",
            "Avoid prolonged sitting or standing in one position"
        ],
        "diet": [
            "Omega-3 fatty acids: fatty fish (salmon, sardines), walnuts, flaxseeds — natural anti-inflammatory",
            "Turmeric with black pepper (curcumin + piperine) — powerful joint inflammation reducer",
            "Cherries, berries, and colourful vegetables for antioxidants",
            "Calcium and Vitamin D: dairy, ragi (finger millet), sesame seeds",
            "Avoid refined sugar, processed food, red meat, and excess alcohol — worsen inflammation"
        ],
        "warning": "See a rheumatologist if joints are very swollen, warm to touch, or morning stiffness lasts more than 1 hour — could be Rheumatoid Arthritis needing early treatment.",
        "follow_up": "Annual X-ray or MRI to monitor joint damage. RF (Rheumatoid Factor) and anti-CCP blood tests help classify the type."
    },

    "acid_reflux": {
        "aliases": ["acidity", "acid reflux", "gerd", "heartburn", "chest burning", "acid", "burping", "sour belching", "indigestion", "gastritis"],
        "medicines": [
            {"name": "Omeprazole 20mg (PPI)",      "dose": "30 min before breakfast, daily",    "note": "Most effective — reduces stomach acid production"},
            {"name": "Pantoprazole 40mg (PPI)",    "dose": "30 min before breakfast",            "note": "Alternative PPI — slightly longer acting"},
            {"name": "Ranitidine / Famotidine",    "dose": "Twice daily before meals",           "note": "H2 blocker — milder option for mild acidity"},
            {"name": "Antacid (Gelusil, Digene)",  "dose": "2 tablets after meals as needed",   "note": "Instant relief — not a long-term solution"},
        ],
        "precautions": [
            "Eat smaller, more frequent meals — avoid large meals especially at dinner",
            "Do not lie down for at least 2–3 hours after eating",
            "Elevate head of bed by 15–20 cm if you have nighttime reflux",
            "Avoid smoking and alcohol — they relax the lower esophageal sphincter",
            "Wear loose-fitting clothing — tight waistbands worsen reflux",
            "Do not take NSAIDs (Ibuprofen, Aspirin) on empty stomach"
        ],
        "diet": [
            "Alkaline foods: banana, melon, cucumber, oatmeal, boiled vegetables",
            "Coconut water and cold milk provide quick relief",
            "Avoid: citrus fruits, tomatoes, onions, garlic, coffee, tea, chocolate, spicy food",
            "Chew food slowly and thoroughly; avoid eating in a hurry",
            "Fennel seeds (saunf) and jeera water after meals aid digestion naturally"
        ],
        "warning": "See a doctor if you have difficulty swallowing, unexplained weight loss, persistent vomiting, or vomiting blood — these need endoscopy to rule out serious conditions.",
        "follow_up": "Endoscopy (OGD scope) recommended if symptoms persist beyond 4 weeks on medication or recur frequently."
    },

    "jaundice": {
        "aliases": ["jaundice", "yellow eyes", "yellow skin", "hepatitis", "liver problem", "bilirubin high", "yellow urine", "liver infection"],
        "medicines": [
            {"name": "Ursodeoxycholic acid (UDCA)", "dose": "As prescribed by doctor",            "note": "Improves bile flow and liver function"},
            {"name": "Liv 52 (herbal liver tonic)", "dose": "2 tablets twice daily",              "note": "Ayurvedic liver support — safe and commonly used"},
            {"name": "Antiviral (Tenofovir/Entecavir)","dose": "As prescribed (for Hepatitis B)", "note": "Suppresses viral replication — must be prescribed"},
            {"name": "Cholestyramine",               "dose": "As prescribed",                     "note": "Reduces bile acid-related itching"},
        ],
        "precautions": [
            "Complete bed rest is essential — liver needs rest to heal",
            "STOP all alcohol completely — even small amounts are severely toxic to a damaged liver",
            "Avoid ALL unnecessary medicines including Paracetamol — consult doctor for any medication",
            "Use separate utensils — Hepatitis A and E are highly contagious",
            "Get liver function tests (LFT) and bilirubin levels checked every 3–5 days",
            "Avoid fatty and oily foods entirely during recovery"
        ],
        "diet": [
            "Sugarcane juice — popular home remedy to support liver recovery",
            "Fresh fruits: papaya, watermelon, amla — rich in antioxidants",
            "Boiled or steamed vegetables: gourd, pumpkin, spinach",
            "Coconut water — natural electrolyte and liver soother",
            "Avoid: alcohol, oil, ghee, fried food, red meat, excess protein during acute phase"
        ],
        "warning": "Seek IMMEDIATE hospital care if: jaundice worsens rapidly, confusion or drowsiness occurs (liver encephalopathy), severe abdominal swelling, or bleeding from gums or vomiting blood.",
        "follow_up": "Liver function test (LFT), bilirubin, and Hepatitis serology panel are key follow-up tests. Hepatitis B vaccination recommended for contacts."
    }
}

# ─── General FAQ responses ─────────────────────────────────────────────────────

GENERAL_RESPONSES = {
    "greet": {
        "triggers": ["hello", "hi", "hey", "good morning", "good evening", "namaste"],
        "response": "Hello! I am MedAssist, your AI patient support assistant. I can help you with medicines, precautions, diet advice, and health tips for common conditions. What would you like to know?"
    },
    "thanks": {
        "triggers": ["thank", "thanks", "great", "helpful", "good"],
        "response": "You're welcome! Remember — this information is for general guidance only. Always consult a licensed doctor for diagnosis and personalised treatment. Take care of your health!"
    },
    "emergency": {
        "triggers": ["emergency", "chest pain", "can't breathe", "unconscious", "stroke", "heart attack", "severe"],
        "response": "⚠ THIS SOUNDS LIKE A MEDICAL EMERGENCY. Please call emergency services (108 in India / 911 in US) or go to the nearest hospital emergency room IMMEDIATELY. Do not wait."
    },
    "antibiotic": {
        "triggers": ["antibiotic", "amoxicillin", "azithromycin", "ciprofloxacin"],
        "response": "Antibiotics must ONLY be taken with a doctor's prescription. Never self-medicate with antibiotics — misuse causes antibiotic resistance. Please consult a doctor who will prescribe the right antibiotic based on your specific infection."
    },
    "dosage": {
        "triggers": ["how much", "dosage", "dose", "how many tablets", "how often"],
        "response": "Dosages vary based on your age, weight, kidney/liver health, and other medicines you take. The doses I mention are general adult guidelines. Always follow your doctor's or pharmacist's specific instructions for your prescription."
    },
    "side_effects": {
        "triggers": ["side effect", "reaction", "allergy", "rash after medicine", "medicine causing"],
        "response": "If you experience a serious side effect (rash, swelling, difficulty breathing, severe stomach pain), STOP the medicine and see a doctor immediately. For mild side effects like nausea or headache, consult your doctor before stopping the medicine."
    }
}


# ─── Matching Engine ──────────────────────────────────────────────────────────

def _find_disease_match(text: str) -> str | None:
    """Return disease key if message matches any known disease"""
    t = text.lower()
    for key, info in SUPPORT_DB.items():
        if any(alias in t for alias in info["aliases"]):
            return key
    return None


def _find_general_match(text: str) -> str | None:
    """Return a general FAQ response if it matches"""
    t = text.lower()
    for key, info in GENERAL_RESPONSES.items():
        if any(trigger in t for trigger in info["triggers"]):
            return info["response"]
    return None


def _build_disease_response(key: str, intent: str) -> dict:
    """Build a structured response for a matched disease"""
    info = SUPPORT_DB[key]

    if "medicine" in intent or "tablet" in intent or "drug" in intent or "treat" in intent:
        return {
            "type": "medicines",
            "disease": key,
            "disease_label": key.replace("_", " ").title(),
            "medicines": info["medicines"],
            "warning": info["warning"],
            "message": f"Here are the medicines commonly used for {key.replace('_',' ').title()}:"
        }
    elif "diet" in intent or "eat" in intent or "food" in intent or "avoid" in intent:
        return {
            "type": "diet",
            "disease": key,
            "disease_label": key.replace("_", " ").title(),
            "diet": info["diet"],
            "message": f"Diet advice for {key.replace('_',' ').title()}:"
        }
    else:
        # Default: full support card
        return {
            "type": "full",
            "disease": key,
            "disease_label": key.replace("_", " ").title(),
            "medicines": info["medicines"],
            "precautions": info["precautions"],
            "diet": info["diet"],
            "warning": info["warning"],
            "follow_up": info["follow_up"],
            "message": f"Complete support guide for {key.replace('_',' ').title()}:"
        }


# ─── Main Chat Function ───────────────────────────────────────────────────────

def get_support(message: str, disease: str = "") -> dict:
    """
    Main function called by Flask route /chat
    Input : message (user text), disease (optional — passed from Module 1)
    Output: structured response dict
    """
    if not message.strip():
        return {
            "type": "error",
            "message": "Please type a question or describe your condition."
        }

    text = message.lower().strip()

    # Priority 1: Emergency check
    general = _find_general_match(text)
    if "emergency" in _find_general_match(text + " emergency").lower() if "emergency" in text or "chest pain" in text or "unconscious" in text else False:
        return {"type": "general", "message": GENERAL_RESPONSES["emergency"]["response"]}

    # Priority 2: If disease was passed from Module 1, use it directly
    if disease and disease.lower() in SUPPORT_DB:
        return _build_disease_response(disease.lower(), text)

    # Priority 3: Try to match disease from message text
    matched_disease = _find_disease_match(text)
    if matched_disease:
        return _build_disease_response(matched_disease, text)

    # Priority 4: General FAQ
    if general:
        return {"type": "general", "message": general}

    # Fallback
    return {
        "type": "fallback",
        "message": "I can provide support for: flu, cold, diabetes, hypertension, malaria, gastroenteritis, thyroid, anemia, dengue, asthma, COVID-19, typhoid, chickenpox, migraine, UTI, arthritis, acid reflux, and jaundice. Please mention your condition or disease name, and I will give you medicines, precautions, and diet advice.",
        "suggestions": list(SUPPORT_DB.keys())
    }


def get_all_diseases() -> list:
    """Return all supported disease names for frontend display"""
    return [
        {"key": k, "label": k.replace("_", " ").title()}
        for k in SUPPORT_DB.keys()
    ]
