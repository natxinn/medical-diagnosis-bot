# cases.py - Your medical cases
MEDICAL_CASES = {
    "cholecystitis": {
        "diagnosis": "CHOLECYSTITIS",
        "case_text": """
👩 CASE: A 40-year-old female presents with constant, severe upper right belly pain that started a few hours after a heavy meal. The pain shoots through to her right upper back.

📊 VITALS: T 38.5°C, HR 105

🔍 PHYSICAL EXAM: Patient winces and holds her breath when the doctor presses deeply under the right rib cage.

💉 LABS:
• WBC: 13.2 x10⁹/L (Ref: 4.0-11.0)
• AST: 68 U/L (Ref: 10-40)
• ALT: 72 U/L (Ref: 7-55)
        """
    },
    "diverticulitis": {
        "diagnosis": "DIVERTICULITIS", 
        "case_text": """
👨 CASE: A 65-year-old male presents with constant pain in the lower left part of his belly for 2 days, along with fever.

📊 VITALS: T 38.1°C, HR 100

🔍 PHYSICAL EXAM: The lower left abdomen is firm and painful to touch.

💉 LABS:
• WBC: 14.5 x10⁹/L (Ref: 4.0-11.0)
• CRP: 48 mg/L (Ref: < 5.0)
        """
    },
    "pulmonary_embolism": {
        "diagnosis": "PULMONARY EMBOLISM",
        "case_text": """
👩 CASE: A 52-year-old female, who had knee surgery two weeks ago, presents with sudden shortness of breath and sharp chest pain that gets worse when she takes a deep breath.

📊 VITALS: T 37.8°C, HR 125, RR 26, SpO2 92%

🔍 PHYSICAL EXAM: Breathing rapidly. Lungs sound clear.

💉 LABS:
• d-dimer: 1.8 mg/L FEU (Ref: < 0.5)
• pO₂ (on ABG): 72 mmHg (Ref: 80-100)
        """
    },
    "pyelonephritis": {
        "diagnosis": "PYELONEPHRITIS",
        "case_text": """
👩 CASE: 32yo F presents with 2 days of fever, chills, and left-sided flank pain. She reports increased urinary frequency and burning.

📊 VITALS: T 39.2°C, HR 110

🔍 PHYSICAL EXAM: Marked tenderness when the doctor taps firmly over her left lower back.

💉 LABS:
• WBC: 14.8 x10⁹/L (Ref: 4.0-11.0)
• Urine WBC: >100 /HPF (Ref: 0-5)
• Urine Nitrite: Positive (Ref: Negative)
        """
    }
}
