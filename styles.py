"""All CSS lives here. Palette: ink #0B2B30, teal #0E7C86, mist #F1F5F5, line #D5E1E3, alert #C62839."""

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Noto+Nastaliq+Urdu:wght@400;600&family=Noto+Naskh+Arabic:wght@400;600&display=swap');
:root { --ink:#0B2B30; --teal:#0E7C86; --teal-d:#0A5F67; --mist:#F1F5F5; --paper:#FFFFFF; --line:#D5E1E3; --muted:#4A666D;
        --alert:#C62839; --amber:#D99A00; --orange:#E36A14; --green:#2F9E6E; }
html, body, [class*="st-"], .stApp { font-family:'Plus Jakarta Sans','Noto Naskh Arabic',system-ui,sans-serif; }
.stApp { background:var(--mist); color:var(--ink); }
#MainMenu, footer { visibility:hidden; }
header[data-testid="stHeader"] { background:transparent; }
.block-container { max-width:880px; padding-top:1.2rem; padding-bottom:5rem; }
h1,h2,h3 { color:var(--ink); letter-spacing:-.015em; font-weight:700; }

/* ---------- hero ---------- */
.hero { background:var(--ink); color:#E6F1F2; border-radius:20px; padding:clamp(1.2rem,4vw,2.1rem); display:flex; flex-wrap:wrap;
        gap:1.2rem 2rem; align-items:center; justify-content:space-between; position:relative; overflow:hidden; }
.hero .brand { font-size:clamp(2rem,6.5vw,3.1rem); font-weight:800; letter-spacing:-.04em; line-height:1; color:#fff; }
.hero .tag { margin-top:.65rem; font-size:1.02rem; color:#C5DDE0; max-width:34ch; line-height:1.5; }
.hero svg { width:min(100%,260px); height:auto; flex:0 1 260px; opacity:.95; }
.pills { display:flex; flex-wrap:wrap; gap:.5rem; margin:.8rem 0 1.2rem; }
.pill { background:var(--paper); border:1px solid var(--line); color:var(--ink); border-radius:999px; padding:.32rem .8rem; font-size:.84rem; font-weight:600; }
.pill b { color:var(--teal-d); }
.pill.warn { background:#FFF6DD; border-color:#EBD58A; color:#5A4500; }

/* ---------- chat ---------- */
[data-testid="stChatMessage"] { background:var(--paper); border:1px solid var(--line); border-radius:16px; padding:1rem 1.1rem; }
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]),
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) { background:#E3F0F1; border-color:#BBD7DA; }
[data-testid="stChatInput"] { border-radius:14px; }

/* ---------- urgency card ---------- */
.urg { --c:var(--teal); background:var(--paper); border:1px solid var(--line); border-left:6px solid var(--c); border-radius:14px;
       padding:.8rem 1rem; margin:0 0 .7rem; direction:ltr; text-align:left; }
.urg-top { display:flex; justify-content:space-between; align-items:center; gap:1rem; flex-wrap:wrap; }
.urg-top b { font-size:1.12rem; color:var(--ink); }
.seg-row { display:inline-flex; gap:4px; }
.seg { width:30px; height:9px; border-radius:3px; background:#DCE7E9; }
.seg.on { background:var(--c); }
.urg-sub { color:var(--muted); font-size:.92rem; margin-top:.25rem; }
.urg.emg { background:#FFF1F2; border-color:#F0B9BF; }
.urg.emg .urg-sub { color:#8E1320; font-weight:700; }
.call { display:inline-block; margin:.6rem .5rem 0 0; background:var(--alert); color:#fff !important; font-weight:800; text-decoration:none !important;
        padding:.62rem 1.3rem; border-radius:12px; font-size:1.05rem; }
.call.alt { background:transparent; color:var(--alert) !important; border:2px solid var(--alert); }
.chips { display:flex; flex-wrap:wrap; gap:.35rem; margin:.1rem 0 .7rem; direction:ltr; }
.chip { background:#EAF3F4; border:1px solid #C9DEE1; color:#1D4A52; border-radius:999px; padding:.14rem .6rem; font-size:.78rem; font-weight:600; }
.chip.mem { background:#EDE8FA; border-color:#D3C9F0; color:#43318A; }

/* ---------- misc cards ---------- */
.welcome { border:1.5px dashed #9CBBC0; border-radius:16px; padding:1.1rem 1.25rem; color:#27454D; line-height:1.6; background:rgba(255,255,255,.65); }
.welcome ul { margin:.4rem 0 0 1.1rem; padding:0; }
.note { background:#FFF6DD; border:1px solid #EBD58A; border-radius:12px; padding:.7rem .9rem; color:#5A4500; font-size:.92rem; margin-bottom:1rem; }
.xr { background:#fff; border:1px solid var(--line); border-radius:14px; padding:1rem 1.1rem; margin:.8rem 0; }
.xr-top { display:flex; justify-content:space-between; font-weight:700; margin-bottom:.5rem; }
.bar { height:10px; background:#DCE7E9; border-radius:99px; overflow:hidden; }
.bar i { display:block; height:100%; }
.foot { margin-top:2rem; text-align:center; font-size:.82rem; color:var(--muted); }

/* ---------- tabs, buttons, forms, sidebar ---------- */
.stTabs [data-baseweb="tab-list"] { gap:1.3rem; border-bottom:1px solid #C9DADD; }
.stTabs [data-baseweb="tab"] { font-weight:600; color:var(--muted); padding:.6rem .1rem; }
.stTabs [aria-selected="true"] { color:var(--ink); }
.stTabs [data-baseweb="tab-highlight"] { background:var(--teal); height:3px; }
.stButton > button, .stDownloadButton > button { border-radius:10px; border:1px solid #B5CFD3; background:#fff; color:var(--ink); font-weight:600; }
.stButton > button:hover, .stDownloadButton > button:hover { border-color:var(--teal); background:#F1F9FA; color:var(--ink); }
.stButton > button[kind="primary"], [data-testid="stFormSubmitButton"] button { background:var(--ink); color:#fff; border:0; border-radius:10px; font-weight:700; }
.stButton > button[kind="primary"]:hover, [data-testid="stFormSubmitButton"] button:hover { background:var(--teal); color:#fff; }
[data-testid="stForm"] { background:#fff; border:1px solid var(--line); border-radius:14px; padding:1.1rem; }
[data-testid="stSidebar"] { background:#fff; border-right:1px solid var(--line); }
[data-testid="stMetric"] { background:#fff; border:1px solid var(--line); border-radius:14px; padding:.8rem 1rem; }
[data-testid="stExpander"] { border:1px solid var(--line); border-radius:12px; background:#fff; }
:focus-visible { outline:3px solid var(--teal) !important; outline-offset:2px; }
@media (max-width:640px) { .seg { width:22px; } .hero svg { display:none; } }
@media (prefers-reduced-motion: reduce) { * { transition:none !important; animation:none !important; } }
"""

RTL_CSS = {
    "اردو (Urdu)": "font-family:'Noto Nastaliq Urdu',serif;line-height:2.3;",
    "پښتو (Pashto)": "font-family:'Noto Naskh Arabic',serif;line-height:2;",
}


def rtl_css(lang):
    if lang not in RTL_CSS:
        return ""
    return ("[data-testid='stChatMessage'] [data-testid='stMarkdownContainer'] {direction:rtl;text-align:right;%s}" % RTL_CSS[lang])
