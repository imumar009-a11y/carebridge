# CareBridge code, explained simply
Think of a clinic: a **guard** (emergencies), a **receptionist** (what kind of message is this?), a **nurse** (who is the patient, how long, how bad?), a **rule book** (what each symptom needs), a **doctor's assistant** (Gemini, writes the advice in your language), and a **notebook** (optional memory).

## cb/ - the brain
- `knowledge/red_flags.py` - danger phrases in 4 writing styles. Checked first, answered instantly.
- `knowledge/symptoms.py` - the rule book. One block per symptom: keywords, base level, escalation `Rule`s (duration, severity, age, pregnancy, conditions, other symptoms), safe self-care and warning signs.
- `text.py` - cleans text so different keyboards match, and understands "no fever" (negation).
- `parsing.py` - finds durations ("3 din se", "for 2 weeks"), severity ("mild", "bohat tez") and numbers (BP 150/95, sugar 320, SpO2 88).
- `patient.py` - who is it for ("my father is 70"), age, pregnancy, diabetes/heart/asthma...
- `intent.py` - greeting, thanks, appointment, medicine question, general question, follow-up.
- `rules.py` - combines everything into a **safety floor** (0 Home care ... 3 Emergency) with reasons.
- `triage.py` - the pipeline. Final level = the higher of rules and AI.
- `ai.py` - Gemini for the written answer and for speech to text.
- `memory.py` - optional saved profile + history. `case.py` - remembers the current chat so "since 3 days" makes sense.
- `i18n.py` - translated headings, hints, first-aid steps.

## ui/ - the face
`app.py` only wires things together. `ui/styles.py` is all the CSS, `components.py` the urgency card / chips / Listen button, `sidebar.py` language + memory, `voice.py` record/upload + review, `pages/` the three tabs.

## xray.py / train_xray.py - the CNN
ResNet18 already trained on everyday images; only the last layer is taught NORMAL vs PNEUMONIA. We report accuracy, sensitivity and specificity.
