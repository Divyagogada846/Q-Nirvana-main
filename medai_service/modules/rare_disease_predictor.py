# modules/rare_disease_predictor.py
# ─────────────────────────────────────────────────────────────────────────────
# Module 5 — Rare Disease Predictor
# Accepts: gene name, variant notation, VUS classification inputs
# Returns: ranked rare disease candidates, ACMG criteria, confidence, management
# Data based on: Orphanet, OMIM, ClinVar, ACMG 2015 guidelines
# ─────────────────────────────────────────────────────────────────────────────

# ══════════════════════════════════════════════════════════════════════════════
# RARE DISEASE DATABASE  (subset of Orphanet / OMIM)
# Each entry: gene → { disease info, acmg criteria, variant patterns }
# ══════════════════════════════════════════════════════════════════════════════

RARE_DISEASE_DB = {
    "NF1": {
        "disease": "Neurofibromatosis Type 1",
        "omim": "162200",
        "orpha": "636",
        "inheritance": "Autosomal Dominant",
        "prevalence": "1 in 3,000",
        "chromosome": "17q11.2",
        "acmg_class": "Pathogenic",
        "severity": "high",
        "onset": "Childhood",
        "icd10": "Q85.0",
        "symptoms": [
            "Café-au-lait macules (≥6 spots >5mm)",
            "Cutaneous neurofibromas",
            "Lisch nodules (iris hamartomas)",
            "Optic pathway glioma",
            "Learning disabilities",
            "Scoliosis",
            "Freckling in axillary/inguinal regions"
        ],
        "pathogenic_variants": ["frameshift", "nonsense", "splice_site", "deletion", "duplication"],
        "vus_patterns": ["missense", "synonymous"],
        "known_variants": ["p.Arg1947*", "p.Gln2140*", "p.Arg816*", "c.2033del"],
        "management": [
            "Annual dermatology and ophthalmology review",
            "Regular neurological assessment",
            "MEK inhibitor (Selumetinib) for plexiform neurofibromas",
            "MRI brain/spine if neurological symptoms",
            "Genetic counselling for family members"
        ],
        "clinvar_significance": "Pathogenic/Likely pathogenic",
        "research_refs": ["PMID:32109273", "PMID:30078418"],
        "category": "Neurocutaneous"
    },
    "MEFV": {
        "disease": "Familial Mediterranean Fever",
        "omim": "249100",
        "orpha": "342",
        "inheritance": "Autosomal Recessive",
        "prevalence": "1 in 1,000 (Mediterranean)",
        "chromosome": "16p13.3",
        "acmg_class": "Likely Pathogenic",
        "severity": "high",
        "onset": "Childhood (<20 years in 90%)",
        "icd10": "E85.0",
        "symptoms": [
            "Recurrent fever episodes (38–40°C, lasting 1–3 days)",
            "Abdominal pain / peritonitis",
            "Pleuritis / chest pain",
            "Arthritis (large joints)",
            "Skin erysipelas-like erythema",
            "Risk of AA amyloidosis",
            "Elevated CRP/ESR during attacks"
        ],
        "pathogenic_variants": ["missense", "compound_heterozygous"],
        "vus_patterns": ["missense", "synonymous"],
        "known_variants": ["M694V", "M680I", "V726A", "M694I", "E148Q"],
        "management": [
            "Colchicine 1–2mg/day (prevents attacks and amyloidosis)",
            "IL-1 inhibitors: Anakinra or Canakinumab for refractory cases",
            "Kidney function monitoring (amyloidosis risk)",
            "Avoid known attack triggers",
            "Regular ESR/CRP monitoring"
        ],
        "clinvar_significance": "Likely pathogenic",
        "research_refs": ["PMID:29097088", "PMID:31585107"],
        "category": "Autoinflammatory"
    },
    "GLA": {
        "disease": "Fabry Disease",
        "omim": "301500",
        "orpha": "324",
        "inheritance": "X-linked",
        "prevalence": "1 in 40,000–170,000",
        "chromosome": "Xq22.1",
        "acmg_class": "VUS → Likely Pathogenic",
        "severity": "high",
        "onset": "Childhood (classic) / Adulthood (late-onset)",
        "icd10": "E75.21",
        "symptoms": [
            "Acroparesthesia (burning pain in hands/feet)",
            "Angiokeratomas (skin)",
            "Cornea verticillata",
            "Cardiac hypertrophy / arrhythmia",
            "Progressive renal failure (proteinuria)",
            "Stroke / TIA",
            "Reduced alpha-galactosidase A enzyme activity"
        ],
        "pathogenic_variants": ["missense", "nonsense", "frameshift", "splice_site"],
        "vus_patterns": ["missense"],
        "known_variants": ["c.644A>G", "p.Asn215Ser", "p.Arg112His", "c.1066C>T"],
        "management": [
            "Enzyme Replacement Therapy: Agalsidase alfa (0.2mg/kg IV q2w)",
            "Pharmacological chaperone: Migalastat 123mg oral (amenable variants only)",
            "ACE inhibitors for proteinuria",
            "Nephrology follow-up (eGFR annually)",
            "Cardiology review (ECG, Echo annually)",
            "Antiplatelet/anticoagulation for stroke prevention"
        ],
        "clinvar_significance": "VUS / Likely pathogenic",
        "research_refs": ["PMID:31735529", "PMID:29914908"],
        "category": "Lysosomal Storage"
    },
    "ATP7B": {
        "disease": "Wilson Disease",
        "omim": "277900",
        "orpha": "905",
        "inheritance": "Autosomal Recessive",
        "prevalence": "1 in 30,000",
        "chromosome": "13q14.3",
        "acmg_class": "Likely Pathogenic",
        "severity": "high",
        "onset": "5–35 years",
        "icd10": "E83.01",
        "symptoms": [
            "Kayser-Fleischer rings (copper in cornea)",
            "Liver disease: hepatitis → cirrhosis",
            "Neurological: tremor, dysarthria, dystonia",
            "Psychiatric symptoms (personality change)",
            "Low serum ceruloplasmin (<20mg/dL)",
            "Elevated 24h urine copper",
            "Haemolytic anaemia"
        ],
        "pathogenic_variants": ["missense", "nonsense", "frameshift"],
        "vus_patterns": ["missense"],
        "known_variants": ["p.His1069Gln", "p.Arg778Leu", "p.Met769Val", "c.3207C>A"],
        "management": [
            "D-Penicillamine 750–1500mg/day (chelation therapy)",
            "Trientine 750–1500mg/day (if intolerant to penicillamine)",
            "Zinc acetate 150mg/day (maintenance / presymptomatic)",
            "Low copper diet (avoid liver, shellfish, nuts, chocolate)",
            "Liver transplant if fulminant hepatic failure",
            "Annual liver function tests and neurological review"
        ],
        "clinvar_significance": "Likely pathogenic",
        "research_refs": ["PMID:31373261", "PMID:28890682"],
        "category": "Metabolic"
    },
    "COL3A1": {
        "disease": "Vascular Ehlers-Danlos Syndrome (vEDS)",
        "omim": "130050",
        "orpha": "286",
        "inheritance": "Autosomal Dominant",
        "prevalence": "1 in 50,000–200,000",
        "chromosome": "2q32.2",
        "acmg_class": "VUS",
        "severity": "critical",
        "onset": "Any age",
        "icd10": "Q79.61",
        "symptoms": [
            "Arterial rupture (especially aorta, celiac, renal arteries)",
            "Intestinal perforation",
            "Uterine rupture (in pregnancy)",
            "Thin translucent skin with visible veins",
            "Characteristic facies",
            "Easy bruising",
            "Small joint hypermobility"
        ],
        "pathogenic_variants": ["missense", "splice_site", "glycine_substitution"],
        "vus_patterns": ["missense", "glycine_substitution"],
        "known_variants": ["p.Gly328Ser", "p.Gly436Arg", "p.Gly252Val"],
        "management": [
            "Celiprolol (beta-blocker) to reduce arterial events",
            "Avoid contact sports, heavy lifting, straining",
            "Annual vascular imaging (CT angiography or MRI)",
            "Emergency protocols for unexplained severe pain",
            "Obstetric high-risk unit for any pregnancy",
            "Medical alert bracelet strongly recommended"
        ],
        "clinvar_significance": "VUS / Likely pathogenic",
        "research_refs": ["PMID:30679817", "PMID:29283194"],
        "category": "Connective Tissue"
    },
    "CFTR": {
        "disease": "Cystic Fibrosis",
        "omim": "219700",
        "orpha": "586",
        "inheritance": "Autosomal Recessive",
        "prevalence": "1 in 2,500–3,500 (Caucasian)",
        "chromosome": "7q31.2",
        "acmg_class": "Pathogenic",
        "severity": "high",
        "onset": "Birth / Early childhood",
        "icd10": "E84.9",
        "symptoms": [
            "Chronic productive cough",
            "Recurrent pulmonary infections (Pseudomonas, Staph aureus)",
            "Bronchiectasis",
            "Pancreatic insufficiency / malabsorption",
            "Failure to thrive in children",
            "Elevated sweat chloride (>60 mmol/L)",
            "Male infertility (congenital absence of vas deferens)"
        ],
        "pathogenic_variants": ["deletion", "missense", "nonsense", "frameshift"],
        "vus_patterns": ["missense"],
        "known_variants": ["p.Phe508del", "p.Gly542*", "p.Arg117His", "p.Trp1282*"],
        "management": [
            "CFTR modulators: Elexacaftor/Tezacaftor/Ivacaftor (Trikafta) — F508del eligible",
            "Airway clearance physiotherapy twice daily",
            "Inhaled DNase (Dornase alfa) and hypertonic saline",
            "Pancreatic enzyme replacement with meals",
            "High-calorie, high-fat diet",
            "Annual pulmonary function tests and sputum cultures"
        ],
        "clinvar_significance": "Pathogenic",
        "research_refs": ["PMID:31661651", "PMID:32979940"],
        "category": "Pulmonary"
    },
    "FBN1": {
        "disease": "Marfan Syndrome",
        "omim": "154700",
        "orpha": "558",
        "inheritance": "Autosomal Dominant",
        "prevalence": "1 in 5,000",
        "chromosome": "15q21.1",
        "acmg_class": "Pathogenic",
        "severity": "high",
        "onset": "Birth / Any age",
        "icd10": "Q87.40",
        "symptoms": [
            "Aortic root dilatation / dissection",
            "Ectopia lentis (lens dislocation)",
            "Tall stature with disproportionately long limbs",
            "Scoliosis and chest deformities (pectus)",
            "Arm span-to-height ratio >1.05",
            "High-arched palate",
            "Spontaneous pneumothorax"
        ],
        "pathogenic_variants": ["missense", "nonsense", "frameshift", "splice_site"],
        "vus_patterns": ["missense"],
        "known_variants": ["p.Cys1663Arg", "p.Arg2726Trp", "p.Gly1796Ser"],
        "management": [
            "Losartan 25–100mg/day or atenolol (aortic protection)",
            "Annual echocardiogram to monitor aortic root",
            "Elective aortic root surgery if diameter >4.5–5.0cm",
            "Ophthalmology annual review",
            "Avoid contact sports and isometric exercise",
            "Pre-pregnancy counselling (50% transmission risk)"
        ],
        "clinvar_significance": "Pathogenic",
        "research_refs": ["PMID:30596005", "PMID:28317521"],
        "category": "Connective Tissue"
    },
    "HEXA": {
        "disease": "Tay-Sachs Disease",
        "omim": "272800",
        "orpha": "845",
        "inheritance": "Autosomal Recessive",
        "prevalence": "1 in 320,000 (1 in 27 Ashkenazi Jewish)",
        "chromosome": "15q23",
        "acmg_class": "Pathogenic",
        "severity": "critical",
        "onset": "3–6 months (infantile) / Adult-onset forms exist",
        "icd10": "E75.01",
        "symptoms": [
            "Progressive neurodegeneration",
            "Cherry-red spot on macula",
            "Exaggerated startle response",
            "Seizures",
            "Progressive muscle weakness",
            "Loss of motor/mental milestones",
            "Megalencephaly (head enlargement)"
        ],
        "pathogenic_variants": ["frameshift", "splice_site", "nonsense", "missense"],
        "vus_patterns": ["missense"],
        "known_variants": ["c.1278insTATC", "c.1421+1G>C", "p.Arg247Trp"],
        "management": [
            "No disease-modifying therapy currently available",
            "Supportive care: anti-epileptics for seizures",
            "Nutritional support and PEG tube if swallowing affected",
            "Physiotherapy to maintain function",
            "Palliative care coordination",
            "Carrier testing for family members (especially Ashkenazi Jewish)"
        ],
        "clinvar_significance": "Pathogenic",
        "research_refs": ["PMID:30945348", "PMID:28671673"],
        "category": "Lysosomal Storage"
    },
    "GBA": {
        "disease": "Gaucher Disease Type 1",
        "omim": "230800",
        "orpha": "355",
        "inheritance": "Autosomal Recessive",
        "prevalence": "1 in 40,000 (1 in 900 Ashkenazi Jewish)",
        "chromosome": "1q22",
        "acmg_class": "Pathogenic",
        "severity": "medium",
        "onset": "Any age",
        "icd10": "E75.22",
        "symptoms": [
            "Hepatosplenomegaly (massive spleen)",
            "Bone pain and bone crises",
            "Anaemia and thrombocytopenia",
            "Fatigue",
            "Growth retardation in children",
            "Reduced glucocerebrosidase enzyme activity",
            "Elevated chitotriosidase"
        ],
        "pathogenic_variants": ["missense", "deletion", "frameshift"],
        "vus_patterns": ["missense"],
        "known_variants": ["p.Asn409Ser (N370S)", "p.Leu483Pro (L444P)", "84GG"],
        "management": [
            "Enzyme Replacement Therapy: Imiglucerase or Velaglucerase alfa (IV q2w)",
            "Substrate Reduction Therapy: Miglustat or Eliglustat (oral)",
            "Splenomegaly monitoring — avoid splenectomy if ERT available",
            "Annual CBC, liver function, ferritin",
            "DEXA scan for bone density",
            "Parkinson disease surveillance (GBA is PD risk factor)"
        ],
        "clinvar_significance": "Pathogenic",
        "research_refs": ["PMID:31104288", "PMID:27353728"],
        "category": "Lysosomal Storage"
    },
    "PKD1": {
        "disease": "Autosomal Dominant Polycystic Kidney Disease",
        "omim": "173900",
        "orpha": "730",
        "inheritance": "Autosomal Dominant",
        "prevalence": "1 in 400–1,000",
        "chromosome": "16p13.3",
        "acmg_class": "Pathogenic",
        "severity": "high",
        "onset": "30–60 years (symptoms) / Birth (cysts)",
        "icd10": "Q61.2",
        "symptoms": [
            "Bilateral renal cysts → progressive CKD",
            "Flank pain and haematuria",
            "Hypertension (early sign)",
            "Intracranial aneurysms (5–10%)",
            "Liver cysts",
            "Mitral valve prolapse",
            "ESRD in 50% by age 60"
        ],
        "pathogenic_variants": ["frameshift", "nonsense", "missense", "splice_site"],
        "vus_patterns": ["missense"],
        "known_variants": ["p.Arg3277Cys", "p.Gln2199*", "c.7880+1G>T"],
        "management": [
            "Tolvaptan (V2R antagonist) to slow cyst growth — ADPKD-specific",
            "Strict blood pressure control (<130/80 mmHg)",
            "Annual renal ultrasound and eGFR",
            "MRA/CTA for intracranial aneurysm screening (if family history)",
            "Dialysis/transplant planning when GFR <15",
            "Avoid nephrotoxic agents (NSAIDs, contrast)"
        ],
        "clinvar_significance": "Pathogenic/Likely pathogenic",
        "research_refs": ["PMID:29379140", "PMID:26756418"],
        "category": "Renal"
    }
}

# ══════════════════════════════════════════════════════════════════════════════
# VUS CLASSIFICATION  (ACMG 2015 framework, simplified rule engine)
# ══════════════════════════════════════════════════════════════════════════════

ACMG_CRITERIA = {
    "PVS1": {"weight": 8, "desc": "Null variant (nonsense/frameshift/splice) in loss-of-function gene"},
    "PS1":  {"weight": 7, "desc": "Same amino acid change as established pathogenic variant"},
    "PS2":  {"weight": 7, "desc": "De novo (confirmed) in patient with disease, no family history"},
    "PS3":  {"weight": 6, "desc": "Functional studies showing damaging effect"},
    "PS4":  {"weight": 6, "desc": "Prevalence significantly increased in affected vs controls"},
    "PM1":  {"weight": 4, "desc": "Located in mutational hot spot / critical functional domain"},
    "PM2":  {"weight": 4, "desc": "Absent or extremely low frequency in population databases"},
    "PM3":  {"weight": 3, "desc": "Detected in trans with pathogenic variant (AR disease)"},
    "PM4":  {"weight": 3, "desc": "Protein length change (in-frame del/ins, stop codon extension)"},
    "PM5":  {"weight": 3, "desc": "Novel missense at same position as known pathogenic missense"},
    "PM6":  {"weight": 3, "desc": "Assumed de novo (no paternity/maternity confirmed)"},
    "PP1":  {"weight": 2, "desc": "Co-segregation with disease in multiple affected family members"},
    "PP2":  {"weight": 2, "desc": "Missense in gene with low benign missense rate"},
    "PP3":  {"weight": 2, "desc": "Multiple in silico predictions of damaging effect"},
    "PP4":  {"weight": 2, "desc": "Phenotype highly specific for gene's disease"},
    "PP5":  {"weight": 2, "desc": "Reputable source recently reports as pathogenic"},
    "BA1":  {"weight": -8,"desc": "Allele frequency >5% in population databases"},
    "BS1":  {"weight": -4,"desc": "Allele frequency greater than expected for disorder"},
    "BS2":  {"weight": -3,"desc": "Observed in healthy adult (dominant/XL / homozygous recessive)"},
    "BS3":  {"weight": -4,"desc": "Functional studies show no damaging effect"},
    "BS4":  {"weight": -2,"desc": "Non-segregation with disease in family"},
    "BP1":  {"weight": -1,"desc": "Missense in gene where only truncating cause disease"},
    "BP2":  {"weight": -2,"desc": "Observed in trans with pathogenic variant in dominant gene"},
    "BP3":  {"weight": -1,"desc": "In-frame del/ins in repetitive region without known function"},
    "BP4":  {"weight": -2,"desc": "Multiple in silico predictions suggest benign effect"},
    "BP5":  {"weight": -1,"desc": "Variant found in case with alternate molecular basis"},
    "BP6":  {"weight": -2,"desc": "Reputable source reports as benign"},
    "BP7":  {"weight": -1,"desc": "Silent variant with no predicted splice impact"},
}


def _apply_acmg_rules(variant_type: str, allele_freq: float,
                      cadd_score: float, gene: str,
                      inheritance: str, compound_het: bool) -> dict:
    """
    Apply ACMG 2015 rules and return triggered criteria + classification.
    Returns: { criteria_met: [...], score: int, classification: str }
    """
    criteria = []
    score = 0

    variant_type = variant_type.lower().replace(" ", "_")

    # Pathogenic criteria
    if variant_type in ["nonsense", "frameshift", "splice_site", "stop_gained"]:
        criteria.append("PVS1")
        score += ACMG_CRITERIA["PVS1"]["weight"]

    if allele_freq == 0 or allele_freq < 0.000001:
        criteria.append("PM2")
        score += ACMG_CRITERIA["PM2"]["weight"]
    elif allele_freq < 0.0001:
        criteria.append("PP3")
        score += ACMG_CRITERIA["PP3"]["weight"]

    if cadd_score >= 30:
        criteria.append("PS3")
        score += ACMG_CRITERIA["PS3"]["weight"]
    elif cadd_score >= 20:
        criteria.append("PP3")
        score += max(ACMG_CRITERIA["PP3"]["weight"], 0)

    if variant_type == "missense" and gene in RARE_DISEASE_DB:
        db = RARE_DISEASE_DB[gene]
        if "low_benign_rate" in db.get("flags", []):
            criteria.append("PP2")
            score += ACMG_CRITERIA["PP2"]["weight"]

    if compound_het and inheritance == "Autosomal Recessive":
        criteria.append("PM3")
        score += ACMG_CRITERIA["PM3"]["weight"]

    if gene in RARE_DISEASE_DB:
        criteria.append("PP4")
        score += ACMG_CRITERIA["PP4"]["weight"]

    # Benign criteria
    if allele_freq > 0.05:
        criteria.append("BA1")
        score += ACMG_CRITERIA["BA1"]["weight"]
    elif allele_freq > 0.01:
        criteria.append("BS1")
        score += ACMG_CRITERIA["BS1"]["weight"]

    if variant_type == "synonymous":
        criteria.append("BP7")
        score += ACMG_CRITERIA["BP7"]["weight"]

    if cadd_score < 10:
        criteria.append("BP4")
        score += ACMG_CRITERIA["BP4"]["weight"]

    # Classification
    if score >= 10:
        classification = "Pathogenic"
    elif score >= 6:
        classification = "Likely Pathogenic"
    elif score <= -6:
        classification = "Benign"
    elif score <= -2:
        classification = "Likely Benign"
    else:
        classification = "VUS"

    return {
        "criteria_met": criteria,
        "score": score,
        "classification": classification
    }


def _confidence_from_score(score: int, classification: str) -> int:
    """Convert ACMG score to a 0–100 confidence percentage for display."""
    if classification == "Pathogenic":
        return min(95, 70 + score * 2)
    elif classification == "Likely Pathogenic":
        return min(80, 50 + score * 3)
    elif classification == "VUS":
        return max(20, 35 + score * 3)
    elif classification == "Likely Benign":
        return max(10, 30 + abs(score) * 2)
    else:  # Benign
        return max(5, 20 + abs(score) * 2)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN PREDICTION FUNCTION
# ══════════════════════════════════════════════════════════════════════════════

def predict_rare_disease(
    gene: str,
    variant_notation: str,
    variant_type: str,
    allele_freq: float,
    cadd_score: float,
    compound_het: bool = False,
    additional_genes: list = None
) -> dict:
    """
    Main function called by Flask /api/rare route.

    Parameters
    ----------
    gene             : str   — Gene symbol e.g. "NF1"
    variant_notation : str   — HGVS notation e.g. "p.Arg1947*"
    variant_type     : str   — "missense"|"nonsense"|"frameshift"|"splice_site"|"deletion"|etc.
    allele_freq      : float — gnomAD allele frequency (0.0 = absent)
    cadd_score       : float — CADD Phred score (higher = more deleterious)
    compound_het     : bool  — True if compound heterozygous second variant present
    additional_genes : list  — Additional genes from multi-gene panel

    Returns
    -------
    dict with status, top_disease, all_candidates, acmg, confidence, etc.
    """
    if not gene:
        return {"status": "error", "message": "Gene symbol is required."}

    gene = gene.strip().upper()
    all_genes = [gene] + [g.strip().upper() for g in (additional_genes or [])]

    candidates = []

    for g in all_genes:
        if g not in RARE_DISEASE_DB:
            continue

        db = RARE_DISEASE_DB[g]
        inheritance = db.get("inheritance", "Unknown")

        # ACMG classification
        acmg = _apply_acmg_rules(
            variant_type, allele_freq, cadd_score, g,
            inheritance, compound_het
        )

        confidence = _confidence_from_score(acmg["score"], acmg["classification"])

        # Reduce confidence if variant type is not typical for this gene
        if variant_type.lower() in db.get("vus_patterns", []):
            confidence = max(confidence - 15, 10)
            if acmg["classification"] == "Pathogenic":
                acmg["classification"] = "Likely Pathogenic"

        # Boost if variant in known variant list
        if variant_notation and any(
            v.lower() in variant_notation.lower() for v in db.get("known_variants", [])
        ):
            confidence = min(confidence + 20, 97)

        candidates.append({
            "gene": g,
            "disease": db["disease"],
            "omim": db["omim"],
            "orpha": db["orpha"],
            "inheritance": inheritance,
            "prevalence": db["prevalence"],
            "chromosome": db["chromosome"],
            "severity": db["severity"],
            "onset": db["onset"],
            "icd10": db["icd10"],
            "category": db["category"],
            "acmg_classification": acmg["classification"],
            "acmg_criteria": acmg["criteria_met"],
            "acmg_score": acmg["score"],
            "confidence": confidence,
            "symptoms": db["symptoms"],
            "management": db["management"],
            "clinvar_significance": db["clinvar_significance"],
            "research_refs": db["research_refs"],
        })

    # If gene not found, do partial name match
    if not candidates:
        for db_gene, db in RARE_DISEASE_DB.items():
            if gene.lower() in db["disease"].lower() or gene.lower() in db_gene.lower():
                candidates.append({
                    "gene": db_gene,
                    "disease": db["disease"],
                    "omim": db["omim"],
                    "orpha": db["orpha"],
                    "inheritance": db.get("inheritance", ""),
                    "prevalence": db["prevalence"],
                    "chromosome": db["chromosome"],
                    "severity": db["severity"],
                    "onset": db["onset"],
                    "icd10": db["icd10"],
                    "category": db["category"],
                    "acmg_classification": "VUS",
                    "acmg_criteria": ["PP4"],
                    "acmg_score": 2,
                    "confidence": 30,
                    "symptoms": db["symptoms"],
                    "management": db["management"],
                    "clinvar_significance": db["clinvar_significance"],
                    "research_refs": db["research_refs"],
                })

    if not candidates:
        return {
            "status": "not_found",
            "message": (
                f"Gene '{gene}' not found in the rare disease database. "
                "Supported genes: " + ", ".join(RARE_DISEASE_DB.keys())
            ),
            "supported_genes": list(RARE_DISEASE_DB.keys())
        }

    # Sort by confidence descending
    candidates.sort(key=lambda x: x["confidence"], reverse=True)
    top = candidates[0]

    return {
        "status": "success",
        "gene": gene,
        "variant": variant_notation or "Not specified",
        "variant_type": variant_type,
        "allele_freq": allele_freq,
        "cadd_score": cadd_score,
        "top_disease": top["disease"],
        "top_confidence": top["confidence"],
        "top_severity": top["severity"],
        "top_acmg": top["acmg_classification"],
        "top_criteria": top["acmg_criteria"],
        "candidates": candidates[:5],      # top 5 matches
        "total_checked": len(all_genes),
        "db_size": len(RARE_DISEASE_DB)
    }


def get_all_genes() -> list:
    """Return all supported gene symbols."""
    return sorted(RARE_DISEASE_DB.keys())


def get_disease_categories() -> list:
    """Return unique disease categories."""
    cats = list({v["category"] for v in RARE_DISEASE_DB.values()})
    return sorted(cats)


def get_gene_info(gene: str) -> dict:
    """Return full info for a single gene (for quick lookup)."""
    gene = gene.strip().upper()
    if gene in RARE_DISEASE_DB:
        return {"status": "found", "gene": gene, **RARE_DISEASE_DB[gene]}
    return {"status": "not_found", "gene": gene}
