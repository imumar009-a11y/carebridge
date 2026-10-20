"""Sidebar: language, examples, new check, memory panel."""
import datetime
import streamlit as st
from cb.config import LANGS
from cb.memory import MemoryStore, Profile
from cb.patient import CONDITION_LABELS

EXAMPLES = [("🌡️ Fever and headache", "I have fever and headache for 2 days"),
            ("🧒 Child with fever", "My 3-year-old has had a fever for 2 days"),
            ("❤️ Chest pain", "chest pain"),
            ("🗣️ Roman Urdu", "mujhe bukhar aur sar dard hai"),
            ("🤰 Pregnancy concern", "I am 6 months pregnant with a bad headache and blurry vision"),
            ("🩸 Sugar reading", "My father is 62 with diabetes, his sugar is 320 and he feels weak")]


def render():
    ss = st.session_state
    st.sidebar.markdown("### Language / زبان")
    lang = st.sidebar.selectbox("Language", list(LANGS), label_visibility="collapsed")
    st.sidebar.markdown("**Try an example**")
    for label, text in EXAMPLES:
        if st.sidebar.button(label, use_container_width=True, key="ex_" + label):
            ss.pending = text
    if st.sidebar.button("↺ Start a new check", use_container_width=True):
        ss.msgs, ss.case = [], {}
        st.rerun()
    _memory_panel()
    return lang


def _memory_panel():
    ss = st.session_state
    with st.sidebar.expander("🧠 Memory (optional)", expanded=bool(ss.get("memory"))):
        mem = ss.get("memory")
        if mem is None:
            st.caption("Off by default. If you turn it on, CareBridge remembers your health profile and past checks "
                       "(symptom tags and urgency, never your words) so advice fits you. You can download or delete it at any time.")
            name = st.text_input("Memory name", key="mem_name", placeholder="e.g. ali")
            pin = st.text_input("PIN (4 or more characters)", type="password", key="mem_pin")
            agree = st.checkbox("I agree to save this on this server", key="mem_agree")
            if st.button("Turn on memory", use_container_width=True, type="primary"):
                if not (name.strip() and len(pin) >= 4 and agree):
                    st.warning("Enter a name, a PIN of 4+ characters, and tick the agreement.")
                else:
                    store = MemoryStore()
                    ss.memory = store.load(name, pin) or store.create(name, pin)
                    st.rerun()
            st.caption("Not encrypted. Do not use on a shared public server for sensitive data.")
            return
        _profile_form(mem)
        c1, c2 = st.columns(2)
        c1.download_button("Download", mem.export_json(), file_name="my_carebridge_memory.json", mime="application/json", use_container_width=True)
        if c2.button("Turn off", use_container_width=True):
            ss.memory = None
            st.rerun()
        if mem.history:
            st.markdown("**Recent checks**")
            for h in reversed(mem.history[-5:]):
                st.caption("%s · %s · %s" % (h["date"], ", ".join(h["symptoms"]), h["urgency"]))
            if st.button("Clear history", use_container_width=True):
                mem.clear_history()
                st.rerun()
        if st.button("Forget me (delete everything)", use_container_width=True):
            mem.store.delete(mem.name, mem.pin)
            ss.memory = None
            st.rerun()


def _profile_form(mem):
    p = mem.profile
    keys = list(CONDITION_LABELS)
    with st.form("profile"):
        st.markdown("**Your health profile**")
        nick = st.text_input("Nickname (optional)", value=p.nickname)
        year = st.number_input("Year of birth (0 = not set)", min_value=0, max_value=datetime.date.today().year, value=int(p.birth_year or 0), step=1)
        sex = st.selectbox("Sex", ["Not set", "female", "male"], index=["Not set", "female", "male"].index(p.sex or "Not set"))
        preg = st.checkbox("Currently pregnant", value=p.pregnant)
        conds = st.multiselect("Long-term conditions", keys, default=[c for c in p.conditions if c in keys], format_func=lambda k: CONDITION_LABELS[k])
        allergies = st.text_input("Allergies (comma separated)", value=", ".join(p.allergies))
        meds = st.text_input("Regular medicines (comma separated)", value=", ".join(p.medications))
        keep = st.checkbox("Remember my past checks", value=mem.save_history)
        if st.form_submit_button("Save profile"):
            mem.profile = Profile(nickname=nick.strip(), birth_year=int(year) or None, sex=None if sex == "Not set" else sex,
                                  pregnant=bool(preg) and sex != "male", conditions=conds,
                                  allergies=[a.strip() for a in allergies.split(",") if a.strip()],
                                  medications=[m.strip() for m in meds.split(",") if m.strip()], language=p.language)
            mem.save_history = keep
            mem.save()
            st.success("Saved")
