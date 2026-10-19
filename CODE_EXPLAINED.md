carebridge/
├── app.py            ← The FACE: Professional UI with voice input
├── config.py         ← Centralized settings & constants
├── core.py           ← Triage orchestrator (pipeline coordinator)
├── ai_engine.py      ← AI-powered symptom analysis (Gemini)
├── emergency.py      ← Emergency keyword detection (multi-language)
├── symptom_db.py     ← Comprehensive symptom database (12 areas)
├── logger.py         ← CSV logging & n8n webhook automation
├── voice.py          ← Voice input component (Web Speech API)
├── xray.py           ← Chest X-ray CNN model (ResNet18)
├── train_xray.py     ← X-ray model training script (Colab)
└── .streamlit/
    └── config.toml   ← Streamlit theme & server config