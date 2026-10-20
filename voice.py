"""Voice input: record (or upload a voice note) -> Gemini transcribes -> you review the text -> send."""
import hashlib
import streamlit as st
from cb import ai

_MIME = {"wav": "audio/wav", "mp3": "audio/mp3", "ogg": "audio/ogg", "oga": "audio/ogg", "opus": "audio/ogg",
         "aac": "audio/aac", "m4a": "audio/aac", "flac": "audio/flac"}


def _mime(f):
    ext = (getattr(f, "name", "") or "").rsplit(".", 1)[-1].lower()
    return _MIME.get(ext) or getattr(f, "type", None) or "audio/wav"


def voice_input(lang):
    """Returns the text to send, or None. Shows its own small panel."""
    ss = st.session_state
    ss.setdefault("v_nonce", 0)
    ss.setdefault("v_text", "")
    ss.setdefault("v_hash", None)
    ss.setdefault("v_err", "")
    send = None
    with st.expander("🎙️ Speak instead of typing", expanded=bool(ss.v_text)):
        if not ai.available():
            st.info("Voice needs the Gemini key (it turns speech into text). Set GEMINI_API_KEY and reload.")
            return None
        n = ss.v_nonce
        audio = st.audio_input("Press the mic, speak, press stop", key="rec_%d" % n) if hasattr(st, "audio_input") else None
        up = st.file_uploader("…or upload a voice note (WhatsApp .ogg/.opus, mp3, wav, m4a)", type=list(_MIME), key="up_%d" % n)
        src = audio or up
        if src is not None:
            data = src.getvalue()
            h = hashlib.sha1(data).hexdigest()
            if h != ss.v_hash:
                ss.v_hash = h
                with st.spinner("Listening…"):
                    txt = ai.transcribe(data, _mime(src), lang)
                ss.v_text = txt
                ss.v_err = "" if txt else "I could not hear clear speech. Please try again, closer to the microphone."
                ss.v_nonce += 1          # resets the recorder so the next recording starts clean
                st.rerun()
        if ss.v_err:
            st.warning(ss.v_err)
        if ss.v_text:
            edited = st.text_area("Check what I heard and fix it if needed", value=ss.v_text, key="vt_%d" % ss.v_nonce, height=96)
            c1, c2 = st.columns(2)
            if c1.button("Send", type="primary", use_container_width=True, key="vsend_%d" % ss.v_nonce) and edited.strip():
                send = edited.strip()
                ss.v_text, ss.v_err = "", ""
                ss.v_nonce += 1
            if c2.button("Discard", use_container_width=True, key="vdisc_%d" % ss.v_nonce):
                ss.v_text, ss.v_err = "", ""
                ss.v_nonce += 1
                st.rerun()
    return send
