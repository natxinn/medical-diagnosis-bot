# cases.py - Your medical cases
MEDICAL_CASES = {
    "cholecystitis": {
        "diagnosis": "CHOLECYSTITIS",
        "case_text": """
👩 CASE: A 40-year-old female presents with severe, constant right upper quadrant pain that started after a fatty meal. The pain radiates to her right scapula. She reports nausea and one episode of vomiting.

📊 VITALS: T 38.5°C, HR 105, BP 145/90

🔍 PHYSICAL EXAM: Positive Murphy's sign (arrest of inspiration on deep palpation of the RUQ)

💉 LABS:
• LFTs: AST 68 U/L, ALT 72 U/L, Alkaline Phosphatase 150 U/L (Mildly Elevated)
• CBC: WBC 13.2 x10^9/L (High)
        """
    },
    "diverticulitis": {
        "diagnosis": "DIVERTICULITIS", 
        "case_text": """
👨 CASE: A 65-year-old male with a history of constipation presents with 2 days of constant left lower quadrant pain, fever, and a change in bowel habits.

📊 VITALS: T 38.1°C, HR 100, BP 128/85

🔍 PHYSICAL EXAM: Tenderness and guarding in the left lower quadrant. No hernias.

💉 LABS:
• CBC: WBC 14.5 x10^9/L (High)
• CRP: 48 mg/L (High)
        """
    },
    "pulmonary_embolism": {
        "diagnosis": "PULMONARY EMBOLISM",
        "case_text": """
👩 CASE: A 52-year-old female, 2 weeks post-knee surgery, presents with sudden onset of sharp chest pain and shortness of breath. She describes the pain as worse when breathing in.

📊 VITALS: T 37.8°C, HR 125, BP 108/70, RR 26, SpO2 92% on RA

🔍 PHYSICAL EXAM: Tachypneic and tachycardic. Lungs clear to auscultation bilaterally.

💉 LABS:
• d-dimer: 1.8 mg/L (High) [Normal < 0.5]
• ABG: pH 7.48, pCO2 32 mmHg, pO2 72 mmHg (Respiratory Alkalosis, Hypoxia)
        """
    },
    "appendicitis": {
        "diagnosis": "APPENDICITIS",
        "case_text": """
👩 CASE: 19 y/o female with 24h of migrating periumbilical pain now localised to severe RLQ pain, associated with nausea/vomiting.

📊 VITALS: T 38.3°C, HR 116, BP 132/84, RR 18, SpO2 99% RA

🔍 PHYSICAL EXAM: Guarding & maximal tenderness at McBurney's point. Positive Rovsing's and Psoas signs.

💉 LABS:
• WBC 15.8, Neutrophils 86%, CRP 52
• Urine: Beta-hCG negative, no WBCs or bacteria
        """
    },
    "dengue_fever": {
        "diagnosis": "DENGUE FEVER",
        "case_text": """
👨 CASE: 28yo male returned from a tropical vacation 4 days ago. Presents with 3 days of high fever, severe myalgias/arthralgias, and a new rash.

📊 VITALS: T 39.1°C, HR 102, BP 118/78, RR 22

🔍 PHYSICAL EXAM: Diffuse blanching macular rash. Positive tourniquet test. Mild hepatomegaly on palpation.

💉 LABS:
• CBC: WBC 3.5 x10^9/L (Low), Platelets 92 x10^9/L (Low), Hct 45.5%
• Serology: Arbovirus PCR Panel: Positive for Flavivirus
        """
    }
}
