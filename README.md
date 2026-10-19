CareBridge
AI health guidance (English / Urdu / Roman Urdu / Pashto), a chest X-ray CNN demo and clinic automation for Pakistan. Decision support, not diagnosis.
Architecture
Rule guard (instant Rescue 1122 for danger words) -> 2. Gemini with strict JSON rules -> 3. Safety floor (children, pregnancy, 65+) -> 4. Automation (CSV log + n8n webhook) -> dashboard. X-ray: ResNet18 transfer learning (Kaggle pneumonia dataset).
Run locally (Windows)
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
$env:GEMINI_API_KEY="your_key"
streamlit run app.py
Optional: $env:N8N_WEBHOOK_URL="..." and pip install -r requirements-xray.txt.
Train the X-ray model (Google Colab, free GPU)
Upload train_xray.py and the Kaggle "Chest X-Ray Images (Pneumonia)" folder as chest_xray/, run python train_xray.py, download xray_model.pt into the project folder.
Deploy free (public link)
Push to GitHub, open share.streamlit.io, pick the repo and app.py, and add GEMINI_API_KEY under Secrets.
Evaluation
python run_tests.py -> text triage accuracy and under-triage count. Add results here.
Limitations
No clinical validation. Pashto/Urdu keywords need native-speaker and clinician review. Needs internet for Gemini. The X-ray dataset is pediatric and from one source, so results will not transfer to all hospitals.
Never commit API keys.