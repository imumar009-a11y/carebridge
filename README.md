# CareBridge
AI health guidance in English / Urdu / Roman Urdu / Pashto, with voice input, optional memory, a chest X-ray CNN demo and clinic automation for Pakistan.
**Decision support, not diagnosis.**

## What it does
1. **Emergency guard** - danger phrases (chest pain, cannot breathe, seizure, heavy bleeding, suicide, snake bite...) get an instant, rule-based answer with first-aid steps. No AI, no waiting.
2. **Intent router** - greetings, thanks, appointment requests, medicine questions (no doses are ever given) and general health questions are handled differently from symptom reports.
3. **Patient understanding** - who is sick (you or a relative), age, pregnancy, long-term conditions (diabetes, heart, asthma...), duration, severity and numbers (temperature, BP, sugar, SpO2, pulse).
4. **Symptom rule engine** - 38 symptom areas, each with its own escalation rules. Same words give different decisions for different people (a fever in a 3-year-old is not a fever in a healthy adult; 3 days is not 8 days).
5. **Gemini** adds detail in the person's language. **Final urgency = MAX(rules, AI)**: the AI can raise the level, never lower it.
6. **Voice** - record or upload a voice note (WhatsApp .ogg works); Gemini turns it into text, you check it, then send. Answers can be read aloud with the browser's voice.
7. **Memory (optional, off by default)** - saves a health profile and past checks (symptom tags + urgency, never your words). Used for better advice and to notice repeated symptoms. Download or delete anytime.
8. **Automation** - anonymous CSV log (+ optional n8n webhook) and a clinic dashboard.

## Folder map
```
app.py                  entry point (thin)
core.py                 old import path, kept for compatibility
cb/                     the brain (no web code)
  config.py  text.py  parsing.py  patient.py  intent.py  case.py
  rules.py              rule engine
  triage.py             the pipeline
  ai.py                 Gemini: answers + speech to text
  memory.py             optional memory
  i18n.py               translated fixed texts and first aid
  automation.py  xray.py
  knowledge/            DATA: red_flags.py, symptoms.py, model.py
ui/                     the face
  styles.py components.py sidebar.py voice.py
  pages/                symptom_check.py xray_tab.py clinic_desk.py
tests/test_engine.py    offline unit tests
run_tests.py            runs test_cases.csv (77 cases)
```

## Run locally (Windows PowerShell)
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
$env:GEMINI_API_KEY="your_key"
streamlit run app.py
```
Without a key the app still works with the built-in safety rules (English only, voice off).
Optional: `$env:N8N_WEBHOOK_URL="..."` and `pip install -r requirements-xray.txt`.

## Add or change a symptom (no code changes)
Open `cb/knowledge/symptoms.py`, copy an existing `Symptom(...)` block, change the keywords (any of the 4 languages), the base level and the `Rule(...)` lines. Run `python run_tests.py --offline`.

## Tests
```
python -m unittest discover -s tests -v     # offline unit tests
python run_tests.py --offline               # 77 regression cases, rules only
python run_tests.py                         # rules + Gemini (needs key)
```
These are **regression tests written by the developer, not clinical validation.**

## Deploy free
Push to GitHub, open share.streamlit.io, choose the repo and `app.py`, and add under *Secrets*: `GEMINI_API_KEY = "your_key"`.
Streamlit Cloud forgets files when it restarts, so saved memory and logs are temporary there. Use a persistent host for real use.

## Train the X-ray model (Google Colab)
Upload `train_xray.py` and the Kaggle "Chest X-Ray Images (Pneumonia)" folder as `chest_xray/`, run it, download `xray_model.pt` into the project folder.

## Limitations (read this)
- No clinical validation. A doctor must review every rule in `cb/knowledge/` before real use.
- Urdu, Roman Urdu and Pashto keywords and fixed texts need native-speaker review. First-aid steps exist in English, Urdu and Roman Urdu for the common emergencies and fall back to English otherwise (including Pashto).
- Voice transcription quality varies, especially for Pashto. The person always reviews the text before it is sent.
- Memory files are not encrypted. Do not store sensitive data on a shared public server.
- The X-ray dataset is pediatric and from one source; results will not transfer to all hospitals.

**Never commit or screenshot API keys.** If a key is exposed, delete it in Google AI Studio and make a new one.
