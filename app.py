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
# 5. INPUT + TTS COMPONENTS
#    TEXT: st.chat_input() — native Streamlit, zero JS bridge needed
#    VOICE: components.html mic → window.parent.location ?vt=... → query_params
#    TTS:  components.html one-way audio output (no bridge needed)
# ═══════════════════════════════════════════════════════════════
import streamlit.components.v1 as components
import re as _re

def strip_md_for_tts(text):
    """Strip markdown symbols so TTS reads clean spoken text."""
    t = _re.sub(r'\*{1,3}(.*?)\*{1,3}', r'\1', text, flags=_re.DOTALL)
    t = _re.sub(r'#{1,6}\s*', '', t)
    t = _re.sub(r'`{1,3}.*?`{1,3}', '', t, flags=_re.DOTALL)
    t = _re.sub(r'[-•►▸]\s+', '', t)
    t = _re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', t)
    t = _re.sub(r'[|]', ' ', t)
    t = _re.sub(r'\s{2,}', ' ', t)
    return t.strip()

def get_mic_component_html(lang_code, countdown_sec=6):
    """
    Mic-only component that communicates via URL query param.
    When voice transcript is ready it does:
      window.parent.location.href = base_url + '?vt=' + encodeURIComponent(text)
    This is cross-origin safe — you CAN navigate window.parent even cross-origin.
    Streamlit detects the URL change and reruns, Python reads st.query_params['vt'].
    """
    lang_map = {"English":"en-IN","Telugu":"te-IN","Hindi":"hi-IN","Urdu":"ur-PK"}
    lang     = lang_map.get(lang_code, "en-IN")
    return f"""<!DOCTYPE html><html><head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{{box-sizing:border-box;margin:0;padding:0;font-family:'Segoe UI',sans-serif;}}
body{{background:transparent;display:flex;align-items:center;justify-content:center;padding:6px;}}
.mic-wrap{{display:flex;align-items:center;gap:10px;}}
.ibtn{{
  width:46px;height:46px;border-radius:50%;border:none;
  display:flex;align-items:center;justify-content:center;
  cursor:pointer;font-size:1.3rem;transition:all 0.18s;
  -webkit-tap-highlight-color:transparent;
}}
.ibtn:active{{transform:scale(0.88);}}
.mic-idle{{background:#2D333B;color:#8b949e;border:2px solid #30363D;}}
.mic-idle:hover{{background:#3D444D;color:#e6edf3;}}
.mic-on{{background:linear-gradient(135deg,#EF4444,#DC2626);color:white;border:none;
  animation:mpulse 0.9s infinite;}}
@keyframes mpulse{{0%,100%{{transform:scale(1);box-shadow:0 0 0 0 rgba(239,68,68,0.5);}}
  50%{{transform:scale(1.08);box-shadow:0 0 0 8px rgba(239,68,68,0);}}}}
.info{{font-size:0.78rem;color:#8b949e;max-width:200px;line-height:1.3;}}
.info b{{color:#22D3A5;}}
.cd{{display:none;background:rgba(34,211,165,0.15);border:1px solid #22D3A5;
  border-radius:50px;padding:2px 10px;font-size:0.75rem;color:#22D3A5;font-weight:700;}}
.cd.on{{display:inline-block;}}
.ldot{{display:inline-block;width:7px;height:7px;background:#EF4444;border-radius:50%;
  animation:dp 0.9s infinite;vertical-align:middle;margin-right:4px;}}
@keyframes dp{{0%,100%{{opacity:1;}}50%{{opacity:0.2;}}}}
</style></head><body>
<div class="mic-wrap">
  <button class="ibtn mic-idle" id="micBtn" onclick="toggleMic()" title="Tap to speak">🎙️</button>
  <span class="cd" id="cd">{countdown_sec}s</span>
  <div class="info" id="info">Tap 🎙️ to speak in {lang_code}</div>
</div>
<script>
var SR      = window.SpeechRecognition || window.webkitSpeechRecognition;
var rec     = null;
var isListen= false;
var cdTimer = null;
var cdLeft  = {countdown_sec};
var LANG    = '{lang}';
var micBtn  = document.getElementById('micBtn');
var cdEl    = document.getElementById('cd');
var infoEl  = document.getElementById('info');

function setInfo(html){{ infoEl.innerHTML=html; }}

function toggleMic(){{
  if(!SR){{ setInfo('⚠️ Use <b>Chrome</b> browser'); return; }}
  if(isListen){{ stopMic(); }} else {{ startMic(); }}
}}

function startMic(){{
  if(cdTimer){{ clearInterval(cdTimer); cdTimer=null; cdEl.className='cd'; }}
  rec = new SR();
  rec.lang=LANG; rec.continuous=false; rec.interimResults=true; rec.maxAlternatives=3;
  rec.onstart=function(){{
    isListen=true;
    micBtn.className='ibtn mic-on'; micBtn.innerHTML='⏹';
    setInfo('<span class="ldot"></span>Listening...');
  }};
  rec.onresult=function(e){{
    var interim='',final='';
    for(var i=e.resultIndex;i<e.results.length;i++){{
      var t=e.results[i][0].transcript;
      if(e.results[i].isFinal){{final+=t;}}else{{interim+=t;}}
    }}
    if(final){{
      setInfo('✅ <b>'+final+'</b>');
      sendToStreamlit(final);
    }} else {{
      setInfo('🎙️ '+interim);
    }}
  }};
  rec.onerror=function(e){{
    isListen=false; resetMic();
    var m={{'no-speech':'🔇 No speech. Try again.','not-allowed':'🚫 Allow mic in browser.','audio-capture':'🎤 No mic found.'}};
    setInfo(m[e.error]||'Error: '+e.error);
  }};
  rec.onend=function(){{
    isListen=false; resetMic();
  }};
  try{{rec.start();}}catch(ex){{setInfo('Mic error: '+ex.message);isListen=false;resetMic();}}
}}

function stopMic(){{
  if(rec){{try{{rec.stop();}}catch(e){{}}}}
  isListen=false; resetMic();
}}

function resetMic(){{
  micBtn.className='ibtn mic-idle'; micBtn.innerHTML='🎙️';
}}

function sendToStreamlit(text){{
  // ── THE RELIABLE CROSS-ORIGIN BRIDGE ──
  // window.parent.location navigation IS allowed cross-origin.
  // Changing the URL triggers a Streamlit rerun.
  // Python reads st.query_params['vt'] to get the transcript.
  try{{
    var base = window.parent.location.href.split('?')[0].split('#')[0];
    window.parent.location.href = base + '?vt=' + encodeURIComponent(text);
  }} catch(ex) {{
    // Last resort: postMessage (may not trigger rerun but worth trying)
    window.parent.postMessage({{type:'vt',text:text}},'*');
    setInfo('⚠️ Could not send. Try typed input.');
  }}
}}
</script></body></html>"""

def get_tts_component_html(lang_code, gender, speak_text):
    """
    TTS-only component. Purely one-way: Python pushes text → JS speaks it.
    No bridge needed. Safe on all origins.
    """
    lang_map  = {"English":"en-IN","Telugu":"te-IN","Hindi":"hi-IN","Urdu":"ur-PK"}
    lang      = lang_map.get(lang_code, "en-IN")
    pitch     = "1.3" if gender == "Female" else "0.8"
    safe_spk  = (speak_text
                 .replace("\\", "\\\\")
                 .replace("'", "\\\'")
                 .replace("\r", " ")
                 .replace("\n", " ")
                 .replace("`", "'"))

    return f"""<!DOCTYPE html><html><head>
<style>
*{{box-sizing:border-box;margin:0;padding:0;font-family:'Segoe UI',sans-serif;}}
body{{background:transparent;display:flex;align-items:center;padding:4px 8px;}}
.tts-row{{display:flex;align-items:center;gap:8px;width:100%;}}
.wave{{display:none;align-items:flex-end;gap:2px;height:16px;}}
.wave.on{{display:flex;}}
.wb{{width:3px;border-radius:2px;animation:wb 0.65s infinite;}}
.wb:nth-child(1){{height:5px;background:#22D3A5;animation-delay:0s;}}
.wb:nth-child(2){{height:12px;background:#4F8EF7;animation-delay:0.1s;}}
.wb:nth-child(3){{height:8px;background:#22D3A5;animation-delay:0.2s;}}
.wb:nth-child(4){{height:14px;background:#F59E0B;animation-delay:0.3s;}}
.wb:nth-child(5){{height:6px;background:#22D3A5;animation-delay:0.4s;}}
@keyframes wb{{0%,100%{{transform:scaleY(0.3);}}50%{{transform:scaleY(1.1);}}}}
.info{{font-size:0.78rem;color:#8b949e;flex:1;}}
.info.spk{{color:#fbbf24;font-weight:600;}}
.stop{{background:#2D333B;border:1px solid #30363D;color:#F59E0B;
  border-radius:50px;padding:3px 12px;font-size:0.75rem;cursor:pointer;display:none;}}
.stop:hover{{background:#3D444D;}}
</style></head><body>
<div class="tts-row">
  <div class="wave" id="wave">
    <div class="wb"></div><div class="wb"></div><div class="wb"></div>
    <div class="wb"></div><div class="wb"></div>
  </div>
  <div class="info" id="info"></div>
  <button class="stop" id="stopBtn" onclick="stopSpeak()">⏹ Stop</button>
</div>
<script>
var SPEAK_TEXT = '{safe_spk}';
var LANG  = '{lang}';
var PITCH = {pitch};
var ttsQueue   = [];
var ttsRunning = false;
var wave   = document.getElementById('wave');
var info   = document.getElementById('info');
var stopBtn= document.getElementById('stopBtn');

function chunkText(text){{
  var parts = text.split(/(?<=[।.!?])\s+|(?<=\n)/);
  var out=[]; var buf='';
  for(var i=0;i<parts.length;i++){{
    var s=parts[i].trim();
    if(!s) continue;
    if((buf+' '+s).trim().length > 200){{
      if(buf) out.push(buf.trim());
      buf=s;
    }} else {{ buf=(buf+' '+s).trim(); }}
  }}
  if(buf) out.push(buf.trim());
  return out.length ? out : [text];
}}

function pickVoice(voices,lang,gender){{
  var base=lang.split('-')[0].toLowerCase();
  var fem=['heera','raveena','lekha','aditi','swara','female','zira','susan','sunali'];
  var mal=['hemant','rajan','kalpana','male','david','mark'];
  var gnames=(gender==='Female')?fem:mal;
  for(var i=0;i<voices.length;i++){{
    var v=voices[i]; var n=v.name.toLowerCase();
    if(v.lang.toLowerCase().indexOf(base)===0)
      for(var j=0;j<gnames.length;j++) if(n.indexOf(gnames[j])>=0) return v;
  }}
  for(var i=0;i<voices.length;i++)
    if(voices[i].lang.toLowerCase().indexOf(base)===0) return voices[i];
  var fb= lang==='te-IN'?['te','hi','en']:lang==='ur-PK'?['ur','hi','en']:lang==='hi-IN'?['hi','en']:['en'];
  for(var f=0;f<fb.length;f++)
    for(var i=0;i<voices.length;i++)
      if(voices[i].lang.toLowerCase().indexOf(fb[f])===0) return voices[i];
  return null;
}}

function showSpeaking(){{
  wave.className='wave on'; info.className='info spk';
  info.innerText='🔊 Reading response aloud...';
  stopBtn.style.display='inline-block';
}}
function clearUI(){{
  wave.className='wave'; info.className='info';
  info.innerText=''; stopBtn.style.display='none';
}}

function speakNext(){{
  if(ttsRunning||ttsQueue.length===0){{ if(!ttsRunning)clearUI(); return; }}
  ttsRunning=true;
  var chunk=ttsQueue.shift();
  var u=new SpeechSynthesisUtterance(chunk);
  u.lang=LANG; u.rate=0.87; u.pitch=PITCH; u.volume=1.0;
  var voices=window.speechSynthesis.getVoices();
  var v=pickVoice(voices,LANG,'{"Female" if gender=="Female" else "Male"}');
  if(v) u.voice=v;
  showSpeaking();
  u.onend=function(){{
    ttsRunning=false;
    if(ttsQueue.length>0) setTimeout(speakNext,100);
    else clearUI();
  }};
  u.onerror=function(){{
    ttsRunning=false;
    if(ttsQueue.length>0) setTimeout(speakNext,100);
    else clearUI();
  }};
  // Chrome 15s cutoff fix
  var ka=setInterval(function(){{
    if(!window.speechSynthesis.speaking){{clearInterval(ka);return;}}
    window.speechSynthesis.pause(); window.speechSynthesis.resume();
  }},11000);
  window.speechSynthesis.speak(u);
}}

function doSpeak(text){{
  if(!window.speechSynthesis||!text||text.trim().length<2) return;
  window.speechSynthesis.cancel();
  ttsQueue=chunkText(text); ttsRunning=false;
  var voices=window.speechSynthesis.getVoices();
  if(voices.length===0){{ window.speechSynthesis.onvoiceschanged=function(){{setTimeout(speakNext,100);}}; }}
  else{{ setTimeout(speakNext,200); }}
}}

function stopSpeak(){{
  ttsQueue=[]; ttsRunning=false;
  if(window.speechSynthesis) window.speechSynthesis.cancel();
  clearUI();
}}

// Auto-speak on load
if(SPEAK_TEXT && SPEAK_TEXT.trim().length>2){{
  setTimeout(function(){{doSpeak(SPEAK_TEXT);}},600);
}}
</script></body></html>"""

# ═══════════════════════════════════════════════════════════════
# 6. SYSTEM PROMPT
# ═══════════════════════════════════════════════════════════════
def build_system_prompt(school_name, student_name, student_class):
    return f"""
You are a **Professional AI Tutor from {school_name}**, specializing in Telangana State Board (SCERT) English Medium Curriculum for Academic Year 2025-26.

You are currently helping: **{student_name}** | Class: **{student_class}**

═══════════════════════════════════════════════════════════════
🗣️ LANGUAGE & COMMUNICATION STYLE — STRICTLY FOLLOW
═══════════════════════════════════════════════════════════════

ENGLISH RESPONSES — 100% INDIAN SLANG STYLE (MANDATORY):
You MUST speak like a warm, friendly Indian teacher from Telangana.
Use these Indian English expressions naturally:
- "Arey yaar, this is very simple only!"
- "See na, this concept is like this only..."
- "Bhai/Behen, listen carefully..."
- "Accha, so what happens is..."
- "Ekdum right! You got it!"
- "Arre wah! Brilliant thinking!"
- "Chalo, let us understand step by step..."
- "What to say, this formula is superb only!"
- "No tension, I will explain properly..."
- "Suno carefully, this is important for exam!"
- "Haan haan, good question asked!"
- "Basically what happens is na..."
- "Got it na? Simple only it is!"
STRICTLY FORBIDDEN: Western/American/British slang like "Hey guys", "Awesome sauce", "That's totally rad", "Oh snap", "Dude" (western style). Use ONLY Indian style English.

TELUGU MEDIUM (if student asks in Telugu):
Respond fully in Telugu script. Example: "అరేయ్, ఈ అంశం చాలా సులభంగా ఉంది. చూడండి..."

HINDI MEDIUM (if student asks in Hindi):
Respond fully in Hindi. Example: "अरे यार, यह बिल्कुल आसान है। देखो..."

URDU MEDIUM (if student asks in Urdu):
Respond fully in Urdu. Example: "ارے بھائی، یہ بالکل آسان ہے۔ دیکھو..."

═══════════════════════════════════════════════════════════════
🔊 VOICE/TTS FRIENDLY FORMAT (MANDATORY)
═══════════════════════════════════════════════════════════════

Your responses will be READ ALOUD by text-to-speech — EVERY word, number, symbol must be spelled out clearly:
- Write numbers as words when in sentences: "six carbon dioxide molecules" not "6 CO2"
- Spell formulas verbally: "H 2 O is water", "a squared plus b squared equals c squared"
- NO markdown symbols in explanations: no **, no #, no bullets with -, no > arrows
- Use numbered steps: "Step 1... Step 2..." for TTS readability
- Keep sentences under 25 words each for smooth audio reading
- Avoid abbreviations — say "Chapter" not "Ch", "page" not "pp"
- For fractions say: "3 by 4" not "3/4"

═══════════════════════════════════════════════════════════════
📚 KNOWLEDGE BASE & SCOPE
═══════════════════════════════════════════════════════════════

OFFICIAL SOURCE: SCERT Telangana e-Textbooks (https://scert.telangana.gov.in/)
Academic Year: 2025-26 | Medium: English/Telugu/Hindi/Urdu | Classes: 1-10

SUBJECTS: Languages, Mathematics, Physical Science, Biological Science, Environmental Science, Social Studies, Computer Science

═══════════════════════════════════════════════════════════════
🎓 TEACHING STYLE — ALWAYS USE ANALOGIES
═══════════════════════════════════════════════════════════════

Start with: "Arey, great question! Let me explain [topic] from your Class [X] textbook..."
Use: "Think of it this way na..." before every analogy
End with: "Got it na? Or shall I explain in different way?"
Use encouraging phrases: "Ekdum sahi! You are on right track!", "Arre wah, excellent thinking!"

Science analogy: "A plant is like a solar-powered kitchen na, it uses sunlight to cook food only!"
Math analogy: "Algebra variables are like empty dabba boxes waiting to be filled with numbers!"
History analogy: "Constitution is like school rulebook only, but for whole country!"

═══════════════════════════════════════════════════════════════
📋 CLASS 10 SOCIAL STUDIES CURRICULUM (SCERT 2025-26)
═══════════════════════════════════════════════════════════════

Part 1: Chapter 1 India Relief Features, Chapter 2 Ideas of Development, Chapter 3 Production and Employment, Chapter 4 Climate of India, Chapter 5 Indian Rivers and Water Resources, Chapter 6 The Population, Chapter 7 Settlements and Migrations, Chapter 8 Rampur A Village Economy, Chapter 9 Globalisation, Chapter 10 Food Security, Chapter 11 Sustainable Development with Equity

Part 2: Chapter 12 World Between the World Wars 1914 to 1945, Chapter 13 National Liberation Movements in the Colonies, Chapter 14 National Movement in India Partition and Independence, Chapter 15 The Making of Independent India Constitution, Chapter 16 Election Process in India, Chapter 17 Independent India The First 30 years, Chapter 18 Emerging Political Trends 1977 to 2000, Chapter 19 Post War World and India, Chapter 20 Social Movements in Our Times, Chapter 21 The Movement for the Formation of Telangana State

═══════════════════════════════════════════════════════════════
📝 EXAM ANSWER FORMATS (SSC Board 2025-26)
═══════════════════════════════════════════════════════════════

1 mark: One precise sentence with key term
2 marks: Two clear points or one point with example
4 marks: Definition plus 3 explanation points plus real example
8 marks: Introduction 2 lines, then 6 detailed points, then conclusion 2 lines, mention diagram if needed

ALWAYS say: "This is a [X] mark topic in your board exam, so remember it well!"

═══════════════════════════════════════════════════════════════
🚫 BOUNDARIES
═══════════════════════════════════════════════════════════════

NEVER answer non-SCERT Telangana topics. NEVER give direct homework answers without teaching.
ALWAYS teach the concept first then help solve. ALWAYS reference chapter and page numbers.
ALWAYS use Telangana examples: Hyderabad Metro, Charminar, Hussain Sagar, Bathukamma, Golconda Fort.

Your mission: Make every student feel confident and capable. You are building young minds for a better Telangana!
"""

# ═══════════════════════════════════════════════════════════════
# 7. GROQ API CLIENT
# ═══════════════════════════════════════════════════════════════
# Support both .env (local) and Streamlit Cloud secrets
api_key = (
    os.getenv("GROQ_API_KEY")
    or os.getenv("GROK-API-KEY")          # legacy fallback
    or st.secrets.get("GROQ_API_KEY", None)
    or st.secrets.get("GROK-API-KEY", None)  # legacy fallback
)
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
    "page": "login",
    "last_spoken_idx": -1
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
                    st.error("⚠️ API Key not found. Add GROQ_API_KEY to your .env or Streamlit Cloud secrets.")
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

    # ── Handle voice input via query_params (cross-origin safe) ──
    # The mic component navigates window.parent.location to ?vt=<transcript>
    # Streamlit reruns and we read st.query_params here.
    voice_qp = st.query_params.get("vt", "").strip()
    if voice_qp:
        # Clear the param immediately so it doesn't re-trigger on next rerun
        st.query_params.clear()
        if check_usage_limit(data, username):
            process_message(voice_qp, "voice", data, username,
                            student_name, student_class, school)
        st.rerun()

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

        if voice_lang in ["Telugu", "Hindi", "Urdu"]:
            st.markdown(f"""
            <div style='background:rgba(245,158,11,0.1);border:1px solid #F59E0B;
                border-radius:8px;padding:0.6rem 0.8rem;font-size:0.75rem;color:#fbbf24;margin-top:0.3rem;'>
            🔔 <b>{voice_lang} voice</b> works best on<br>
            Chrome on Android phone.<br>
            Ask questions in {voice_lang} for full reply!
            </div>""", unsafe_allow_html=True)

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

    # ════════════════════════════════════════════════════════
    # ── CHAT HISTORY DISPLAY
    # ════════════════════════════════════════════════════════
    import re as _re2

    if not st.session_state.messages:
        st.markdown(f"""
        <div style='text-align:center; padding:2.5rem 1rem; color:var(--text-muted);'>
            <div style='font-size:3rem; margin-bottom:0.5rem;'>📚</div>
            <div style='font-size:1.1rem; font-weight:600; color:var(--text);'>
                Ready to learn, {student_name}!
            </div>
            <div style='font-size:0.88rem; margin-top:0.4rem;'>
                Type below or tap 🎙️ to speak your question
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                icon = "🎙️" if msg.get("type") == "voice" else "⌨️"
                st.markdown(f"""
                <div class='chat-user'>{icon} {msg['content']}
                    <div class='chat-meta'>{msg.get('time','')}</div>
                </div><div class='chat-clear'></div>""", unsafe_allow_html=True)
            elif msg["role"] == "assistant":
                c = msg['content']
                c = _re2.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', c)
                c = _re2.sub(r'\*(.+?)\*', r'<em>\1</em>', c)
                c = _re2.sub(r'#{1,6}\s*(.+)', r'<strong>\1</strong>', c)
                c = _re2.sub(r'\n\n', '<br><br>', c)
                c = _re2.sub(r'\n', '<br>', c)
                c = _re2.sub(r'[-•]\s+(.+?)(?=<br>|$)', r'&nbsp;&nbsp;▸ \1', c)
                st.markdown(f"""
                <div class='chat-ai'>🎓 {c}
                    <div class='chat-meta'>{msg.get('time','')}</div>
                </div><div class='chat-clear'></div>""", unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════
    # ── TTS: speak latest AI response (auto, one-way component)
    # ════════════════════════════════════════════════════════
    speak_content = ""
    if st.session_state.auto_speak and st.session_state.messages:
        for m in reversed(st.session_state.messages):
            if m["role"] == "assistant":
                last_ai_idx = len(st.session_state.messages)
                if last_ai_idx != st.session_state.get("last_spoken_idx", -1):
                    speak_content = strip_md_for_tts(m.get("content", ""))
                    st.session_state["last_spoken_idx"] = last_ai_idx
                break

    if speak_content:
        tts_html = get_tts_component_html(
            st.session_state.voice_lang,
            st.session_state.voice_gender,
            speak_content
        )
        components.html(tts_html, height=36, scrolling=False)

    # ════════════════════════════════════════════════════════
    # ── INPUT ROW: Native chat_input (text) + Mic component (voice)
    # ════════════════════════════════════════════════════════
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    if check_usage_limit(data, username):

        # ── Row: mic button (left) + text input (right) ──────
        mic_col, tip_col = st.columns([1, 5])

        with mic_col:
            # Mic component: captures voice, navigates parent URL to ?vt=<text>
            mic_html = get_mic_component_html(
                lang_code     = st.session_state.voice_lang,
                countdown_sec = 6
            )
            components.html(mic_html, height=64, scrolling=False)

        with tip_col:
            st.markdown(f"""
            <div style='background:#161B22;border:1px solid #30363D;border-radius:10px;
                padding:0.55rem 1rem;font-size:0.82rem;color:#8b949e;margin-top:6px;'>
            🎙️ Tap mic to speak &nbsp;·&nbsp; ⌨️ Or type below &nbsp;·&nbsp;
            <span style='color:#22D3A5;font-weight:600;'>
            {st.session_state.voice_lang} · {st.session_state.voice_gender} voice
            </span>
            </div>""", unsafe_allow_html=True)

        # ── Native Streamlit chat input — ALWAYS works, no JS bridge ──
        user_text = st.chat_input(
            f"Ask anything... (Class {student_class} · {st.session_state.voice_lang} Medium)",
            key="main_chat_input"
        )
        if user_text and user_text.strip():
            process_message(user_text.strip(), "text", data, username,
                            student_name, student_class, school)
            st.rerun()

    else:
        st.markdown(f"""
        <div style='background:rgba(239,68,68,0.1);border:1px solid #EF4444;
            border-radius:10px;padding:12px 20px;text-align:center;
            color:#fca5a5;font-size:0.9rem;margin-top:8px;'>
            ⏸️ Daily limit of {daily_limit} questions reached. Come back tomorrow!
        </div>""", unsafe_allow_html=True)

    # Footer
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='text-align:center; color:var(--text-muted); font-size:0.75rem; padding:0.5rem 0;'>
        🎓 Powered by AI9Campus &nbsp;|&nbsp; SCERT Telangana {st.session_state.voice_lang} Medium 2025-26 &nbsp;|&nbsp;
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
            model="llama-3.3-70b-versatile",   # reliable Groq model; swap to moonshotai/kimi-k2-instruct if available in your tier
            messages=api_messages,
            max_tokens=4096,
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
