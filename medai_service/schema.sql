-- ════════════════════════════════════════════════════════════
-- MedAI Database Schema
-- Run: mysql -u root -p < schema.sql
-- ════════════════════════════════════════════════════════════

CREATE DATABASE IF NOT EXISTS medai_db;
USE medai_db;

-- ── Table 1: Diseases ──────────────────────────────────────
CREATE TABLE diseases (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    severity    ENUM('low','medium','high') DEFAULT 'medium',
    category    VARCHAR(50),
    description TEXT,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ── Table 2: Symptoms ──────────────────────────────────────
CREATE TABLE symptoms (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    display     VARCHAR(100)
);

-- ── Table 3: Disease-Symptom mapping ──────────────────────
CREATE TABLE disease_symptoms (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    disease_id  INT, symptom_id INT,
    FOREIGN KEY (disease_id) REFERENCES diseases(id),
    FOREIGN KEY (symptom_id) REFERENCES symptoms(id)
);

-- ── Table 4: Medicines ─────────────────────────────────────
CREATE TABLE medicines (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    disease_id  INT,
    name        VARCHAR(150) NOT NULL,
    dosage      VARCHAR(200),
    notes       TEXT,
    type        ENUM('otc','prescription') DEFAULT 'prescription',
    FOREIGN KEY (disease_id) REFERENCES diseases(id)
);

-- ── Table 5: Precautions ───────────────────────────────────
CREATE TABLE precautions (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    disease_id  INT,
    precaution  TEXT NOT NULL,
    FOREIGN KEY (disease_id) REFERENCES diseases(id)
);

-- ── Table 6: Patient sessions (optional) ──────────────────
CREATE TABLE patient_sessions (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    session_id      VARCHAR(100),
    symptoms_input  TEXT,
    predicted_disease VARCHAR(100),
    confidence      INT,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ── Sample data ────────────────────────────────────────────
INSERT INTO diseases (name, severity, category) VALUES
('Influenza (Flu)', 'medium', 'Viral infection'),
('Common Cold',     'low',    'Viral infection'),
('Malaria',         'high',   'Parasitic infection'),
('Type 2 Diabetes', 'medium', 'Chronic disease'),
('Gastroenteritis', 'medium', 'Infection');

INSERT INTO symptoms (name, display) VALUES
('fever',             'Fever'),
('cough',             'Cough'),
('fatigue',           'Fatigue'),
('headache',          'Headache'),
('body_ache',         'Body ache'),
('chills',            'Chills'),
('runny_nose',        'Runny nose'),
('vomiting',          'Vomiting'),
('diarrhea',          'Diarrhea'),
('frequent_urination','Frequent urination');
