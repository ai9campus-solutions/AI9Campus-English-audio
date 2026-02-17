import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
from gtts import gTTS
from streamlit_mic_recorder import mic_recorder
import tempfile

# ═══════════════════════════════════════════════════════════════
# ENV SETUP
# ═══════════════════════════════════════════════════════════════
load_dotenv()

api_key = os.getenv("GROK-API-KEY")
if not api_key:
    st.error("API Key Missing. Add GROK-API-KEY in .env file")
    st.stop()

client = Groq(api_key=api_key)

# ═══════════════════════════════════════════════════════════════
# PAGE CONFIG (MOBILE OPTIMIZED)
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Smart Tutor - Telangana SCERT",
    page_icon="🎓",
    layout="centered"
)

# Mobile friendly CSS
st.markdown("""
<style>
html, body, [class*="css"]  {
    font-size: 16px;
}
.main-header {
    text-align:center;
    font-size:28px;
    font-weight:bold;
    color:#1E88E5;
}
.sub-header {
    text-align:center;
    color:gray;
    margin-bottom:10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🎓 Smart Tutor</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Telangana State Board (SCERT)</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# SYSTEM PROMPT (STRICT ACADEMIC MODE)
# ═══════════════════════════════════════════════════════════════
SYSTEM_PROMPT = """
You are a Telangana State Board (SCERT) tutor.

STRICT RULES:
- Answer ONLY academic syllabus questions (Classes 1–10)
- Refuse non-educational questions politely
- Explain like a friendly teacher
- Use simple analogies
- Respond in selected language when possible
"""

# ═══════════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════════
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# ═══════════════════════════════════════════════════════════════
# SIDEBAR SETTINGS
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.header("⚙️ Voice Settings")

    voice_gender = st.selectbox(
        "Voice Type",
        ["Female", "Male"]
    )

    voice_lang = st.selectbox(
        "Voice Language",
        ["English", "Telugu", "Hindi"]
    )

    st.divider()

    if st.button("🔄 Reset Chat"):
        st.session_state.clear()
        st.rerun()

# ═══════════════════════════════════════════════════════════════
# CHAT HISTORY DISPLAY
# ═══════════════════════════════════════════════════════════════
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ═══════════════════════════════════════════════════════════════
# VOICE INPUT
# ═══════════════════════════════════════════════════════════════
st.markdown("### 🎤 Speak or Type Your Question")

audio = mic_recorder(
    start_prompt="🎙️ Start Recording",
    stop_prompt="⏹️ Stop Recording",
    just_once=True,
    use_container_width=True
)

# Dummy transcription (replace with real STT later)
def transcribe_audio(audio_bytes):
    return "Explain photosynthesis"

# Text input
text_prompt = st.chat_input("Type your question here...")

prompt = None

if audio:
    prompt = transcribe_audio(audio['bytes'])

elif text_prompt:
    prompt = text_prompt

# ═══════════════════════════════════════════════════════════════
# RESPONSE LOGIC
# ═══════════════════════════════════════════════════════════════
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        try:
            stream = client.chat.completions.create(
                model="moonshotai/kimi-k2-instruct-0905",
                messages=st.session_state.messages,
                temperature=0.5,
                stream=True
            )

            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    token = chunk.choices[0].delta.content
                    full_response += token
                    placeholder.markdown(full_response + "▌")

            placeholder.markdown(full_response)

            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )

            # ═══════════════════════════════════════════
            # TEXT → SPEECH
            # ═══════════════════════════════════════════
            lang_code = "en"

            if voice_lang == "Telugu":
                lang_code = "te"
            elif voice_lang == "Hindi":
                lang_code = "hi"

            tts = gTTS(text=full_response, lang=lang_code)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                audio_path = fp.name

            st.audio(audio_path)

        except Exception as e:
            st.error(f"Error: {str(e)}")

# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════
st.divider()
st.caption("Powered by AI Tutor | Telangana SCERT Learning Assistant")
