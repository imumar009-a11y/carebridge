"""ai_engine.py - AI-powered triage engine using Google Gemini."""
import os
import json
import time
from google import genai
from google.genai import types

from config import MODEL, LANGS, LEVELS
from symptom_db import build_symptom_context, needs_extra_care

# ─── System Prompt ───
SYSTEM_PROMPT = (
    "You are CareBridge, an advanced health guidance assistant for people in Pakistan. "
    "You are NOT a doctor. Never diagnose. Never prescribe specific medicine or doses. "
    "\n\n"
    "INSTRUCTIONS:\n"
    "1. Analyze the patient's symptoms carefully, considering all mentioned symptoms together.\n"
    "2. Consider the patient's age, gender, and any mentioned medical history.\n"
    "3. For each symptom combination, think about what conditions commonly present this way in Pakistan.\n"
    "4. Provide condition-specific guidance - do NOT give generic advice.\n"
    "5. If symptom analysis context is provided, use it to improve your assessment.\n"
    "\n"
    "Reply with ONLY a JSON object with these keys:\n"
    '  urgency: exactly one of: "Home care", "See a doctor soon", "Urgent", "Emergency"\n'
    '  possibilities: list of 2-3 general possibilities (not diagnoses), SPECIFIC to the symptoms described\n'
    '  steps: list of 3-4 safe, SPECIFIC things to do now (tailored to the symptoms, not generic advice)\n'
    '  warning_signs: list of 3-4 specific warning signs that mean they should see a doctor immediately\n'
    '  followup_question: one relevant follow-up question to better understand their condition\n'
    "\n"
    "SAFETY RULES:\n"
    "- Children under 5 with ANY symptoms: minimum 'See a doctor soon'\n"
    "- Pregnant women with ANY concerning symptoms: minimum 'Urgent'\n"
    "- People over 65 with ANY symptoms: minimum 'See a doctor soon'\n"
    "- Multiple severe symptoms together: escalate urgency\n"
    "- If unsure, ALWAYS choose the more urgent level\n"
    "- Fever > 3 days: minimum 'See a doctor soon'\n"
    "- Any bleeding during pregnancy: 'Emergency'\n"
    "\n"
    "Write all text values in LANGNAME but keep the urgency value in English. "
    "Keep every item concise but specific to the reported symptoms."
)


def ask_ai(text: str, lang: str, history: list[str] | None = None) -> dict | None:
    """Send symptoms to Gemini AI with symptom context for better accuracy."""
    # Build the prompt with history and symptom context
    prompt_parts = []

    if history:
        prompt_parts.append(
            "Earlier messages from the same person: " + " | ".join(history[-3:])
        )

    prompt_parts.append("Current message: " + text)

    # Add symptom analysis context to improve accuracy
    symptom_context = build_symptom_context(text)
    if symptom_context:
        prompt_parts.append(symptom_context)

    full_prompt = "\n".join(prompt_parts)

    # Configure the AI
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    system = SYSTEM_PROMPT.replace("LANGNAME", LANGS[lang])
    cfg = types.GenerateContentConfig(
        system_instruction=system,
        response_mime_type="application/json",
    )

    # Retry logic with exponential backoff
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=MODEL, contents=full_prompt, config=cfg
            )
            data = json.loads(response.text.strip())

            # Validate urgency level
            if data.get("urgency") not in LEVELS:
                data["urgency"] = "See a doctor soon"  # fail-safe

            return data
        except Exception:
            time.sleep(2 * (attempt + 1))

    return None


def format_reply(data: dict) -> str:
    """Format the AI response into a readable message."""
    def bullets(key: str) -> str:
        items = data.get(key, [])
        if not items:
            return "_No information available_"
        return "\n".join(f"• {item}" for item in items)

    sections = [
        "**🔍 What this could relate to**",
        bullets("possibilities"),
        "",
        "**💊 What you can do now**",
        bullets("steps"),
        "",
        "**⚠️ See a doctor immediately if**",
        bullets("warning_signs"),
    ]

    # Add follow-up question if present
    followup = data.get("followup_question")
    if followup:
        sections.extend(["", f"**❓ To help you better:** {followup}"])

    sections.extend([
        "",
        "---",
        "_🩺 Decision support only — not a diagnosis. If in doubt, see a doctor._",
    ])

    return "\n".join(sections)


def triage_with_ai(text: str, lang: str, history: list[str] | None = None) -> dict:
    """Run AI triage with safety floor checks."""
    data = ask_ai(text, lang, history or [])

    if data is None:
        return {
            "urgency": "See a doctor soon",
            "source": "fallback",
            "text": "⚠️ Service is busy. Please try again. If it feels serious, call 1122 or see a doctor.",
        }

    urgency = data["urgency"]
    note = ""

    # Safety floor: vulnerable groups never get "Home care"
    if needs_extra_care(text) and urgency == "Home care":
        urgency = "See a doctor soon"
        note = "\n\n**🛡️ Safety rule:** Because of age or pregnancy, please see a doctor soon."

    return {
        "urgency": urgency,
        "source": "ai",
        "text": format_reply(data) + note,
    }