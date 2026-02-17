import streamlit as st
from groq import Groq
import os
import json
import hashlib
import datetime
from dotenv import load_dotenv
from pathlib import Path
import base64

# ═══════════════════════════════════════════════════════════════
# 1. ENVIRONMENT SETUP
# ═══════════════════════════════════════════════════════════════
load_dotenv()

# ═══════════════════════════════════════════════════════════════
# 2. PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="School Name Smart Tutor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════
# 3. CUSTOM CSS - PROFESSIONAL DARK EDU THEME
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Root Variables ── */
:root {
    --primary:    #4F8EF7;
    --primary-dk: #2563EB;
    --accent:     #22D3A5;
    --accent2:    #F59E0B;
    --danger:     #EF4444;
    --bg:         #0D1117;
    --bg2:        #161B22;
    --bg3:        #21262D;
    --border:     #30363D;
    --text:       #E6EDF3;
    --text-muted: #7D8590;
    --radius:     12px;
    --shadow:     0 8px 32px rgba(0,0,0,0.4);
}

/* ── Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    font-family: 'Outfit', sans-serif !important;
    color: var(--text) !important;
}

[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stHeader"] { background: transparent !important; }
.block-container { padding: 1.5rem 2rem !important; max-width: 1100px !important; }

/* ── Hero Banner ── */
.hero-banner {
    background: linear-gradient(135deg, #1a2744 0%, #0D1117 50%, #0f2a1f 100%);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -20%;
    width: 60%;
    height: 200%;
    background: radial-gradient(ellipse, rgba(79,142,247,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #4F8EF7, #22D3A5);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.3rem;
}
.hero-sub {
    color: var(--text-muted);
    font-size: 0.95rem;
    font-weight: 400;
}

/* ── Cards ── */
.card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
}
.card:hover { border-color: var(--primary); }

.stat-card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.2rem 1rem;
    text-align: center;
    transition: all 0.2s;
}
.stat-card:hover {
    border-color: var(--accent);
    transform: translateY(-2px);
    box-shadow: var(--shadow);
}
.stat-number { font-size: 2rem; font-weight: 800; color: var(--accent); }
.stat-label  { font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem; }

/* ── Voice Widget ── */
.voice-widget {
    background: linear-gradient(135deg, #1a2744 0%, #161B22 100%);
    border: 1px solid var(--primary);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    margin-bottom: 1rem;
}
.voice-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: linear-gradient(135deg, var(--primary), var(--primary-dk));
    color: white;
    border: none;
    border-radius: 50px;
    padding: 0.75rem 2rem;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    box-shadow: 0 4px 15px rgba(79,142,247,0.3);
}
.voice-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(79,142,247,0.5);
}
.recording-pulse {
    display: inline-block;
    width: 12px; height: 12px;
    background: var(--danger);
    border-radius: 50%;
    animation: pulse 1s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.5; transform: scale(1.3); }
}

/* ── Voice Gender Selector ── */
.gender-selector {
    display: flex;
    gap: 1rem;
    justify-content: center;
    margin: 1rem 0;
}
.gender-btn {
    flex: 1;
    padding: 0.8rem;
    border-radius: 10px;
    border: 2px solid var(--border);
    background: var(--bg3);
    color: var(--text);
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    text-align: center;
}
.gender-btn.active {
    border-color: var(--accent);
    background: rgba(34,211,165,0.1);
    color: var(--accent);
}
.gender-btn:hover {
    border-color: var(--primary);
    background: rgba(79,142,247,0.1);
}

/* ── Chat Bubbles ── */
.chat-user {
    background: linear-gradient(135deg, var(--primary-dk), var(--primary));
    color: white;
    border-radius: 16px 16px 4px 16px;
    padding: 0.8rem 1.2rem;
    margin: 0.4rem 0 0.4rem 3rem;
    max-width: 80%;
    float: right;
    clear: both;
    font-size: 0.95rem;
    box-shadow: 0 2px 12px rgba(79,142,247,0.2);
}
.chat-ai {
    background: var(--bg3);
    border: 1px solid var(--border);
    color: var(--text);
    border-radius: 16px 16px 16px 4px;
    padding: 0.8rem 1.2rem;
    margin: 0.4rem 3rem 0.4rem 0;
    max-width: 80%;
    float: left;
    clear: both;
    font-size: 0.95rem;
}
.chat-clear { clear: both; }
.chat-meta { font-size: 0.72rem; color: var(--text-muted); margin-top: 0.3rem; }

/* ── Usage Bar ── */
.usage-bar-track {
    background: var(--bg3);
    border-radius: 50px;
    height: 8px;
    overflow: hidden;
    margin: 0.4rem 0;
}
.usage-bar-fill {
    height: 100%;
    border-radius: 50px;
    background: linear-gradient(90deg, var(--accent), var(--primary));
    transition: width 0.5s ease;
}

/* ── Badges ── */
.badge {
    display: inline-block;
    padding: 0.2rem 0.65rem;
    border-radius: 50px;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.badge-green  { background: rgba(34,211,165,0.15); color: var(--accent); border: 1px solid rgba(34,211,165,0.3); }
.badge-blue   { background: rgba(79,142,247,0.15); color: var(--primary); border: 1px solid rgba(79,142,247,0.3); }
.badge-yellow { background: rgba(245,158,11,0.15); color: var(--accent2); border: 1px solid rgba(245,158,11,0.3); }
.badge-red    { background: rgba(239,68,68,0.15); color: var(--danger); border: 1px solid rgba(239,68,68,0.3); }

/* ── Login Page ── */
.login-container {
    max-width: 420px;
    margin: 3rem auto;
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2.5rem;
    box-shadow: var(--shadow);
}
.login-logo {
    text-align: center;
    font-size: 3rem;
    margin-bottom: 0.5rem;
}
.login-title {
    text-align: center;
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 0.3rem;
}
.login-sub {
    text-align: center;
    color: var(--text-muted);
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
}

/* ── Language Selector ── */
.lang-grid {
    display: flex;
    gap: 0.6rem;
    flex-wrap: wrap;
    margin: 0.5rem 0;
}
.lang-chip {
    padding: 0.4rem 0.9rem;
    border-radius: 50px;
    border: 1.5px solid var(--border);
    background: var(--bg3);
    color: var(--text-muted);
    font-size: 0.82rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s;
}
.lang-chip.active {
    border-color: var(--accent);
    background: rgba(34,211,165,0.1);
    color: var(--accent);
}

/* ── Dashboard Table ── */
.dash-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.88rem;
}
.dash-table th {
    background: var(--bg3);
    padding: 0.75rem 1rem;
    text-align: left;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    font-size: 0.72rem;
    letter-spacing: 0.05em;
    border-bottom: 1px solid var(--border);
}
.dash-table td {
    padding: 0.75rem 1rem;
    border-bottom: 1px solid rgba(48,54,61,0.5);
    color: var(--text);
}
.dash-table tr:hover td { background: rgba(79,142,247,0.05); }

/* ── Streamlit overrides ── */
.stTextInput > div > div > input,
.stSelectbox > div > div > select,
.stTextArea > div > div > textarea {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
    font-family: 'Outfit', sans-serif !important;
}
.stButton > button {
    background: linear-gradient(135deg, var(--primary), var(--primary-dk)) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(79,142,247,0.4) !important;
}
.stTabs [data-baseweb="tab"] {
    background: var(--bg2) !important;
    color: var(--text-muted) !important;
    border-radius: 8px 8px 0 0 !important;
    font-family: 'Outfit', sans-serif !important;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: var(--bg3) !important;
    color: var(--primary) !important;
}
.stAlert { border-radius: var(--radius) !important; }
div[data-testid="stMarkdownContainer"] p { color: var(--text) !important; }
label, .stSelectbox label, .stTextInput label { color: var(--text-muted) !important; font-weight: 500 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--primary); }

/* ── Divider ── */
hr { border-color: var(--border) !important; }

/* ── Audio hidden ── */
audio { display: none; }

/* ── Responsive ── */
@media (max-width: 640px) {
    .hero-title { font-size: 1.4rem; }
    .block-container { padding: 1rem !important; }
    .chat-user, .chat-ai { max-width: 92%; }
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# 4. DATA STORAGE (File-based for Streamlit Cloud)
# ═══════════════════════════════════════════════════════════════
DATA_FILE = "school_data.json"

def load_data():
    if Path(DATA_FILE).exists():
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return get_default_data()

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_default_data():
    return {
        "users": {
            "admin": {
                "password": hashlib.sha256("admin123".encode()).hexdigest(),
                "role": "teacher",
                "name": "Administrator",
                "class": "N/A",
                "usage_today": 0,
                "total_usage": 0,
                "last_active": "",
                "created": str(datetime.date.today())
            },
            "student1": {
                "password": hashlib.sha256("student123".encode()).hexdigest(),
                "role": "student",
                "name": "Demo Student",
                "class": "10",
                "usage_today": 0,
                "total_usage": 0,
                "last_active": "",
                "created": str(datetime.date.today())
            }
        },
        "settings": {
            "school_name": "School Name",
            "daily_limit": 30,
            "total_limit": 500
        },
        "logs": []
    }

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password, data):
    if username in data["users"]:
        if data["users"][username]["password"] == hash_password(password):
            return True
    return False

def log_interaction(data, username, query_type, subject=""):
    entry = {
        "user": username,
        "type": query_type,
        "subject": subject,
        "timestamp": str(datetime.datetime.now()),
        "date": str(datetime.date.today())
    }
    data["logs"].append(entry)
    # Update user stats
    if username in data["users"]:
        data["users"][username]["total_usage"] += 1
        data["users"][username]["last_active"] = str(datetime.datetime.now())
        today = str(datetime.date.today())
        last = data["users"][username].get("last_active_date", "")
        if last != today:
            data["users"][username]["usage_today"] = 0
            data["users"][username]["last_active_date"] = today
        data["users"][username]["usage_today"] += 1
    save_data(data)
    return data

def check_usage_limit(data, username):
    if username not in data["users"]:
        return False
    user = data["users"][username]
    if user["role"] == "teacher":
        return True  # No limit for teachers
    today = str(datetime.date.today())
    if user.get("last_active_date", "") != today:
        return True
    daily_limit = data["settings"]["daily_limit"]
    return user["usage_today"] < daily_limit

# ═══════════════════════════════════════════════════════════════
# 5. VOICE JAVASCRIPT - Web Speech API (Browser-native, accurate)
# ═══════════════════════════════════════════════════════════════
VOICE_JS = """
<script>
// ── Speech Recognition ──────────────────────────────────────
let recognition = null;
let isListening = false;

function getLangCode(lang) {
    const codes = { 'English': 'en-IN', 'Telugu': 'te-IN', 'Hindi': 'hi-IN', 'Urdu': 'ur-IN' };
    return codes[lang] || 'en-IN';
}

function initRecognition(lang) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        document.getElementById('voice-status').innerText = '⚠️ Speech recognition not supported in this browser. Use Chrome or Edge.';
        return null;
    }
    const rec = new SpeechRecognition();
    rec.lang = getLangCode(lang);
    rec.continuous = false;
    rec.interimResults = true;
    rec.maxAlternatives = 3;
    return rec;
}

function startListening(lang) {
    if (isListening) { stopListening(); return; }

    recognition = initRecognition(lang);
    if (!recognition) return;

    isListening = true;
    const btn = document.getElementById('voice-btn');
    const status = document.getElementById('voice-status');
    const transcript = document.getElementById('voice-transcript');

    if (btn) {
        btn.innerHTML = '<span class="recording-pulse"></span> Listening... (click to stop)';
        btn.style.background = 'linear-gradient(135deg, #EF4444, #DC2626)';
    }
    if (status) status.innerText = '🎙️ Speak now...';

    recognition.onresult = (event) => {
        let interim = '';
        let final_t = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
            const t = event.results[i][0].transcript;
            if (event.results[i].isFinal) { final_t += t; }
            else { interim += t; }
        }
        if (transcript) transcript.value = final_t || interim;
        if (status) status.innerText = final_t ? `✅ Heard: "${final_t}"` : `🎙️ ${interim}...`;
        if (final_t) {
            // Send to Streamlit via query param trick
            setTimeout(() => {
                document.getElementById('submit-voice').click();
            }, 500);
        }
    };

    recognition.onerror = (e) => {
        isListening = false;
        resetBtn();
        const msgs = {
            'no-speech': '🔇 No speech detected. Try again.',
            'audio-capture': '🎤 Microphone not found.',
            'not-allowed': '🚫 Microphone access denied. Please allow microphone.',
            'network': '🌐 Network error.'
        };
        if (status) status.innerText = msgs[e.error] || `Error: ${e.error}`;
    };

    recognition.onend = () => {
        isListening = false;
        resetBtn();
    };

    try { recognition.start(); }
    catch(e) { isListening = false; resetBtn(); }
}

function stopListening() {
    if (recognition) { recognition.stop(); }
    isListening = false;
    resetBtn();
}

function resetBtn() {
    const btn = document.getElementById('voice-btn');
    if (btn) {
        btn.innerHTML = '🎙️ Tap to Speak';
        btn.style.background = 'linear-gradient(135deg, #4F8EF7, #2563EB)';
    }
}

// ── Text to Speech ───────────────────────────────────────────
function speakText(text, gender, lang) {
    if (!window.speechSynthesis) return;
    window.speechSynthesis.cancel();

    const utter = new SpeechSynthesisUtterance(text);
    const langCode = {'English':'en-IN','Telugu':'te-IN','Hindi':'hi-IN','Urdu':'ur-PK'}[lang] || 'en-IN';
    utter.lang = langCode;
    utter.rate = 0.9;
    utter.pitch = gender === 'Female' ? 1.3 : 0.85;
    utter.volume = 1;

    // Try to pick matching voice
    const voices = window.speechSynthesis.getVoices();
    const preferred = voices.find(v =>
        v.lang.startsWith(langCode.split('-')[0]) &&
        (gender === 'Female' ? (v.name.includes('Female') || v.name.includes('f') || v.name.includes('Heera') || v.name.includes('Raveena')) :
                               (v.name.includes('Male') || v.name.includes('m') || v.name.includes('Hemant')))
    ) || voices.find(v => v.lang.startsWith(langCode.split('-')[0]));

    if (preferred) utter.voice = preferred;
    window.speechSynthesis.speak(utter);
}

// ── Auto-speak on new AI message ────────────────────────────
function autoSpeak(text, gender, lang) {
    // Remove markdown symbols for cleaner speech
    const clean = text.replace(/[#*_`>\\[\\]]/g, '').replace(/\\n+/g,' ').trim();
    speakText(clean.substring(0, 500), gender, lang);  // limit to 500 chars
}

// Stop speech
function stopSpeaking() {
    if (window.speechSynthesis) window.speechSynthesis.cancel();
}
</script>
"""

# ═══════════════════════════════════════════════════════════════
# 6. SYSTEM PROMPT
# ═══════════════════════════════════════════════════════════════
def build_system_prompt(school_name, student_name, student_class):
    return f"""
You are a **Professional AI Tutor from {school_name}**, specializing in Telangana State Board (SCERT) English Medium Curriculum for Academic Year 2025-26.

You are currently helping: **{student_name}** | Class: **{student_class}**

═══════════════════════════════════════════════════════════════
📚 KNOWLEDGE BASE & SCOPE
═══════════════════════════════════════════════════════════════

OFFICIAL SOURCE: SCERT Telangana e-Textbooks (https://scert.telangana.gov.in/)
Academic Year: 2025-26 | Medium: English Only | Classes: 1-10

SUBJECTS: Languages (English/Telugu/Hindi/Urdu/Sanskrit), Mathematics, Physical Science, Biological Science, Environmental Science, Social Studies, Computer Science

═══════════════════════════════════════════════════════════════
🎓 TEACHING STYLE - PROFESSIONAL + FRIENDLY + ANALOGIES
═══════════════════════════════════════════════════════════════

ALWAYS USE ANALOGIES:
• Science: "A plant is like a solar-powered kitchen - it uses sunlight to cook food"
• Math: "Algebra variables are like empty boxes waiting to be filled with numbers"
• History: "The Constitution is like the rulebook of a country, just like school has rules"
• Geography: "Latitude lines are like horizontal rungs on a ladder circling the Earth"
• Physics: "Electricity flows like water in pipes - more voltage = more pressure"
• Biology: "DNA is like a recipe book - it contains instructions to build every part of your body"

COMMUNICATION STYLE:
✅ Professional yet warm - like an experienced, caring teacher
✅ Start explanations with: "Great question! Let me explain [topic] from your Class [X] textbook..."
✅ Use "Think of it this way..." before every analogy
✅ End responses with: "Does this make sense? Would you like me to explain any part differently?"
✅ For complex topics, break into numbered steps
✅ Use encouraging phrases: "You're thinking in the right direction!", "Excellent observation!"

VOICE-FRIENDLY RESPONSES:
Since students may be listening via text-to-speech:
- Keep sentences clear and not too long
- Spell out formulas verbally: "six CO2 plus six H2O gives C6H12O6 plus six O2"
- Avoid excessive bullet points in main explanations

═══════════════════════════════════════════════════════════════
📋 CURRICULUM: 10th Social Studies (English Medium) 2025-26
═══════════════════════════════════════════════════════════════

Part I - Resources Development and Equity:
Ch1: India Relief Features (pp1-14) | Ch2: Ideas of Development (pp15-28)
Ch3: Production and Employment (pp29-44) | Ch4: Climate of India (pp45-58)
Ch5: Indian Rivers and Water Resources (pp59-71) | Ch6: The Population (pp72-87)
Ch7: Settlements-Migrations (pp88-102) | Ch8: Rampur A Village Economy (pp103-117)
Ch9: Globalisation (pp118-131) | Ch10: Food Security (pp132-145)
Ch11: Sustainable Development with Equity (pp146-162)

Part II - Contemporary World and India:
Ch12: World Between the World Wars 1914-1945 (pp163-186)
Ch13: National Liberation Movements in the Colonies (pp187-197)
Ch14: National Movement in India Partition and Independence 1939-1947 (pp198-211)
Ch15: The Making of Independent India's Constitution (pp212-228)
Ch16: Election Process in India (pp229-238)
Ch17: Independent India The First 30 years 1947-77 (pp239-253)
Ch18: Emerging Political Trends 1977 to 2000 (pp254-271)
Ch19: Post War World and India (pp272-287)
Ch20: Social Movements in Our Times (pp288-303)
Ch21: The Movement for the Formation of Telangana State (pp304-336)

═══════════════════════════════════════════════════════════════
📝 EXAM ANSWER FORMATS (SSC Board 2025-26)
═══════════════════════════════════════════════════════════════

1-mark: One precise sentence with key term
2-mark: Two clear points or one point with example  
4-mark: Definition + 3 explanation points + real example
8-mark: Introduction (2 lines) + 6 detailed points + conclusion (2 lines) + diagram note if needed

ALWAYS mention: "This is a [X]-mark topic in your board exam"

═══════════════════════════════════════════════════════════════
🚫 BOUNDARIES
═══════════════════════════════════════════════════════════════

NEVER: Answer non-SCERT Telangana topics | Give direct homework answers without teaching
NEVER: Use other board content | Discuss non-educational topics
ALWAYS: Teach the concept FIRST, then help solve | Reference chapter and page numbers
ALWAYS: Use Telangana examples (Hyderabad Metro, Charminar, Hussain Sagar, Bathukamma)

Your mission: Make every student feel confident and capable. You're not just answering questions — you're building young minds for a better Telangana! 🎓
"""

# ═══════════════════════════════════════════════════════════════
# 7. GROQ API CLIENT
# ═══════════════════════════════════════════════════════════════
# Support both .env (local) and Streamlit Cloud secrets
api_key = os.getenv("GROK-API-KEY") or st.secrets.get("GROK-API-KEY", None)
client = None
if api_key:
    client = Groq(api_key=api_key)

# ═══════════════════════════════════════════════════════════════
# 8. INITIALIZE SESSION STATE
# ═══════════════════════════════════════════════════════════════
defaults = {
    "logged_in": False,
    "username": "",
    "role": "",
    "user_name": "",
    "user_class": "",
    "messages": [],
    "voice_gender": "Female",
    "voice_lang": "English",
    "auto_speak": True,
    "school_data": None,
    "voice_transcript": "",
    "page": "login"
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

if st.session_state.school_data is None:
    st.session_state.school_data = load_data()

data = st.session_state.school_data

# ═══════════════════════════════════════════════════════════════
# 9. LOGIN PAGE
# ═══════════════════════════════════════════════════════════════
def show_login():
    st.markdown(VOICE_JS, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        school = data["settings"]["school_name"]
        st.markdown(f"""
        <div class="login-container">
            <div class="login-logo">🎓</div>
            <div class="login-title">{school} Smart Tutor</div>
            <div class="login-sub">Telangana State Board (SCERT) 2025-26<br>English Medium · Classes 1–10</div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("Sign In →", use_container_width=True)

            if submitted:
                if not api_key:
                    st.error("⚠️ API Key not found. Add GROK-API-KEY to your .env or Streamlit secrets.")
                elif authenticate(username, password, data):
                    user = data["users"][username]
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.role = user["role"]
                    st.session_state.user_name = user["name"]
                    st.session_state.user_class = user.get("class", "")
                    st.session_state.messages = []
                    st.session_state.page = "dashboard" if user["role"] == "teacher" else "chat"
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password.")

        st.markdown("""
        <div style='text-align:center; margin-top:1rem; color:var(--text-muted); font-size:0.8rem;'>
            Demo: <b>admin</b> / <b>admin123</b> &nbsp;|&nbsp; <b>student1</b> / <b>student123</b>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# 10. TEACHER DASHBOARD
# ═══════════════════════════════════════════════════════════════
def show_teacher_dashboard():
    school = data["settings"]["school_name"]

    st.markdown(f"""
    <div class="hero-banner">
        <div class="hero-title">📊 Teacher Dashboard</div>
        <div class="hero-sub">{school} · SCERT Telangana 2025-26 · Welcome, {st.session_state.user_name}</div>
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["📈 Overview", "👥 Students", "⚙️ Settings", "📝 Add Student"])

    # ── Overview ──────────────────────────────────────────────
    with tabs[0]:
        students = {u: d for u, d in data["users"].items() if d["role"] == "student"}
        today_logs = [l for l in data["logs"] if l.get("date") == str(datetime.date.today())]
        total_q = sum(d["total_usage"] for d in students.values())

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""<div class="stat-card">
                <div class="stat-number">{len(students)}</div>
                <div class="stat-label">Total Students</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="stat-card">
                <div class="stat-number">{len(today_logs)}</div>
                <div class="stat-label">Questions Today</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class="stat-card">
                <div class="stat-number">{total_q}</div>
                <div class="stat-label">Total Questions</div>
            </div>""", unsafe_allow_html=True)
        with c4:
            active = sum(1 for d in students.values() if d.get("last_active_date","") == str(datetime.date.today()))
            st.markdown(f"""<div class="stat-card">
                <div class="stat-number">{active}</div>
                <div class="stat-label">Active Today</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Recent activity
        st.markdown("<div class='card'><b>📋 Recent Activity (Last 20)</b></div>", unsafe_allow_html=True)
        recent = data["logs"][-20:][::-1]
        if recent:
            table_rows = ""
            for log in recent:
                badge = "badge-blue" if log.get("type") == "text" else "badge-green"
                icon = "⌨️" if log.get("type") == "text" else "🎙️"
                table_rows += f"""<tr>
                    <td>{log.get('user','—')}</td>
                    <td><span class='badge {badge}'>{icon} {log.get('type','—')}</span></td>
                    <td>{log.get('subject','—') or 'General'}</td>
                    <td style='color:var(--text-muted); font-size:0.8rem;'>{log.get('timestamp','—')[:16]}</td>
                </tr>"""
            st.markdown(f"""
            <table class='dash-table'>
                <thead><tr>
                    <th>Student</th><th>Type</th><th>Subject</th><th>Time</th>
                </tr></thead>
                <tbody>{table_rows}</tbody>
            </table>""", unsafe_allow_html=True)
        else:
            st.info("No activity recorded yet.")

    # ── Students ──────────────────────────────────────────────
    with tabs[1]:
        students = {u: d for u, d in data["users"].items() if d["role"] == "student"}
        daily_limit = data["settings"]["daily_limit"]

        if students:
            table_rows = ""
            for uname, udata in students.items():
                used = udata.get("usage_today", 0) if udata.get("last_active_date","") == str(datetime.date.today()) else 0
                pct = min(100, int(used / daily_limit * 100))
                color = "#22D3A5" if pct < 70 else "#F59E0B" if pct < 90 else "#EF4444"
                badge_cls = "badge-green" if pct < 70 else "badge-yellow" if pct < 90 else "badge-red"
                table_rows += f"""<tr>
                    <td><b>{udata.get('name','—')}</b><br><span style='color:var(--text-muted);font-size:0.78rem;'>{uname}</span></td>
                    <td>Class {udata.get('class','—')}</td>
                    <td>
                        <div style='display:flex; align-items:center; gap:0.5rem;'>
                            <div class='usage-bar-track' style='width:80px;'>
                                <div class='usage-bar-fill' style='width:{pct}%; background:{color};'></div>
                            </div>
                            <span class='badge {badge_cls}'>{used}/{daily_limit}</span>
                        </div>
                    </td>
                    <td>{udata.get('total_usage',0)}</td>
                    <td style='color:var(--text-muted);font-size:0.8rem;'>{str(udata.get('last_active','—'))[:16]}</td>
                </tr>"""
            st.markdown(f"""
            <table class='dash-table'>
                <thead><tr>
                    <th>Student</th><th>Class</th><th>Today's Usage</th><th>Total</th><th>Last Active</th>
                </tr></thead>
                <tbody>{table_rows}</tbody>
            </table>""", unsafe_allow_html=True)
        else:
            st.info("No students added yet. Use the 'Add Student' tab.")

    # ── Settings ──────────────────────────────────────────────
    with tabs[2]:
        st.markdown("<div class='card'><b>⚙️ School Settings</b></div>", unsafe_allow_html=True)
        with st.form("settings_form"):
            new_school = st.text_input("School Name", value=data["settings"]["school_name"])
            new_limit = st.number_input("Daily Question Limit per Student", min_value=5, max_value=200,
                                         value=data["settings"]["daily_limit"])
            if st.form_submit_button("💾 Save Settings", use_container_width=True):
                data["settings"]["school_name"] = new_school
                data["settings"]["daily_limit"] = int(new_limit)
                st.session_state.school_data = data
                save_data(data)
                st.success("✅ Settings saved!")
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='card'><b>🔑 Change Admin Password</b></div>", unsafe_allow_html=True)
        with st.form("pw_form"):
            curr_pw = st.text_input("Current Password", type="password")
            new_pw = st.text_input("New Password", type="password")
            conf_pw = st.text_input("Confirm New Password", type="password")
            if st.form_submit_button("🔒 Update Password", use_container_width=True):
                if hash_password(curr_pw) != data["users"][st.session_state.username]["password"]:
                    st.error("❌ Current password incorrect.")
                elif new_pw != conf_pw:
                    st.error("❌ Passwords do not match.")
                elif len(new_pw) < 6:
                    st.error("❌ Password must be at least 6 characters.")
                else:
                    data["users"][st.session_state.username]["password"] = hash_password(new_pw)
                    save_data(data)
                    st.success("✅ Password updated!")

    # ── Add Student ───────────────────────────────────────────
    with tabs[3]:
        st.markdown("<div class='card'><b>➕ Add New Student</b></div>", unsafe_allow_html=True)
        with st.form("add_student_form"):
            col_a, col_b = st.columns(2)
            with col_a:
                new_uname = st.text_input("Username (login ID)", placeholder="e.g. ravi2025")
                new_name = st.text_input("Full Name", placeholder="e.g. Ravi Kumar")
            with col_b:
                new_class = st.selectbox("Class", ["1","2","3","4","5","6","7","8","9","10"])
                new_pw_s = st.text_input("Password", type="password", placeholder="Min 6 chars")

            if st.form_submit_button("➕ Add Student", use_container_width=True):
                if not new_uname or not new_name or not new_pw_s:
                    st.error("❌ Please fill all fields.")
                elif new_uname in data["users"]:
                    st.error("❌ Username already exists.")
                elif len(new_pw_s) < 6:
                    st.error("❌ Password must be at least 6 characters.")
                else:
                    data["users"][new_uname] = {
                        "password": hash_password(new_pw_s),
                        "role": "student",
                        "name": new_name,
                        "class": new_class,
                        "usage_today": 0,
                        "total_usage": 0,
                        "last_active": "",
                        "created": str(datetime.date.today())
                    }
                    save_data(data)
                    st.session_state.school_data = data
                    st.success(f"✅ Student **{new_name}** added! Username: `{new_uname}`")

# ═══════════════════════════════════════════════════════════════
# 11. STUDENT CHAT PAGE
# ═══════════════════════════════════════════════════════════════
def show_chat():
    school = data["settings"]["school_name"]
    student_name = st.session_state.user_name
    student_class = st.session_state.user_class
    username = st.session_state.username
    daily_limit = data["settings"]["daily_limit"]

    # Inject voice JS
    st.markdown(VOICE_JS, unsafe_allow_html=True)

    # ── Sidebar ──────────────────────────────────────────────
    with st.sidebar:
        st.markdown(f"<div style='text-align:center; padding:1rem 0;'><div style='font-size:2.5rem;'>🎓</div><div style='font-weight:700; font-size:1.1rem;'>{school}</div><div style='color:var(--text-muted); font-size:0.82rem;'>Smart Tutor · 2025-26</div></div>", unsafe_allow_html=True)
        st.divider()

        user = data["users"].get(username, {})
        used_today = user.get("usage_today", 0) if user.get("last_active_date","") == str(datetime.date.today()) else 0
        pct = min(100, int(used_today / daily_limit * 100))
        bar_color = "#22D3A5" if pct < 70 else "#F59E0B" if pct < 90 else "#EF4444"

        st.markdown(f"""
        <div class='card'>
            <div style='font-size:0.8rem; color:var(--text-muted); margin-bottom:0.5rem;'>👤 STUDENT</div>
            <div style='font-weight:600;'>{student_name}</div>
            <div style='color:var(--text-muted); font-size:0.82rem;'>Class {student_class} · English Medium</div>
            <div style='margin-top:0.8rem; font-size:0.8rem; color:var(--text-muted);'>Daily Usage: {used_today}/{daily_limit}</div>
            <div class='usage-bar-track' style='margin-top:0.3rem;'>
                <div class='usage-bar-fill' style='width:{pct}%; background:{bar_color};'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**🔊 Voice Settings**")

        # Voice Gender
        st.markdown("**Voice:**")
        gender_col1, gender_col2 = st.columns(2)
        with gender_col1:
            female_active = "active" if st.session_state.voice_gender == "Female" else ""
            if st.button("👩 Female", key="female_btn", use_container_width=True):
                st.session_state.voice_gender = "Female"
                st.rerun()
        with gender_col2:
            if st.button("👨 Male", key="male_btn", use_container_width=True):
                st.session_state.voice_gender = "Male"
                st.rerun()

        st.markdown(f"*Selected: **{st.session_state.voice_gender}***")

        # Voice Language
        voice_lang = st.selectbox(
            "🗣️ Voice Language",
            ["English", "Telugu", "Hindi", "Urdu"],
            index=["English", "Telugu", "Hindi", "Urdu"].index(st.session_state.voice_lang)
        )
        if voice_lang != st.session_state.voice_lang:
            st.session_state.voice_lang = voice_lang
            st.rerun()

        # Auto-speak toggle
        auto_speak = st.toggle("📢 Auto-speak Responses", value=st.session_state.auto_speak)
        if auto_speak != st.session_state.auto_speak:
            st.session_state.auto_speak = auto_speak
            st.rerun()

        st.divider()
        st.markdown("""
        <div style='font-size:0.78rem; color:var(--text-muted);'>
        📚 <b>Try asking:</b><br>
        • Explain Ch1 Social Studies<br>
        • How to solve quadratic equations?<br>
        • What is photosynthesis?<br>
        • Explain democracy<br>
        • Climate of India summary
        </div>
        """, unsafe_allow_html=True)
        st.divider()

        if st.button("🚪 Logout", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    # ── Main Chat Area ────────────────────────────────────────
    used_today = data["users"].get(username, {}).get("usage_today", 0) if data["users"].get(username, {}).get("last_active_date","") == str(datetime.date.today()) else 0
    pct_main = min(100, int(used_today / daily_limit * 100))
    badge_cls = "badge-green" if pct_main < 70 else "badge-yellow" if pct_main < 90 else "badge-red"

    st.markdown(f"""
    <div class="hero-banner">
        <div style='display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem;'>
            <div>
                <div class="hero-title">🎓 {school} Smart Tutor</div>
                <div class="hero-sub">Hello {student_name}! · Class {student_class} · SCERT Telangana 2025-26</div>
            </div>
            <div style='text-align:right;'>
                <span class='badge {badge_cls}'>📊 {used_today}/{daily_limit} today</span><br>
                <span style='font-size:0.78rem; color:var(--text-muted); margin-top:0.3rem; display:block;'>🔊 {st.session_state.voice_gender} · {st.session_state.voice_lang}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Usage limit warning
    if not check_usage_limit(data, username):
        st.markdown(f"""
        <div style='background:rgba(239,68,68,0.1); border:1px solid #EF4444; border-radius:12px; padding:1rem; margin-bottom:1rem; text-align:center;'>
            <div style='font-size:1.5rem;'>⏸️</div>
            <div style='font-weight:700; color:#EF4444;'>Daily Limit Reached</div>
            <div style='color:var(--text-muted); font-size:0.88rem;'>You've used all {daily_limit} questions for today. Come back tomorrow!</div>
        </div>""", unsafe_allow_html=True)

    # ── Voice Widget ──────────────────────────────────────────
    with st.expander("🎙️ Voice Input", expanded=False):
        st.markdown(f"""
        <div class='voice-widget'>
            <div style='font-size:0.85rem; color:var(--text-muted); margin-bottom:1rem;'>
                🔊 Voice: <b>{st.session_state.voice_gender}</b> · Language: <b>{st.session_state.voice_lang}</b>
            </div>
            <button class='voice-btn' id='voice-btn'
                onclick='startListening("{st.session_state.voice_lang}")'>
                🎙️ Tap to Speak
            </button>
            <div id='voice-status' style='margin-top:0.75rem; color:var(--text-muted); font-size:0.85rem;'>
                Press the button and speak your question clearly
            </div>
            <div style='margin-top:0.5rem; font-size:0.75rem; color:var(--text-muted);'>
                ✅ Works best in Chrome or Edge browser · Allow microphone access
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Hidden transcript area + submit
        voice_col1, voice_col2 = st.columns([4, 1])
        with voice_col1:
            voice_text = st.text_input(
                "Voice transcript (editable):",
                value=st.session_state.get("voice_transcript", ""),
                key="voice_input_field",
                placeholder="Your spoken text appears here...",
                label_visibility="collapsed"
            )
        with voice_col2:
            submit_voice = st.button("📤 Send", key="submit_voice_btn", use_container_width=True)

        if submit_voice and voice_text.strip():
            st.session_state.voice_transcript = ""
            process_message(voice_text.strip(), "voice", data, username, student_name, student_class, school)
            st.rerun()

    # ── Chat History ──────────────────────────────────────────
    chat_container = st.container()
    with chat_container:
        if not st.session_state.messages:
            st.markdown(f"""
            <div style='text-align:center; padding:2rem; color:var(--text-muted);'>
                <div style='font-size:3rem; margin-bottom:0.5rem;'>📚</div>
                <div style='font-size:1.1rem; font-weight:600; color:var(--text);'>Ready to learn, {student_name}!</div>
                <div style='font-size:0.88rem; margin-top:0.5rem;'>Ask any question from your SCERT textbook below</div>
            </div>""", unsafe_allow_html=True)
        else:
            for i, msg in enumerate(st.session_state.messages):
                if msg["role"] == "user":
                    icon = "🎙️" if msg.get("type") == "voice" else "⌨️"
                    st.markdown(f"""
                    <div class='chat-user'>{icon} {msg['content']}<div class='chat-meta'>{msg.get('time','')}</div></div>
                    <div class='chat-clear'></div>""", unsafe_allow_html=True)
                elif msg["role"] == "assistant":
                    speak_js = ""
                    if i == len(st.session_state.messages) - 1 and st.session_state.auto_speak:
                        safe = msg['content'].replace("'", "\\'").replace('"', '\\"').replace('\n', ' ')[:500]
                        speak_js = f"<script>setTimeout(()=>autoSpeak('{safe}','{st.session_state.voice_gender}','{st.session_state.voice_lang}'),300);</script>"
                    st.markdown(f"""
                    <div class='chat-ai'>🎓 {msg['content']}
                        <div class='chat-meta' style='display:flex; gap:0.5rem; align-items:center; margin-top:0.4rem;'>
                            <span>{msg.get('time','')}</span>
                            <button onclick='speakText("{msg["content"][:300].replace(chr(39),chr(34)).replace(chr(10)," ")}","{st.session_state.voice_gender}","{st.session_state.voice_lang}")'
                                style='background:none; border:1px solid var(--border); color:var(--text-muted); border-radius:4px; padding:0.1rem 0.4rem; font-size:0.7rem; cursor:pointer;'>🔊</span>
                            <button onclick='stopSpeaking()'
                                style='background:none; border:1px solid var(--border); color:var(--text-muted); border-radius:4px; padding:0.1rem 0.4rem; font-size:0.7rem; cursor:pointer;'>⏹</button>
                        </div>
                    </div>
                    <div class='chat-clear'></div>{speak_js}""", unsafe_allow_html=True)

    # ── Text Input ────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)

    if check_usage_limit(data, username):
        with st.form("chat_form", clear_on_submit=True):
            col_inp, col_btn = st.columns([5, 1])
            with col_inp:
                user_input = st.text_input(
                    "Ask your question:",
                    placeholder=f"Type your question here... (Class {student_class} · English Medium)",
                    label_visibility="collapsed"
                )
            with col_btn:
                send = st.form_submit_button("Send ➤", use_container_width=True)

            if send and user_input.strip():
                process_message(user_input.strip(), "text", data, username, student_name, student_class, school)
                st.rerun()
    else:
        st.info(f"⏸️ Daily limit of {daily_limit} questions reached. See you tomorrow!")

    # Footer
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='text-align:center; color:var(--text-muted); font-size:0.75rem; padding:0.5rem 0;'>
        🎓 Powered by AI9Campus &nbsp;|&nbsp; SCERT Telangana English Medium 2025-26 &nbsp;|&nbsp;
        Always cross-verify with your textbook and teacher
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# 12. MESSAGE PROCESSOR
# ═══════════════════════════════════════════════════════════════
def process_message(user_text, msg_type, data, username, student_name, student_class, school):
    if not client:
        st.error("⚠️ API Key not found. Please check your .env file.")
        return

    now = datetime.datetime.now().strftime("%I:%M %p")

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_text,
        "type": msg_type,
        "time": now
    })

    # Build message list for API (without custom fields)
    system_prompt = build_system_prompt(school, student_name, student_class)
    api_messages = [{"role": "system", "content": system_prompt}]
    for m in st.session_state.messages:
        if m["role"] in ("user", "assistant"):
            api_messages.append({"role": m["role"], "content": m["content"]})

    try:
        response = client.chat.completions.create(
            model="moonshotai/kimi-k2-instruct-0905",
            messages=api_messages,
            max_completion_tokens=4096,
            temperature=0.6,
            top_p=0.9
        )
        answer = response.choices[0].message.content or "I apologize, I couldn't generate a response. Please try again."
    except Exception as e:
        answer = f"⚠️ An error occurred: {str(e)}\n\nPlease check your API key and internet connection."

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "time": datetime.datetime.now().strftime("%I:%M %p")
    })

    # Log interaction
    st.session_state.school_data = log_interaction(
        st.session_state.school_data,
        username,
        msg_type,
        user_text[:50]
    )

# ═══════════════════════════════════════════════════════════════
# 13. MAIN ROUTER
# ═══════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    show_login()
elif st.session_state.role == "teacher":
    # Teacher sidebar logout
    with st.sidebar:
        st.markdown(f"<div style='padding:1rem 0; text-align:center;'><div style='font-size:2rem;'>👩‍🏫</div><div style='font-weight:700;'>{st.session_state.user_name}</div><div style='color:var(--text-muted); font-size:0.82rem;'>Teacher · Admin</div></div>", unsafe_allow_html=True)
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()
    show_teacher_dashboard()
else:
    show_chat()
