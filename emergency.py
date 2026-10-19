"""emergency.py - Emergency keyword detection with multi-language support."""
import re

# ─── Emergency Keywords by Category ───
EMERGENCY_KEYWORDS = {
    "cardiac": {
        "en": ["chest pain", "heart attack", "cardiac arrest"],
        "roman_urdu": ["seene mein dard", "seene me dard", "dil ka daura"],
        "urdu": ["سینے میں درد", "دل کا دورہ"],
        "pashto": ["د سینې درد", "د زړه دورې"],
    },
    "respiratory": {
        "en": ["cannot breathe", "can't breathe", "cant breathe", "not breathing",
               "choking", "suffocating"],
        "roman_urdu": ["saans nahi", "saans nahi aa rahi", "dum ghut raha"],
        "urdu": ["سانس نہیں", "سانس نہیں آ رہی", "دم گھٹ رہا"],
        "pashto": ["ساه نشم", "ساه نه راځي"],
    },
    "neurological": {
        "en": ["unconscious", "seizure", "stroke", "paralys", "fainted", "not responding"],
        "roman_urdu": ["behosh", "daura", "falij", "hosh nahi"],
        "urdu": ["بے ہوش", "دورہ", "فالج", "ہوش نہیں"],
        "pashto": ["بې هوښه", "دوره", "فالج"],
    },
    "bleeding": {
        "en": ["severe bleeding", "heavy bleeding", "coughing blood", "vomiting blood",
               "blood won't stop"],
        "roman_urdu": ["shadeed khoon", "khoon band nahi", "khoon ki ultian"],
        "urdu": ["شدید خون", "خون بند نہیں", "خون کی الٹیاں"],
        "pashto": ["ډیر وینه", "وینه نه دریږي"],
    },
    "poisoning": {
        "en": ["overdose", "poison", "swallowed chemicals", "drank bleach"],
        "roman_urdu": ["zeher", "zeher kha liya"],
        "urdu": ["زہر", "زہر کھا لیا"],
        "pashto": ["زهر", "زهر یې خوړلی"],
    },
    "mental_health": {
        "en": ["suicide", "want to die", "kill myself", "self harm"],
        "roman_urdu": ["khudkushi", "marna chahta", "marna chahti"],
        "urdu": ["خودکشی", "مرنا چاہتا", "مرنا چاہتی"],
        "pashto": ["ځان وژنه"],
    },
}

EMERGENCY_REPLY = {
    "English": "🚨 EMERGENCY! Call Rescue 1122 or go to the nearest hospital now. Do not wait.",
    "اردو (Urdu)": "🚨 ہنگامی صورتحال! فوراً 1122 پر کال کریں یا قریبی ہسپتال جائیں۔",
    "Roman Urdu": "🚨 EMERGENCY! Foran 1122 par call karein ya qareebi hospital jaein.",
    "پښتو (Pashto)": "🚨 بېړنی حالت! همدا اوس ۱۱۲۲ ته زنګ ووهئ یا نږدې روغتون ته ورشئ.",
}


def _flatten_keywords():
    """Flatten all emergency keywords into a single list."""
    keywords = []
    for category in EMERGENCY_KEYWORDS.values():
        for lang_keywords in category.values():
            keywords.extend(lang_keywords)
    return keywords


_ALL_KEYWORDS = _flatten_keywords()


def is_emergency(text: str) -> bool:
    """Check if text contains any emergency keywords."""
    t = text.lower()
    return any(w in t for w in _ALL_KEYWORDS)


def get_emergency_category(text: str) -> str | None:
    """Return the emergency category if detected, else None."""
    t = text.lower()
    for category, langs in EMERGENCY_KEYWORDS.items():
        for lang_keywords in langs.values():
            if any(w in t for w in lang_keywords):
                return category
    return None


def get_emergency_response(lang: str) -> str:
    """Get localized emergency response message."""
    msg = EMERGENCY_REPLY.get(lang, EMERGENCY_REPLY["English"])
    if lang != "English":
        msg += "\n\n" + EMERGENCY_REPLY["English"]
    return "**" + msg + "**"