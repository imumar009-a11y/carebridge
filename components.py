"""Small reusable HTML pieces."""
import html
import json
import streamlit as st
import streamlit.components.v1 as components
from cb.config import LEVELS, EMERGENCY_NUMBER

COLORS = {"Home care": "#2F9E6E", "See a doctor soon": "#D99A00", "Urgent": "#E36A14", "Emergency": "#C62839"}

BRIDGE = ('<svg viewBox="0 0 360 90" fill="none" stroke="#5FD3DB" stroke-width="2.4" stroke-linecap="round" role="img" aria-label="A bridge">'
          '<path d="M10 72H350"/><path d="M30 72C90 -4 270 -4 330 72"/><path d="M80 72V42M120 72V26M160 72V16M200 72V16M240 72V26M280 72V42"/></svg>')


def hero():
    st.markdown(
        '<div class="hero"><div><div class="brand">CareBridge</div>'
        '<div class="tag">Health guidance in your own language, with a direct line to the clinic.</div></div>' + BRIDGE + '</div>',
        unsafe_allow_html=True)


def status_strip(ai_on, mem_on, n_areas):
    pills = [
        ('<span class="pill"><b>Gemini + safety rules</b></span>' if ai_on else
         '<span class="pill warn">AI offline: safety rules only (English)</span>'),
        '<span class="pill"><b>%d</b> symptom areas</span>' % n_areas,
        '<span class="pill"><b>4</b> languages: English, اردو, Roman Urdu, پښتو</span>',
        '<span class="pill"><b>Voice</b> input</span>',
        ('<span class="pill"><b>Memory on</b></span>' if mem_on else '<span class="pill">Memory off</span>'),
    ]
    st.markdown('<div class="pills">' + "".join(pills) + '</div>', unsafe_allow_html=True)


def urgency_card(level, hint):
    i = LEVELS.index(level)
    segs = "".join('<i class="seg%s"></i>' % (" on" if k <= i else "") for k in range(4))
    emg = level == "Emergency"
    call = ('<a class="call" href="tel:%s">Call %s</a><a class="call alt" href="tel:115">Edhi 115</a>' % (EMERGENCY_NUMBER, EMERGENCY_NUMBER)) if emg else ""
    return ('<div class="urg%s" style="--c:%s"><div class="urg-top"><b>%s</b><span class="seg-row" role="img" aria-label="Level %d of 4">%s</span></div>'
            '<div class="urg-sub">%s</div>%s</div>'
            % (" emg" if emg else "", COLORS[level], html.escape(level), i + 1, segs, html.escape(hint), call))


def chips(items, memory_flag="saved profile used"):
    if not items:
        return ""
    out = "".join('<span class="chip%s">%s</span>' % (" mem" if x == memory_flag else "", html.escape(x)) for x in items)
    return '<div class="chips">' + out + '</div>'


_TTS_LANG = {"English": "en-IN", "اردو (Urdu)": "ur-PK", "Roman Urdu": "en-IN", "پښتو (Pashto)": "ps-AF"}


def listen_button(text, lang):
    """Read an answer aloud with the browser's own speech engine (no server, no cost)."""
    payload = json.dumps(text[:1800], ensure_ascii=False).replace("</", "<\\/")
    code = json.dumps(_TTS_LANG.get(lang, "en-IN"))
    components.html("""
<button id="b" style="font:600 14px system-ui,sans-serif;padding:7px 14px;border-radius:10px;border:1px solid #B5CFD3;background:#fff;color:#0B2B30;cursor:pointer">🔊 Listen</button>
<span id="m" style="font:12px system-ui,sans-serif;color:#4A666D;margin-left:8px"></span>
<script>
const text=%s, lang=%s, b=document.getElementById('b'), m=document.getElementById('m');
b.onclick=()=>{
  if(!('speechSynthesis' in window)){m.textContent='This browser cannot read aloud.';return;}
  if(speechSynthesis.speaking){speechSynthesis.cancel();b.textContent='🔊 Listen';return;}
  const u=new SpeechSynthesisUtterance(text); u.lang=lang; u.rate=0.95;
  const pre=lang.slice(0,2).toLowerCase();
  let v=speechSynthesis.getVoices().find(x=>x.lang.toLowerCase().startsWith(pre));
  if(!v && pre==='ps') v=speechSynthesis.getVoices().find(x=>x.lang.toLowerCase().startsWith('ur'));
  if(v){u.voice=v;} else {m.textContent='No voice for this language on your device.';}
  u.onend=()=>{b.textContent='🔊 Listen';}; b.textContent='⏹ Stop'; speechSynthesis.speak(u);
};
</script>""" % (payload, code), height=44)
