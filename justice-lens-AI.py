import streamlit as st
from streamlit_lottie import st_lottie
import json
import random
import os
from tempfile import NamedTemporaryFile
from gtts import gTTS
import base64

# Set up the app config
st.set_page_config(page_title="Justice Lens AI", layout="wide", initial_sidebar_state="expanded")

# Custom bright, high-contrast theme for readability
st.markdown("""
    <style>
    body, .stApp { background-color: #0f172a; color: #f8fafc; font-family: 'Segoe UI', sans-serif; }
    .sidebar .sidebar-content { background-color: #1f2937; color: #f8fafc; }
    h1, h2, h3, h4, h5, h6 { color: #facc15 !important; }
    .stRadio > div { background-color: #1e293b; padding: 20px; border-radius: 10px; font-size: 22px; }
    .stRadio > div label { color: #ffffff; font-size: 20px; }
    .stSelectbox, .stTextInput, .stButton button { color: #000000; }
    .stSuccess { background-color: #14532d !important; }
    .stError { background-color: #7f1d1d !important; }
    .ai-box { background-color: #1e293b; padding: 1em; border-left: 5px solid #facc15; border-radius: 10px; font-size: 1.1em; }
    .timeline-box { background-color: #334155; padding: 1em; border-left: 4px solid #38bdf8; border-radius: 8px; margin-bottom: 1em; }
    .quiz { background-color: #1e293b; padding: 1em; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# TTS using gTTS
def speak_text(text):
    try:
        tts = gTTS(text)
        with NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            audio_bytes = open(fp.name, "rb").read()
            b64 = base64.b64encode(audio_bytes).decode()
            st.audio(f"data:audio/mp3;base64,{b64}", format="audio/mp3")
    except Exception as e:
        st.warning("Voice playback failed.")

# ---------------------- Intro Section ----------------------
st.title("⚖️ Justice Lens AI")

st.markdown("""
Welcome to **Justice Lens AI**, a civic technology prototype that demonstrates how artificial intelligence can contribute to criminal case evaluations. 

While real-world courts are shaped by laws, history, politics, and human judgment, this app explores an alternative: what would it look like if an AI attempted to judge using purely neutral, ethical reasoning based on case facts?

Explore real, controversial criminal cases — some where human decisions were arguably biased — and compare your judgment with that of an AI attempting neutrality.

---
""")

# ---------------------- Real Legal Case Studies ----------------------
case_studies = [
    {
        "title": "Case of the Subway Incident - Jamal Thompson",
        "facts": "A Black teenager was arrested after being accused of fare evasion on the subway. Police used physical force. CCTV later showed he had a valid pass.",
        "bias_note": "Racial bias in assumption of guilt.",
        "human_prompt": "What would you decide in this case?",
        "ai_judgment": "The individual should be released with a formal apology and compensation.",
        "real_outcome": "The teen was charged and spent 3 days in juvenile detention.",
        "ai_opinion": "This reflects systemic racial profiling. A fair system would prioritize evidence before action."
    },
    {
        "title": "Case of Protest Arrest - Anjali Rao",
        "facts": "A woman protesting outside a government building was arrested and charged with disorderly conduct. Video shows she was peaceful.",
        "bias_note": "Political bias potentially influenced the arrest.",
        "human_prompt": "Should she face consequences for the protest?",
        "ai_judgment": "No charges should be filed. Peaceful protest is a protected right.",
        "real_outcome": "Charges were dropped after 2 months.",
        "ai_opinion": "Protecting freedom of expression is essential in a democracy. Bias against protestors must be carefully examined."
    },
    {
        "title": "Priyadarshini Mattoo Case - Santosh Singh",
        "facts": "Law student Priyadarshini Mattoo was found murdered in her home. The prime suspect was a fellow law student and IPS officer's son. Despite strong evidence, he was initially acquitted.",
        "bias_note": "Influence of power and police connections allegedly led to initial acquittal.",
        "human_prompt": "What would you decide with the available evidence?",
        "ai_judgment": "A conviction should be pursued based on forensic evidence and witness testimonies.",
        "real_outcome": "Initial acquittal was overturned by Delhi High Court; the accused was sentenced to death, later commuted.",
        "ai_opinion": "Justice delayed due to systemic privilege. A fair system must ensure equality before the law regardless of social or political connections."
    },
    {
        "title": "Hashimpura Massacre Case - Indian Army Personnel",
        "facts": "In 1987, 42 Muslim men were allegedly rounded up by members of the Provincial Armed Constabulary in Uttar Pradesh and shot dead. Survivors testified against the accused.",
        "bias_note": "Religious bias and abuse of state power.",
        "human_prompt": "How should such state-led killings be handled?",
        "ai_judgment": "Thorough investigation, trials for those involved, and reparations to victims' families.",
        "real_outcome": "After 31 years, 16 ex-PAC personnel were convicted by Delhi HC in 2018.",
        "ai_opinion": "Delayed justice in communal violence undermines trust. The case is a reminder of the need for prompt legal action in state excess."
    },
    {
        "title": "Ruchika Girhotra Case - S.P.S. Rathore",
        "facts": "14-year-old Ruchika was molested by a senior police officer. She faced harassment for filing a complaint, including expulsion from school. She later died by suicide.",
        "bias_note": "Abuse of power and delayed justice.",
        "human_prompt": "Should the officer have faced harsher punishment early on?",
        "ai_judgment": "Immediate suspension, criminal prosecution, and protection for the victim were warranted.",
        "real_outcome": "Officer was sentenced 19 years later to a light sentence. Many claimed it was insufficient.",
        "ai_opinion": "The delay and leniency reflected systemic protection of powerful individuals. A fair system must act swiftly to protect victims."
    }
]

# Sidebar and setup
with st.sidebar:
    st.header("🔎 Case Selection")
    st.caption("Explore real criminal cases where bias may have played a role. Compare your judgment to a neutral AI.")
    selected_case_title = st.selectbox("Choose a case to judge:", [c["title"] for c in case_studies])

selected_case = next(c for c in case_studies if c["title"] == selected_case_title)

# Main content
st.header(f"📂 {selected_case['title']}")

st.markdown(f"""
### 🔍 Case Facts:
{selected_case['facts']}

📌 **Bias Observation:** {selected_case['bias_note']}

---
""")

# Visual timeline of the case
st.markdown("### ⏳ Case Timeline")
st.markdown("""
<div class="timeline-box">🚔 Arrest → 📹 Evidence Review → ⚖️ Human Judgment → 🤖 AI Judgment</div>
""", unsafe_allow_html=True)

# Quiz Mode: Judge before seeing AI
st.subheader("🧑‍⚖️ Judge Before the AI")
with st.expander("Make your judgment before seeing the AI's decision"):
    user_decision = st.radio(
        selected_case['human_prompt'],
        ["Release", "Sentence", "Dismiss", "Warning/Education"],
        key="user_decision"
    )

if "user_decision" in st.session_state:
    st.markdown("---")
    st.subheader("🤖 AI Judge's Recommendation")
    st.markdown(f"""
    <div class='ai-box'>
        <strong>{selected_case['ai_judgment']}</strong>
    </div>
    """, unsafe_allow_html=True)
    speak_text(selected_case['ai_judgment'])

    st.markdown("---")
    st.subheader("📊 Analysis")
    if st.session_state.user_decision.lower() in selected_case["ai_judgment"].lower():
        st.success("✅ Your decision aligns with an unbiased legal interpretation.")
    else:
        st.error("❌ Your judgment differs from a neutral legal interpretation. Consider how bias might influence decisions.")

    st.markdown(f"""
    ### ⚖️ Real Outcome:
    {selected_case['real_outcome']}
    """)

    st.markdown("---")
    st.markdown(f"""
    ### 🧠 AI's Perspective on the Outcome:
    {selected_case['ai_opinion']}
    """)

    st.markdown("---")
    st.markdown("""
    ### 📚 Educational Note:
    Real legal decisions are often influenced by systemic factors. This simulation shows how AI might approach justice based on fairness, equity, and consistency — a valuable perspective for rethinking justice systems.
    """)

    st.markdown("<small>Justice Lens AI – understanding bias, one case at a time.</small>", unsafe_allow_html=True)
