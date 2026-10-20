"""CareBridge: Streamlit entry point. Run:  streamlit run app.py   (all logic lives in the cb/ and ui/ packages)"""
import os
import streamlit as st

st.set_page_config(page_title="CareBridge - Health Guidance", page_icon="🩺", layout="centered", initial_sidebar_state="expanded")

# API key: environment variable, or Streamlit Cloud secret. The app still works without it (safety rules only).
if not os.environ.get("GEMINI_API_KEY"):
    try:
        os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

from cb import ai                                        # noqa: E402  (import after the key is available)
from cb.knowledge.symptoms import SYMPTOMS               # noqa: E402
from ui import components as C, sidebar, styles          # noqa: E402
from ui.pages import symptom_check, xray_tab, clinic_desk  # noqa: E402

st.markdown("<style>" + styles.CSS + "</style>", unsafe_allow_html=True)
lang = sidebar.render()
st.markdown("<style>" + styles.rtl_css(lang) + "</style>", unsafe_allow_html=True)

C.hero()
C.status_strip(ai.available(), bool(st.session_state.get("memory")), len(SYMPTOMS))

tab1, tab2, tab3 = st.tabs(["Symptom check", "Chest X-ray", "Clinic desk"])
with tab1:
    symptom_check.render(lang)
with tab2:
    xray_tab.render()
with tab3:
    clinic_desk.render()

st.markdown('<div class="foot">CareBridge gives general guidance only and is not a diagnosis. In an emergency, call 1122.</div>', unsafe_allow_html=True)
