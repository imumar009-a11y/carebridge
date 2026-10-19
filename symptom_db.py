"""symptom_db.py - Comprehensive symptom database with condition-specific triage rules.

This module contains structured knowledge about symptoms, their associated conditions,
and evidence-based triage rules that work alongside the AI for better accuracy.
"""
import re

# ─── Symptom Patterns ───
# Each pattern maps symptom keywords to conditions with triage context
SYMPTOM_PATTERNS = {
    "fever": {
        "keywords": ["fever", "bukhar", "بخار", "تبه", "temperature", "hot body"],
        "followup_questions": [
            "How many days have you had the fever?",
            "What is your temperature if measured?",
            "Do you have any other symptoms like cough, rash, or body pain?",
        ],
        "conditions": {
            "common_cold": {"additional": ["runny nose", "sneezing", "sore throat"], "default_urgency": "Home care"},
            "flu": {"additional": ["body ache", "fatigue", "chills"], "default_urgency": "Home care"},
            "dengue": {"additional": ["body ache", "rash", "pain behind eyes", "low platelets"], "default_urgency": "Urgent"},
            "typhoid": {"additional": ["stomach pain", "weakness", "prolonged fever"], "default_urgency": "See a doctor soon"},
            "malaria": {"additional": ["chills", "sweating", "shivering"], "default_urgency": "See a doctor soon"},
            "covid": {"additional": ["cough", "loss of taste", "loss of smell", "breathless"], "default_urgency": "See a doctor soon"},
            "uti": {"additional": ["burning urination", "frequent urination"], "default_urgency": "See a doctor soon"},
        },
        "escalation_rules": [
            {"condition": "duration >= 3 days", "min_urgency": "See a doctor soon"},
            {"condition": "temperature >= 103F / 39.4C", "min_urgency": "Urgent"},
            {"condition": "child under 5", "min_urgency": "See a doctor soon"},
            {"condition": "pregnant", "min_urgency": "Urgent"},
        ],
    },
    "headache": {
        "keywords": ["headache", "head pain", "sar dard", "سر درد", "د سر درد", "migraine"],
        "followup_questions": [
            "Where exactly is the pain? (front, back, one side)",
            "How severe is it on a scale of 1-10?",
            "Is it accompanied by nausea, vision changes, or neck stiffness?",
        ],
        "conditions": {
            "tension_headache": {"additional": ["stress", "tight", "band around head"], "default_urgency": "Home care"},
            "migraine": {"additional": ["one side", "nausea", "light sensitivity", "aura"], "default_urgency": "See a doctor soon"},
            "sinusitis": {"additional": ["blocked nose", "face pain", "pressure"], "default_urgency": "See a doctor soon"},
            "meningitis": {"additional": ["stiff neck", "high fever", "rash", "confusion"], "default_urgency": "Emergency"},
            "hypertension": {"additional": ["dizziness", "blurred vision", "high bp"], "default_urgency": "Urgent"},
        },
        "escalation_rules": [
            {"condition": "sudden severe onset (thunderclap)", "min_urgency": "Emergency"},
            {"condition": "with neck stiffness and fever", "min_urgency": "Emergency"},
            {"condition": "with vision changes", "min_urgency": "Urgent"},
            {"condition": "worst headache of life", "min_urgency": "Emergency"},
        ],
    },
    "cough": {
        "keywords": ["cough", "khansi", "کھانسی", "ټوخی", "coughing"],
        "followup_questions": [
            "Is it a dry cough or with phlegm?",
            "How long have you had it?",
            "Is there any blood in the phlegm?",
        ],
        "conditions": {
            "common_cold": {"additional": ["runny nose", "sneezing"], "default_urgency": "Home care"},
            "bronchitis": {"additional": ["phlegm", "chest congestion", "wheezing"], "default_urgency": "See a doctor soon"},
            "pneumonia": {"additional": ["high fever", "chest pain", "breathless", "fast breathing"], "default_urgency": "Urgent"},
            "asthma": {"additional": ["wheezing", "breathless", "chest tight", "night cough"], "default_urgency": "See a doctor soon"},
            "tuberculosis": {"additional": ["weight loss", "night sweats", "prolonged cough", "blood in sputum"], "default_urgency": "See a doctor soon"},
        },
        "escalation_rules": [
            {"condition": "blood in cough/sputum", "min_urgency": "Emergency"},
            {"condition": "cough > 2 weeks", "min_urgency": "See a doctor soon"},
            {"condition": "with breathing difficulty", "min_urgency": "Urgent"},
        ],
    },
    "stomach": {
        "keywords": ["stomach pain", "abdominal pain", "pet dard", "پیٹ درد", "د ګېډې درد",
                     "stomach ache", "belly pain", "tummy pain"],
        "followup_questions": [
            "Where is the pain? (upper, lower, left, right side)",
            "Is it constant or comes and goes?",
            "Do you have nausea, vomiting, or diarrhea?",
        ],
        "conditions": {
            "gastritis": {"additional": ["acidity", "burning", "after eating"], "default_urgency": "Home care"},
            "food_poisoning": {"additional": ["vomiting", "diarrhea", "ate something bad"], "default_urgency": "See a doctor soon"},
            "appendicitis": {"additional": ["right lower pain", "sharp pain", "nausea"], "default_urgency": "Urgent"},
            "kidney_stones": {"additional": ["side pain", "severe pain", "blood in urine", "back pain"], "default_urgency": "Urgent"},
            "ulcer": {"additional": ["burning", "empty stomach pain", "black stool"], "default_urgency": "See a doctor soon"},
        },
        "escalation_rules": [
            {"condition": "severe sudden pain", "min_urgency": "Urgent"},
            {"condition": "blood in stool", "min_urgency": "Urgent"},
            {"condition": "with high fever", "min_urgency": "Urgent"},
            {"condition": "pregnant with abdominal pain", "min_urgency": "Emergency"},
        ],
    },
    "skin": {
        "keywords": ["rash", "itching", "khujli", "کھجلی", "خارښت", "spots", "bumps",
                     "skin", "boil", "wound", "zakhm", "زخم"],
        "followup_questions": [
            "Where is the rash or skin issue?",
            "Is it spreading?",
            "Do you have fever along with it?",
        ],
        "conditions": {
            "allergic_reaction": {"additional": ["hives", "swelling", "after eating"], "default_urgency": "See a doctor soon"},
            "eczema": {"additional": ["dry patches", "itchy", "recurring"], "default_urgency": "Home care"},
            "fungal_infection": {"additional": ["ring shaped", "moist area", "itchy"], "default_urgency": "See a doctor soon"},
            "cellulitis": {"additional": ["red", "warm", "swollen", "spreading", "fever"], "default_urgency": "Urgent"},
            "dengue_rash": {"additional": ["red spots", "fever", "body ache"], "default_urgency": "Urgent"},
        },
        "escalation_rules": [
            {"condition": "rash with fever and body pain", "min_urgency": "Urgent"},
            {"condition": "rapid swelling of face/lips/throat", "min_urgency": "Emergency"},
            {"condition": "spreading red streak from wound", "min_urgency": "Urgent"},
        ],
    },
    "breathing": {
        "keywords": ["breathless", "short of breath", "breathing difficulty", "saans",
                     "سانس", "ساه", "wheezing", "gasping"],
        "followup_questions": [
            "Did it start suddenly or gradually?",
            "Does it happen at rest or only during activity?",
            "Do you have any chest pain or cough?",
        ],
        "conditions": {
            "anxiety": {"additional": ["panic", "fast heartbeat", "tingling", "stress"], "default_urgency": "See a doctor soon"},
            "asthma": {"additional": ["wheezing", "cough", "night symptoms", "allergy"], "default_urgency": "See a doctor soon"},
            "pneumonia": {"additional": ["fever", "cough", "chest pain"], "default_urgency": "Urgent"},
            "heart_failure": {"additional": ["swollen legs", "lying down worse", "fatigue"], "default_urgency": "Urgent"},
            "pulmonary_embolism": {"additional": ["sudden onset", "chest pain", "leg swelling"], "default_urgency": "Emergency"},
        },
        "escalation_rules": [
            {"condition": "sudden onset", "min_urgency": "Emergency"},
            {"condition": "with chest pain", "min_urgency": "Emergency"},
            {"condition": "blue lips/fingers", "min_urgency": "Emergency"},
        ],
    },
    "mental_health": {
        "keywords": ["anxiety", "depression", "sad", "worried", "can't sleep", "panic",
                     "stress", "udaas", "اداس", "پریشان", "نیند نہیں", "tension"],
        "followup_questions": [
            "How long have you been feeling this way?",
            "Is it affecting your daily activities?",
            "Do you have any thoughts of harming yourself?",
        ],
        "conditions": {
            "mild_anxiety": {"additional": ["occasional worry", "exam stress", "work stress"], "default_urgency": "Home care"},
            "generalized_anxiety": {"additional": ["constant worry", "restless", "can't focus"], "default_urgency": "See a doctor soon"},
            "depression": {"additional": ["hopeless", "no interest", "fatigue", "worthless"], "default_urgency": "See a doctor soon"},
            "panic_disorder": {"additional": ["panic attack", "heart racing", "fear of dying"], "default_urgency": "See a doctor soon"},
        },
        "escalation_rules": [
            {"condition": "self-harm thoughts", "min_urgency": "Emergency"},
            {"condition": "inability to function daily", "min_urgency": "Urgent"},
        ],
    },
    "eye": {
        "keywords": ["eye pain", "vision", "blurry", "ankh", "آنکھ", "سترګه",
                     "can't see", "red eye", "watery eyes"],
        "followup_questions": [
            "Is one eye or both affected?",
            "Did you have any injury?",
            "Is there any discharge or swelling?",
        ],
        "conditions": {
            "conjunctivitis": {"additional": ["red", "discharge", "itchy", "pink eye"], "default_urgency": "See a doctor soon"},
            "eye_strain": {"additional": ["screen time", "tired eyes", "headache"], "default_urgency": "Home care"},
            "glaucoma": {"additional": ["severe pain", "vision loss", "halos"], "default_urgency": "Emergency"},
            "eye_injury": {"additional": ["hit", "chemical", "foreign body"], "default_urgency": "Urgent"},
        },
        "escalation_rules": [
            {"condition": "sudden vision loss", "min_urgency": "Emergency"},
            {"condition": "chemical exposure", "min_urgency": "Emergency"},
        ],
    },
    "joint_pain": {
        "keywords": ["joint pain", "knee pain", "back pain", "joron ka dard", "جوڑوں کا درد",
                     "د بندونو درد", "body ache", "muscle pain"],
        "followup_questions": [
            "Which joint is affected?",
            "Is there any swelling or redness?",
            "Did you have any injury or fall?",
        ],
        "conditions": {
            "muscle_strain": {"additional": ["overexertion", "sports", "lifting"], "default_urgency": "Home care"},
            "arthritis": {"additional": ["stiffness", "morning", "multiple joints"], "default_urgency": "See a doctor soon"},
            "gout": {"additional": ["big toe", "sudden", "red", "swollen"], "default_urgency": "See a doctor soon"},
            "fracture": {"additional": ["fall", "unable to move", "deformed", "swollen"], "default_urgency": "Urgent"},
        },
        "escalation_rules": [
            {"condition": "unable to bear weight", "min_urgency": "Urgent"},
            {"condition": "deformity visible", "min_urgency": "Emergency"},
            {"condition": "with fever and joint swelling", "min_urgency": "Urgent"},
        ],
    },
    "urinary": {
        "keywords": ["urine", "peshab", "پیشاب", "ادرار", "burning urination",
                     "blood in urine", "frequent urination"],
        "followup_questions": [
            "Is there pain or burning when passing urine?",
            "How often are you going?",
            "Is there any blood in your urine?",
        ],
        "conditions": {
            "uti": {"additional": ["burning", "frequent", "urgency"], "default_urgency": "See a doctor soon"},
            "kidney_stone": {"additional": ["severe pain", "back pain", "blood"], "default_urgency": "Urgent"},
            "kidney_infection": {"additional": ["fever", "back pain", "chills"], "default_urgency": "Urgent"},
        },
        "escalation_rules": [
            {"condition": "blood in urine", "min_urgency": "Urgent"},
            {"condition": "with high fever and back pain", "min_urgency": "Urgent"},
            {"condition": "unable to urinate at all", "min_urgency": "Emergency"},
        ],
    },
    "diarrhea": {
        "keywords": ["diarrhea", "loose motions", "dast", "دست", "اسهال",
                     "watery stool", "upset stomach"],
        "followup_questions": [
            "How many times in the last 24 hours?",
            "Is there any blood in the stool?",
            "Are you able to keep fluids down?",
        ],
        "conditions": {
            "viral_gastro": {"additional": ["vomiting", "cramps", "short duration"], "default_urgency": "Home care"},
            "food_poisoning": {"additional": ["after eating", "nausea", "cramps"], "default_urgency": "See a doctor soon"},
            "cholera": {"additional": ["watery", "severe", "dehydration"], "default_urgency": "Urgent"},
            "dysentery": {"additional": ["blood", "mucus", "fever"], "default_urgency": "Urgent"},
        },
        "escalation_rules": [
            {"condition": "blood in stool", "min_urgency": "Urgent"},
            {"condition": "signs of dehydration (dry mouth, dizziness)", "min_urgency": "Urgent"},
            {"condition": "child under 5 with diarrhea", "min_urgency": "Urgent"},
        ],
    },
    "pregnancy": {
        "keywords": ["pregnant", "pregnancy", "hamal", "حاملہ", "امیدوار", "حمل",
                     "expecting", "baby coming"],
        "followup_questions": [
            "How many months/weeks pregnant are you?",
            "What symptoms are you experiencing?",
            "Is this your first pregnancy?",
        ],
        "conditions": {
            "morning_sickness": {"additional": ["nausea", "vomiting", "first trimester"], "default_urgency": "See a doctor soon"},
            "preeclampsia": {"additional": ["headache", "blurry vision", "swelling", "high bp"], "default_urgency": "Emergency"},
            "bleeding": {"additional": ["spotting", "bleeding", "cramps"], "default_urgency": "Emergency"},
            "labor": {"additional": ["contractions", "water broke", "regular pain"], "default_urgency": "Urgent"},
        },
        "escalation_rules": [
            {"condition": "any bleeding", "min_urgency": "Emergency"},
            {"condition": "severe headache with blurry vision", "min_urgency": "Emergency"},
            {"condition": "reduced baby movement", "min_urgency": "Urgent"},
            {"condition": "all pregnancy symptoms", "min_urgency": "See a doctor soon"},
        ],
    },
}


def detect_symptoms(text: str) -> list[dict]:
    """Detect symptoms from free text and return matching patterns with context."""
    t = text.lower()
    matches = []
    for symptom_name, data in SYMPTOM_PATTERNS.items():
        for kw in data["keywords"]:
            if kw in t:
                matches.append({
                    "symptom": symptom_name,
                    "conditions": data["conditions"],
                    "followup_questions": data["followup_questions"],
                    "escalation_rules": data["escalation_rules"],
                })
                break
    return matches


def build_symptom_context(text: str) -> str:
    """Build a symptom context string to enhance AI prompt accuracy."""
    matches = detect_symptoms(text)
    if not matches:
        return ""

    context_parts = ["\n--- SYMPTOM ANALYSIS CONTEXT ---"]
    for m in matches:
        context_parts.append(f"\nDetected symptom area: {m['symptom'].upper()}")
        context_parts.append("Possible conditions to consider:")
        for cond_name, cond_data in m["conditions"].items():
            additional = ", ".join(cond_data["additional"])
            context_parts.append(
                f"  - {cond_name.replace('_', ' ').title()}: "
                f"look for [{additional}], default urgency = {cond_data['default_urgency']}"
            )
        context_parts.append("Escalation rules:")
        for rule in m["escalation_rules"]:
            context_parts.append(f"  ⚠ If {rule['condition']} → minimum urgency = {rule['min_urgency']}")

    context_parts.append("--- END SYMPTOM CONTEXT ---")
    return "\n".join(context_parts)


def needs_extra_care(text: str) -> bool:
    """Check if patient belongs to a vulnerable group: child <5, pregnant, age 65+."""
    t = text.lower()
    return bool(
        "pregnan" in t or "حاملہ" in t or "hamal" in t
        or re.search(r"\b[0-4][- ]?(year|yr|saal|sal)s?[- ]?old\b", t)
        or re.search(r"\b(infant|baby|toddler|months? old|newborn|bacha|بچہ|ماشوم)\b", t)
        or re.search(r"\b(6[5-9]|[7-9]\d)[- ]?(year|yr|saal|sal)s?[- ]?old\b", t)
        or re.search(r"\b(elderly|old age|buzurg|بزرگ|بوډا)\b", t)
    )


def get_detected_symptoms_summary(text: str) -> list[str]:
    """Return a list of detected symptom area names."""
    return [m["symptom"] for m in detect_symptoms(text)]