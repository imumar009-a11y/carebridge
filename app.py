"""app.py v4 - Professional CareBridge UI with voice input.
Run: streamlit run app.py
"""
import os
import pandas as pd
import streamlit as st
from PIL import Image

from config import LANGS, LEVELS, COLORS, HINTS, EXAMPLES
from core import triage, book_appointment
from symptom_db import get_detected_symptoms_summary
import xray

st.set_page_config(
    page_title="CareBridge - AI Health Guidance",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ════════════════════════════════════════════════════════════════════════
#  PROFESSIONAL CSS - Glassmorphism + Animations + Modern Design
# ════════════════════════════════════════════════════════════════════════
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Noto+Nastaliq+Urdu:wght@400;600&family=Noto+Naskh+Arabic:wght@400;600&display=swap');

/* ─── Root Variables ─── */
:root {
    --primary: #0E7C86;
    --primary-dark: #0B2F3A;
    --primary-light: #5FD3DB;
    --accent: #0E7C86;
    --bg: #F0F5F7;
    --surface: rgba(255, 255, 255, 0.85);
    --surface-solid: #FFFFFF;
    --border: rgba(211, 226, 229, 0.6);
    --text-primary: #0B2F3A;
    --text-secondary: #3F5E67;
    --text-muted: #7A9AA3;
    --success: #2E9E6B;
    --warning: #E0A100;
    --danger: #D7263D;
    --urgent: #E8731A;
    --shadow-sm: 0 2px 8px rgba(11, 47, 58, 0.06);
    --shadow-md: 0 4px 20px rgba(11, 47, 58, 0.08);
    --shadow-lg: 0 8px 40px rgba(11, 47, 58, 0.12);
    --radius-sm: 10px;
    --radius-md: 16px;
    --radius-lg: 22px;
    --radius-xl: 28px;
}

/* ─── Base ─── */
html, body, [class*="st-"], .stApp {
    font-family: 'Plus Jakarta Sans', 'Noto Naskh Arabic', system-ui, -apple-system, sans-serif;
}
#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }
.block-container {
    max-width: 900px;
    padding-top: 1rem;
    padding-bottom: 3rem;
}

/* ─── Hero Section ─── */
.hero {
    background: linear-gradient(135deg, #0B2F3A 0%, #0E5A63 50%, #0E7C86 100%);
    color: #EAF4F5;
    border-radius: var(--radius-xl);
    padding: clamp(1.5rem, 4vw, 2.5rem);
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem 2.5rem;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow-lg);
}
.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(95, 211, 219, 0.15) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -30%;
    left: -10%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(95, 211, 219, 0.1) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}
.hero .brand {
    font-size: clamp(2.2rem, 7vw, 3.5rem);
    font-weight: 800;
    letter-spacing: -0.04em;
    line-height: 1;
    color: #fff;
    position: relative;
}
.hero .brand-sub {
    display: inline-block;
    background: linear-gradient(135deg, #5FD3DB, #9FE8ED);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 0.35em;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 0.5rem;
}
.hero .tag {
    margin-top: 0.7rem;
    font-size: 1.05rem;
    color: #CFE4E7;
    max-width: 32ch;
    line-height: 1.5;
}
.hero .features {
    margin-top: 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
}
.hero .feature-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.88rem;
    color: #9FC4CA;
}
.hero .feature-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--primary-light);
    flex-shrink: 0;
}
.hero svg {
    width: min(100%, 280px);
    height: auto;
    flex: 0 1 280px;
    filter: drop-shadow(0 4px 12px rgba(95, 211, 219, 0.3));
}

/* ─── Animated Bridge ─── */
@keyframes bridgeDraw {
    from { stroke-dashoffset: 1000; }
    to { stroke-dashoffset: 0; }
}
.hero svg path {
    stroke-dasharray: 1000;
    animation: bridgeDraw 3s ease-out forwards;
}

/* ─── Stats Bar ─── */
.stats-bar {
    display: flex;
    gap: 12px;
    margin-bottom: 1.2rem;
    flex-wrap: wrap;
}
.stat-card {
    flex: 1;
    min-width: 140px;
    background: var(--surface);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 0.9rem 1rem;
    text-align: center;
    box-shadow: var(--shadow-sm);
    transition: transform 0.2s, box-shadow 0.2s;
}
.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}
.stat-number {
    font-size: 1.6rem;
    font-weight: 800;
    color: var(--primary);
    line-height: 1;
}
.stat-label {
    font-size: 0.78rem;
    color: var(--text-muted);
    margin-top: 0.3rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ─── Chat Messages ─── */
[data-testid="stChatMessage"] {
    background: var(--surface);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 1.1rem 1.2rem;
    box-shadow: var(--shadow-sm);
    animation: fadeSlideIn 0.3s ease-out;
}
@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]),
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(135deg, #E8F4F6 0%, #DFEEF0 100%);
    border-color: #BAD6DA;
}
[data-testid="stChatInput"] {
    border-radius: var(--radius-md);
}
[data-testid="stChatInput"] textarea {
    border-radius: var(--radius-sm) !important;
}

/* ─── Urgency Meter ─── */
.urg {
    --c: var(--primary);
    background: var(--surface);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border);
    border-left: 6px solid var(--c);
    border-radius: var(--radius-md);
    padding: 0.85rem 1.1rem;
    margin: 0 0 0.8rem;
    direction: ltr;
    text-align: left;
    box-shadow: var(--shadow-sm);
    transition: border-color 0.3s;
}
.urg-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
}
.urg-top b {
    font-size: 1.1rem;
    color: var(--text-primary);
    font-weight: 700;
}
.seg-row {
    display: inline-flex;
    gap: 5px;
}
.seg {
    width: 32px;
    height: 9px;
    border-radius: 4px;
    background: #E3EDF0;
    transition: background 0.4s ease;
}
.seg.on {
    background: var(--c);
    box-shadow: 0 1px 4px color-mix(in srgb, var(--c) 40%, transparent);
}
.urg-sub {
    color: var(--text-secondary);
    font-size: 0.92rem;
    margin-top: 0.3rem;
    font-weight: 500;
}
.urg.emg {
    background: linear-gradient(135deg, #FFF5F6 0%, #FFF0F1 100%);
    border-color: var(--danger);
}
.urg.emg .urg-sub {
    color: #9B1423;
    font-weight: 700;
}

/* ─── Symptom Tags ─── */
.symptom-tags {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    margin-bottom: 0.6rem;
}
.symptom-tag {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px 12px;
    background: linear-gradient(135deg, #E8F4F6 0%, #D5EDF0 100%);
    border: 1px solid #B5D8DE;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--primary-dark);
    letter-spacing: 0.02em;
}
.symptom-tag::before {
    content: '•';
    color: var(--primary);
    font-weight: 800;
}

/* ─── Welcome Card ─── */
.welcome {
    background: var(--surface);
    backdrop-filter: blur(12px);
    border: 2px dashed rgba(159, 191, 196, 0.5);
    border-radius: var(--radius-lg);
    padding: 1.8rem 1.5rem;
    color: var(--text-secondary);
    line-height: 1.6;
    text-align: center;
    box-shadow: var(--shadow-sm);
}
.welcome b { color: var(--text-primary); font-size: 1.15rem; }
.welcome-features {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
    margin-top: 1.2rem;
}
.welcome-feat {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 8px 16px;
    background: linear-gradient(135deg, #F0F7F8 0%, #E5F0F2 100%);
    border-radius: 30px;
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--text-primary);
    border: 1px solid var(--border);
}

/* ─── Voice Button ─── */
.voice-section {
    background: linear-gradient(135deg, #0B2F3A 0%, #0E7C86 100%);
    border-radius: var(--radius-md);
    padding: 0.8rem 1.2rem;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    box-shadow: var(--shadow-md);
}
.voice-label {
    color: white;
    font-size: 0.9rem;
    font-weight: 600;
}
.voice-label small {
    display: block;
    color: #9FC4CA;
    font-size: 0.78rem;
    font-weight: 400;
    margin-top: 0.15rem;
}

/* ─── Note Card ─── */
.note {
    background: linear-gradient(135deg, #FFF9E8 0%, #FFF7E0 100%);
    border: 1px solid #F0D98A;
    border-radius: var(--radius-md);
    padding: 0.85rem 1rem;
    color: #5A4500;
    font-size: 0.92rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
    box-shadow: var(--shadow-sm);
}

/* ─── X-ray Card ─── */
.xr {
    background: var(--surface);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 1.1rem 1.2rem;
    margin: 0.8rem 0;
    box-shadow: var(--shadow-sm);
}
.xr-top {
    display: flex;
    justify-content: space-between;
    font-weight: 700;
    margin-bottom: 0.6rem;
    color: var(--text-primary);
}
.bar {
    height: 12px;
    background: #E3EDF0;
    border-radius: 99px;
    overflow: hidden;
}
.bar i {
    display: block;
    height: 100%;
    border-radius: 99px;
    transition: width 1s ease-out;
}

/* ─── Footer ─── */
.foot {
    margin-top: 2.5rem;
    text-align: center;
    font-size: 0.82rem;
    color: var(--text-muted);
    padding: 1rem;
    border-top: 1px solid var(--border);
}

/* ─── Tabs ─── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    border-bottom: 2px solid #E3EDF0;
    background: var(--surface);
    border-radius: var(--radius-md) var(--radius-md) 0 0;
    padding: 0 0.5rem;
}
.stTabs [data-baseweb="tab"] {
    font-weight: 600;
    color: var(--text-muted);
    padding: 0.8rem 1.2rem;
    transition: color 0.2s;
    font-size: 0.95rem;
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--text-primary);
}
.stTabs [aria-selected="true"] {
    color: var(--primary) !important;
    font-weight: 700;
}
.stTabs [data-baseweb="tab-highlight"] {
    background: var(--primary);
    height: 3px;
    border-radius: 3px 3px 0 0;
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 1rem;
}

/* ─── Buttons ─── */
.stButton > button {
    border-radius: var(--radius-sm);
    border: 1px solid var(--border);
    background: var(--surface);
    color: var(--text-primary);
    font-weight: 600;
    transition: all 0.2s ease;
    box-shadow: var(--shadow-sm);
}
.stButton > button:hover {
    border-color: var(--primary);
    background: #F1F9FA;
    color: var(--primary-dark);
    transform: translateY(-1px);
    box-shadow: var(--shadow-md);
}
[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(135deg, #0B2F3A 0%, #0E7C86 100%);
    color: #fff;
    border: 0;
    border-radius: var(--radius-sm);
    font-weight: 700;
    padding: 0.6rem 1.2rem;
    box-shadow: 0 4px 12px rgba(14, 124, 134, 0.25);
    transition: all 0.2s ease;
}
[data-testid="stFormSubmitButton"] button:hover {
    background: linear-gradient(135deg, #0E7C86 0%, #10959F 100%);
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(14, 124, 134, 0.35);
}

/* ─── Forms ─── */
[data-testid="stForm"] {
    background: var(--surface);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 1.3rem;
    box-shadow: var(--shadow-sm);
}

/* ─── Sidebar ─── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #FFFFFF 0%, #F5F9FA 100%);
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] .stMarkdown h3 {
    font-size: 0.9rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.5rem;
}

/* ─── Metrics ─── */
[data-testid="stMetric"] {
    background: var(--surface);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 0.9rem 1.1rem;
    box-shadow: var(--shadow-sm);
}

/* ─── Accessibility ─── */
:focus-visible {
    outline: 3px solid var(--primary) !important;
    outline-offset: 2px;
}
@media (prefers-reduced-motion: reduce) {
    * { transition: none !important; animation: none !important; }
}

/* ─── Responsive ─── */
@media (max-width: 640px) {
    .stats-bar { flex-direction: column; }
    .hero { padding: 1.2rem; }
    .welcome-features { flex-direction: column; align-items: center; }
}
"""
st.markdown("<style>" + CSS + "</style>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════
#  HERO BANNER
# ════════════════════════════════════════════════════════════════════════
BRIDGE_SVG = (
    '<svg viewBox="0 0 360 90" fill="none" stroke="#5FD3DB" stroke-width="2.4" '
    'stroke-linecap="round" role="img" aria-label="Bridge illustration">'
    '<path d="M10 72H350"/><path d="M30 72C90 -4 270 -4 330 72"/>'
    '<path d="M80 72V42M120 72V26M160 72V16M200 72V16M240 72V26M280 72V42"/></svg>'
)

st.markdown(
    '<div class="hero">'
    "<div>"
    '<div class="brand">CareBridge<br>'
    '<span class="brand-sub">AI Health Guidance System</span></div>'
    '<div class="tag">Intelligent health guidance in your language — '
    "with a direct line to care.</div>"
    '<div class="features">'
    '<div class="feature-item"><span class="feature-dot"></span>English, اردو, Roman Urdu &amp; پښتو</div>'
    '<div class="feature-item"><span class="feature-dot"></span>Voice input supported — just speak</div>'
    '<div class="feature-item"><span class="feature-dot"></span>Smart symptom analysis with AI</div>'
    '<div class="feature-item"><span class="feature-dot"></span>Your symptom text is never stored</div>'
    "</div></div>" + BRIDGE_SVG + "</div>",
    unsafe_allow_html=True,
)

# ════════════════════════════════════════════════════════════════════════
#  API KEY CHECK
# ════════════════════════════════════════════════════════════════════════
if not os.environ.get("GEMINI_API_KEY"):
    try:
        os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
    except Exception:
        st.error("🔑 GEMINI_API_KEY is not set. Set it in the terminal or Streamlit secrets, then rerun.")
        st.stop()

# ════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### 🌐 Language")
    lang = st.selectbox("Select language / زبان منتخب کریں", list(LANGS), label_visibility="collapsed")

    RTL = {
        "اردو (Urdu)": "font-family:'Noto Nastaliq Urdu',serif;line-height:2.3;",
        "پښتو (Pashto)": "font-family:'Noto Naskh Arabic',serif;line-height:2;",
    }
    if lang in RTL:
        st.markdown(
            "<style>[data-testid='stChatMessage']{direction:rtl;text-align:right;" + RTL[lang] + "}</style>",
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("### 💡 Quick Examples")
    for label, text in EXAMPLES:
        if st.button(label, use_container_width=True):
            st.session_state.pending = text

    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.caption(
        "CareBridge provides AI-powered health guidance for Pakistan. "
        "It supports 4 languages, uses smart symptom analysis, "
        "and prioritizes your privacy — symptom text is never stored."
    )

# ════════════════════════════════════════════════════════════════════════
#  STATS BAR
# ════════════════════════════════════════════════════════════════════════
triage_count = 0
appt_count = 0
if os.path.exists("logs/triage_log.csv"):
    try:
        df_stats = pd.read_csv("logs/triage_log.csv")
        triage_count = len(df_stats)
    except Exception:
        pass
if os.path.exists("logs/appointment_log.csv"):
    try:
        df_appt = pd.read_csv("logs/appointment_log.csv")
        appt_count = len(df_appt)
    except Exception:
        pass

st.markdown(
    '<div class="stats-bar">'
    f'<div class="stat-card"><div class="stat-number">{triage_count}</div>'
    '<div class="stat-label">Symptom Checks</div></div>'
    '<div class="stat-card"><div class="stat-number">4</div>'
    '<div class="stat-label">Languages</div></div>'
    f'<div class="stat-card"><div class="stat-number">{appt_count}</div>'
    '<div class="stat-label">Appointments</div></div>'
    '<div class="stat-card"><div class="stat-number">12</div>'
    '<div class="stat-label">Symptom Areas</div></div>'
    "</div>",
    unsafe_allow_html=True,
)


# ════════════════════════════════════════════════════════════════════════
#  URGENCY METER COMPONENT
# ════════════════════════════════════════════════════════════════════════
def meter(level: str) -> str:
    """Render an urgency meter badge."""
    idx = LEVELS.index(level)
    segs = "".join(
        '<i class="seg%s"></i>' % (" on" if k <= idx else "") for k in range(4)
    )
    emoji = {"Home care": "🟢", "See a doctor soon": "🟡", "Urgent": "🟠", "Emergency": "🔴"}.get(level, "⚪")
    return (
        '<div class="urg%s" style="--c:%s">'
        '<div class="urg-top"><b>%s %s</b>'
        '<span class="seg-row" role="img" aria-label="Level %d of 4">%s</span></div>'
        '<div class="urg-sub">%s</div></div>'
        % (
            " emg" if level == "Emergency" else "",
            COLORS[level],
            emoji,
            level,
            idx + 1,
            segs,
            HINTS[level],
        )
    )


# ════════════════════════════════════════════════════════════════════════
#  VOICE INPUT COMPONENT (Web Speech API)
# ════════════════════════════════════════════════════════════════════════
VOICE_HTML = """
<div id="voiceContainer" style="display:flex;align-items:center;gap:12px;width:100%;">
    <button id="voiceBtn" onclick="toggleVoice()" style="
        display:flex; align-items:center; gap:10px;
        padding:10px 22px;
        background:linear-gradient(135deg,#0B2F3A 0%,#0E7C86 100%);
        border:none; border-radius:50px; cursor:pointer;
        color:white; font-family:'Plus Jakarta Sans',sans-serif;
        font-size:14px; font-weight:600;
        box-shadow:0 4px 15px rgba(14,124,134,0.3);
        transition:all 0.3s ease; user-select:none; white-space:nowrap;">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="white">
            <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/>
            <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
        </svg>
        <span id="btnText">🎙️ Tap to speak</span>
        <span id="waveBars" style="display:none;align-items:center;gap:3px;height:18px;">
            <span style="width:3px;background:white;border-radius:2px;height:6px;animation:w .8s ease-in-out infinite"></span>
            <span style="width:3px;background:white;border-radius:2px;height:12px;animation:w .8s ease-in-out infinite .1s"></span>
            <span style="width:3px;background:white;border-radius:2px;height:18px;animation:w .8s ease-in-out infinite .2s"></span>
            <span style="width:3px;bac</script>
            """