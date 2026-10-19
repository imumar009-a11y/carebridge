"""core.py v3 - Modular triage engine for CareBridge.

Orchestrates emergency detection, AI triage, safety floors, and logging.
"""
from config import LEVELS, LANGS
from emergency import is_emergency, get_emergency_response
from ai_engine import triage_with_ai
from symptom_db import needs_extra_care, get_detected_symptoms_summary
from logger import log_triage, book_appointment, notify

# Re-export for backward compatibility
__all__ = ["triage", "book_appointment", "LANGS", "LEVELS"]


def triage(text: str, lang: str = "English", history: list | None = None, log: bool = True) -> dict:
    """Main triage pipeline: guard → AI → safety floor → logging.
    
    Pipeline:
    1. Emergency keyword detection (instant, no AI needed)
    2. AI-powered symptom analysis with symptom DB context
    3. Safety floor (vulnerable groups never get 'Home care')
    4. Logging (only urgency stored, never patient text)
    
    Args:
        text: Patient's symptom description
        lang: Language key from LANGS
        history: Previous messages from the same session
        log: Whether to log this triage event
    
    Returns:
        dict with keys: urgency, source, text
    """
    # LAYER 1: Emergency keyword guard (fast, deterministic)
    if is_emergency(text):
        msg = get_emergency_response(lang)
        result = {"urgency": "Emergency", "source": "rule", "text": msg}
    else:
        # LAYER 2 + 3: AI triage with built-in safety floor
        result = triage_with_ai(text, lang, history)

    # LAYER 4: Log (privacy-safe: only urgency, never patient words)
    if log:
        log_triage(result["urgency"], result["source"], lang)

    return result