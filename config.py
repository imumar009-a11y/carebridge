"""config.py - Centralized configuration for CareBridge."""
import os

# ─── AI Model ───
MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
WEBHOOK = os.environ.get("N8N_WEBHOOK_URL", "")

# ─── Triage Levels ───
LEVELS = ["Home care", "See a doctor soon", "Urgent", "Emergency"]

# ─── Supported Languages ───
LANGS = {
    "English": "English",
    "اردو (Urdu)": "Urdu, written in Urdu script",
    "Roman Urdu": "Roman Urdu (Urdu written in English letters)",
    "پښتو (Pashto)": "Pashto, written in Pashto script",
}

# ─── Urgency Colors & Hints ───
COLORS = {
    "Home care": "#2E9E6B",
    "See a doctor soon": "#E0A100",
    "Urgent": "#E8731A",
    "Emergency": "#D7263D",
}

HINTS = {
    "Home care": "Self-care is likely enough. Watch for the warning signs below.",
    "See a doctor soon": "Arrange a doctor visit soon.",
    "Urgent": "See a doctor today.",
    "Emergency": "Call 1122 now or go to the nearest hospital.",
}

# ─── Sidebar Examples ───
EXAMPLES = [
    ("🤒 Fever and headache", "I have fever and headache for 2 days"),
    ("👶 Child with fever", "My 3-year-old has had a fever for 2 days"),
    ("💔 Chest pain", "chest pain"),
    ("🗣️ Roman Urdu", "mujhe bukhar aur sar dard hai"),
    ("🤧 Cold and cough", "I have running nose, sneezing and mild cough for 3 days"),
    ("🤰 Pregnancy concern", "I am 7 months pregnant and having severe headache"),
    ("🦴 Joint pain", "My knees hurt badly when I climb stairs"),
    ("😰 Anxiety symptoms", "I feel anxious, my heart races and I can't sleep"),
]