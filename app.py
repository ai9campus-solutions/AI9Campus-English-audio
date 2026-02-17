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
#    TEXT:  st.chat_input() — native Streamlit, no JS needed
#    VOICE: components.html mic → DOM fills st.chat_input textarea
#           (allow-same-origin is set on components.html — DOM access works)
#    TTS:   components.html one-way audio out + live text display
# ═══════════════════════════════════════════════════════════════
import streamlit.components.v1 as components
import re as _re

def strip_md_for_tts(text):
    t = _re.sub(r'\*{1,3}(.*?)\*{1,3}', r'\1', text, flags=_re.DOTALL)
    t = _re.sub(r'#{1,6}\s*', '', t)
    t = _re.sub(r'`{1,3}.*?`{1,3}', '', t, flags=_re.DOTALL)
    t = _re.sub(r'[-•►▸]\s+', '', t)
    t = _re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', t)
    t = _re.sub(r'[|]', ' ', t)
    t = _re.sub(r'\s{2,}', ' ', t)
    return t.strip()

# ─────────────────────────────────────────────────────────────────
# MIC COMPONENT
# Shows: mic button + live transcript preview bar + send button
# Bridge: fills window.parent's st.chat_input textarea via DOM
#         (safe because components.html has allow-same-origin)
# ─────────────────────────────────────────────────────────────────
def get_mic_component_html(lang_code, countdown_sec=6):
    lang_map = {"English":"en-IN","Telugu":"te-IN","Hindi":"hi-IN"}
    lang     = lang_map.get(lang_code, "en-IN")
    return f"""<!DOCTYPE html><html><head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{{box-sizing:border-box;margin:0;padding:0;font-family:'Segoe UI',Roboto,sans-serif;}}
body{{background:transparent;padding:4px 0;}}
.row{{display:flex;align-items:center;gap:8px;width:100%;}}
/* Mic button */
.mic{{
  width:46px;height:46px;min-width:46px;border-radius:50%;border:none;
  display:flex;align-items:center;justify-content:center;
  cursor:pointer;font-size:1.25rem;transition:all 0.18s;
  -webkit-tap-highlight-color:transparent;flex-shrink:0;
}}
.mic:active{{transform:scale(0.88);}}
.mic-idle{{background:#2D333B;color:#8b949e;border:2px solid #30363D;}}
.mic-idle:hover{{background:#3D444D;color:#e6edf3;}}
.mic-on{{background:linear-gradient(135deg,#EF4444,#DC2626);color:white;border:2px solid transparent;
  animation:mpulse 0.9s infinite;box-shadow:0 0 0 4px rgba(239,68,68,0.3);}}
@keyframes mpulse{{0%,100%{{box-shadow:0 0 0 3px rgba(239,68,68,0.3);}}50%{{box-shadow:0 0 0 8px rgba(239,68,68,0.08);}}}}
/* Preview bar — the "text bar beside mic" the user requested */
.preview{{
  flex:1;min-width:0;
  background:#161B22;border:1.5px solid #30363D;border-radius:10px;
  padding:8px 12px;font-size:0.85rem;color:#e6edf3;
  min-height:38px;display:flex;align-items:center;
  transition:border-color 0.2s;word-break:break-word;
  line-height:1.4;
}}
.preview.listening{{border-color:#EF4444;}}
.preview.ready{{border-color:#22D3A5;}}
.preview.sending{{border-color:#4F8EF7;}}
.placeholder{{color:#484f58;font-size:0.82rem;}}
/* Send button */
.send{{
  width:38px;height:38px;min-width:38px;border-radius:50%;border:none;
  background:linear-gradient(135deg,#4F8EF7,#2563EB);color:white;
  display:flex;align-items:center;justify-content:center;
  cursor:pointer;font-size:1rem;flex-shrink:0;
  transition:all 0.18s;visibility:hidden;
}}
.send.show{{visibility:visible;}}
.send:hover{{background:linear-gradient(135deg,#60a5fa,#3b82f6);transform:scale(1.06);}}
.send:active{{transform:scale(0.9);}}
/* Countdown pill */
.cd-pill{{
  display:none;background:rgba(34,211,165,0.15);border:1px solid #22D3A5;
  border-radius:50px;padding:1px 9px;font-size:0.72rem;color:#22D3A5;font-weight:700;
  flex-shrink:0;
}}
.cd-pill.on{{display:inline-block;}}
/* Listening dot */
.ldot{{display:inline-block;width:7px;height:7px;background:#EF4444;border-radius:50%;
  animation:dp 0.9s infinite;vertical-align:middle;margin-right:5px;}}
@keyframes dp{{0%,100%{{opacity:1;}}50%{{opacity:0.15;}}}}
</style></head><body>
<div class="row">
  <button class="mic mic-idle" id="micBtn" onclick="toggleMic()" title="Tap to speak your question">🎙️</button>
  <div class="preview" id="preview">
    <span class="placeholder" id="ph">Tap 🎙️ mic → speak → see text here → auto-sends</span>
  </div>
  <span class="cd-pill" id="cdPill">{countdown_sec}s</span>
  <button class="send" id="sendBtn" onclick="sendNow()" title="Send now">➤</button>
</div>
<script>
var SR       = window.SpeechRecognition || window.webkitSpeechRecognition;
var rec      = null;
var isListen = false;
var cdTimer  = null;
var cdLeft   = {countdown_sec};
var LANG     = '{lang}';
var finalTxt = '';

var micBtn  = document.getElementById('micBtn');
var preview = document.getElementById('preview');
var ph      = document.getElementById('ph');
var cdPill  = document.getElementById('cdPill');
var sendBtn = document.getElementById('sendBtn');

function setPreview(html, state){{
  ph.style.display = 'none';
  preview.innerHTML = html;
  preview.className = 'preview' + (state ? ' '+state : '');
}}
function resetPreview(){{
  preview.innerHTML = '';
  preview.appendChild(ph);
  ph.style.display = '';
  preview.className = 'preview';
}}

// ── Mic toggle ────────────────────────────────────────────────
function toggleMic(){{
  if(!SR){{ setPreview('⚠️ Use <b>Google Chrome</b> browser for voice',''); return; }}
  if(isListen){{ stopMic(); }} else {{ startMic(); }}
}}

function startMic(){{
  cancelCountdown(); finalTxt='';
  sendBtn.className='send'; // hide send
  rec = new SR();
  rec.lang = LANG; rec.continuous = false; rec.interimResults = true; rec.maxAlternatives = 3;

  rec.onstart = function(){{
    isListen = true;
    micBtn.className = 'mic mic-on'; micBtn.innerHTML = '⏹';
    setPreview('<span class="ldot"></span><em style="color:#8b949e;">Listening in {lang_code}...</em>', 'listening');
  }};

  rec.onresult = function(e){{
    var interim='', final='';
    for(var i=e.resultIndex; i<e.results.length; i++){{
      var t = e.results[i][0].transcript;
      if(e.results[i].isFinal){{ final += t; }} else {{ interim += t; }}
    }}
    if(final){{
      finalTxt = final.trim();
      setPreview('✅ <span style="color:#22D3A5;font-weight:600;">' + finalTxt + '</span>', 'ready');
      sendBtn.className = 'send show';
      startCountdown();
    }} else if(interim){{
      setPreview('<span class="ldot"></span><span style="color:#e6edf3;">' + interim + '</span>', 'listening');
    }}
  }};

  rec.onerror = function(e){{
    isListen = false; resetMic();
    var m = {{'no-speech':'🔇 No speech detected. Tap mic and try again.',
              'not-allowed':'🚫 Microphone blocked — allow mic in browser address bar.',
              'audio-capture':'🎤 No microphone found.'}};
    setPreview(m[e.error] || '⚠️ Error: '+e.error, '');
  }};

  rec.onend = function(){{
    isListen = false; resetMic();
  }};

  try{{ rec.start(); }}
  catch(ex){{ setPreview('Mic error: '+ex.message,''); isListen=false; resetMic(); }}
}}

function stopMic(){{
  if(rec){{ try{{ rec.stop(); }}catch(e){{}} }}
  isListen = false; resetMic();
}}
function resetMic(){{
  micBtn.className = 'mic mic-idle'; micBtn.innerHTML = '🎙️';
}}

// ── Countdown ─────────────────────────────────────────────────
function startCountdown(){{
  cdLeft = {countdown_sec};
  cdPill.innerText = cdLeft+'s'; cdPill.className = 'cd-pill on';
  cdTimer = setInterval(function(){{
    cdLeft--;
    cdPill.innerText = cdLeft+'s';
    if(cdLeft <= 0){{ clearInterval(cdTimer); cdTimer=null; cdPill.className='cd-pill'; sendNow(); }}
  }}, 1000);
}}
function cancelCountdown(){{
  if(cdTimer){{ clearInterval(cdTimer); cdTimer=null; }}
  cdPill.className = 'cd-pill';
}}

// ── Send to Streamlit via DOM fill of st.chat_input ──────────
// VOICE:: prefix is prepended to the message text.
// Python strips it and uses it to detect voice origin reliably —
// no separate hidden input needed, works on Streamlit Cloud.
function sendNow(){{
  var text = finalTxt.trim();
  if(!text) return;
  cancelCountdown();
  sendBtn.className = 'send';
  setPreview('⏳ <span style="color:#4F8EF7;">Sending to AI...</span>', 'sending');

  // Prefix "VOICE::" so Python knows this was voice input
  var voiceText = 'VOICE::' + text;

  function tryFill(){{
    var sent = false;
    try{{
      var pd = window.parent.document;

      // Find the chat input textarea
      var ta = pd.querySelector('textarea[data-testid="stChatInputTextArea"]');
      if(!ta) ta = pd.querySelector('[data-testid="stChatInput"] textarea');
      if(!ta) ta = pd.querySelector('section[data-testid="stChatInput"] textarea');
      if(!ta) ta = pd.querySelector('textarea');

      if(ta){{
        var natSetter = Object.getOwnPropertyDescriptor(
          window.parent.HTMLTextAreaElement.prototype, 'value'
        ).set;
        natSetter.call(ta, voiceText);
        ta.dispatchEvent(new Event('input',  {{bubbles:true}}));
        ta.dispatchEvent(new Event('change', {{bubbles:true}}));

        // Click submit button after short delay
        setTimeout(function(){{
          var btn = pd.querySelector('button[data-testid="stChatInputSubmitButton"]');
          if(!btn) btn = pd.querySelector('[data-testid="stChatInput"] button[kind="primaryFormSubmit"]');
          if(!btn) btn = pd.querySelector('[data-testid="stChatInput"] button');
          if(btn){{
            btn.click();
            setPreview('✅ <span style="color:#22D3A5;">Sent! AI is thinking...</span>','ready');
            setTimeout(function(){{ resetPreview(); finalTxt=''; }}, 3000);
          }}
        }}, 250);
        sent = true;
      }}
    }} catch(ex){{
      console.info('DOM access restricted, trying direct fill:', ex.message);
    }}

    // Fallback: put voiced text in preview so user can copy-paste if needed
    if(!sent){{
      setPreview('🎙️ <span style="color:#22D3A5;">Heard: <b>' + escHtml(text) + '</b></span><br><span style="color:#8b949e;font-size:0.75rem;">✏️ Text copied below — press Enter to send</span>', 'ready');
      // Try one more approach for Streamlit Cloud
      try{{
        var pd3 = window.parent.document;
        var allInputs = pd3.querySelectorAll('textarea');
        for(var i=0; i<allInputs.length; i++){{
          var el = allInputs[i];
          try{{
            var s3 = Object.getOwnPropertyDescriptor(window.parent.HTMLTextAreaElement.prototype,'value').set;
            s3.call(el, voiceText);
            el.dispatchEvent(new Event('input', {{bubbles:true}}));
            el.focus();
            break;
          }}catch(se){{}}
        }}
      }}catch(de){{}}
      setTimeout(function(){{ resetPreview(); finalTxt=''; }}, 5000);
    }}
  }}

  setTimeout(tryFill, 80);
}}
</script></body></html>"""

# ─────────────────────────────────────────────────────────────────
# TTS COMPONENT
# Shows: live text being read + animated waveform + stop button
# One-way (Python → JS) — no bridge needed
# ─────────────────────────────────────────────────────────────────
def get_tts_component_html(lang_code, gender, speak_text):
    """
    Natural Indian TTS component.
    - Preprocesses text to add natural pauses for Indian speech rhythm
    - Strictly picks Indian voices (Raveena / Heera / Google English India)
    - rate 0.80 — deliberate, warm teacher pace
    - Chrome 15s keepalive fix included
    """
    lang_map = {"English":"en-IN","Telugu":"te-IN","Hindi":"hi-IN"}
    lang     = lang_map.get(lang_code, "en-IN")
    # Indian voice pitch: Female slightly raised, Male slightly lower — natural range
    pitch    = "1.1" if gender == "Female" else "0.88"

    # ── Server-side text preprocessing for natural Indian speech ─────
    import re as _tts_re

    def naturalise_indian(text):
        """Add commas/pauses at natural Indian speech break points."""
        # After Indian filler words — add pause so voice sounds natural
        t = text
        t = _tts_re.sub(r'\b(Arey|Arre|Accha|Haan|Chalo|Yaar|Na|Suno|Dekho|Bhai|Behen)\b',
                        r'\1,', t, flags=_tts_re.IGNORECASE)
        # "na" at end of clause (not "Naan" or "nahi")
        t = _tts_re.sub(r'\bna\b(?=[.!? ])', r'na,', t)
        # Double space after sentence endings for longer pause
        t = _tts_re.sub(r'([.!?])\s+', r'\1  ', t)
        # Spell out common symbols that TTS reads badly
        t = t.replace(' % ', ' percent ')
        t = t.replace('%', ' percent')
        t = t.replace('₹', 'rupees ')
        t = t.replace('&', ' and ')
        t = t.replace('=', ' equals ')
        t = t.replace('+', ' plus ')
        t = t.replace('×', ' times ')
        t = t.replace('÷', ' divided by ')
        return t

    processed = naturalise_indian(speak_text)

    safe_spk = (processed
                .replace("\\", "\\\\")
                .replace("'", "\\'")
                .replace("\r", " ")
                .replace("\n", "  ")   # double space = natural pause in TTS
                .replace("`", "'"))

    return f"""<!DOCTYPE html><html><head>
<style>
*{{box-sizing:border-box;margin:0;padding:0;font-family:'Segoe UI',Roboto,sans-serif;}}
body{{background:transparent;padding:4px 0;}}
.tts-box{{
  background:linear-gradient(135deg,rgba(34,211,165,0.09),rgba(79,142,247,0.06));
  border:1px solid rgba(34,211,165,0.35);border-radius:12px;
  padding:10px 14px;display:flex;flex-direction:column;gap:5px;
  animation:fadein 0.3s ease;
}}
@keyframes fadein{{from{{opacity:0;transform:translateY(-4px);}}to{{opacity:1;transform:none;}}}}
.tts-top{{display:flex;align-items:center;gap:8px;}}
.wave{{display:flex;align-items:flex-end;gap:2.5px;height:18px;flex-shrink:0;}}
.wb{{width:3px;border-radius:2px;animation:wb 0.6s infinite ease-in-out;}}
.wb:nth-child(1){{height:5px; background:#22D3A5;animation-delay:0s;}}
.wb:nth-child(2){{height:13px;background:#4F8EF7;animation-delay:0.12s;}}
.wb:nth-child(3){{height:8px; background:#22D3A5;animation-delay:0.24s;}}
.wb:nth-child(4){{height:15px;background:#F59E0B;animation-delay:0.36s;}}
.wb:nth-child(5){{height:6px; background:#22D3A5;animation-delay:0.48s;}}
@keyframes wb{{0%,100%{{transform:scaleY(0.3);}}50%{{transform:scaleY(1.0);}}}}
.lbl{{font-size:0.78rem;color:#fbbf24;font-weight:700;flex:1;}}
.stop{{background:#2D333B;border:1px solid #30363D;color:#F59E0B;
  border-radius:50px;padding:3px 14px;font-size:0.74rem;cursor:pointer;flex-shrink:0;}}
.stop:hover{{background:#3D444D;color:#fff;}}
.progress-row{{display:flex;align-items:center;gap:8px;}}
.prog-bar{{flex:1;height:3px;background:#21262D;border-radius:2px;overflow:hidden;}}
.prog-fill{{height:100%;background:linear-gradient(90deg,#22D3A5,#4F8EF7);
  border-radius:2px;transition:width 0.4s linear;width:0%;}}
.live-txt{{
  font-size:0.83rem;color:#c9d1d9;line-height:1.55;padding-top:2px;
  border-left:2px solid rgba(34,211,165,0.4);padding-left:8px;
  min-height:20px;
}}
.hi{{color:#22D3A5;font-weight:600;}}
</style></head><body>
<div class="tts-box" id="box">
  <div class="tts-top">
    <div class="wave">
      <div class="wb"></div><div class="wb"></div><div class="wb"></div>
      <div class="wb"></div><div class="wb"></div>
    </div>
    <span class="lbl" id="lbl">🔊 Reading aloud in {lang_code}...</span>
    <button class="stop" onclick="stopSpeak()">⏹ Stop</button>
  </div>
  <div class="progress-row">
    <div class="prog-bar"><div class="prog-fill" id="prog"></div></div>
  </div>
  <div class="live-txt" id="live"></div>
</div>
<script>
// ── Config ─────────────────────────────────────────────────
var FULL_TEXT = '{safe_spk}';
var LANG      = '{lang}';
var PITCH     = {pitch};
var GENDER    = '{gender}';
var RATE      = 0.80;  // Warm, deliberate Indian teacher pace

// ── Voice priority lists (Indian voices first) ─────────────
// These are the actual voice names on Chrome/Android for Indian voices
var FEMALE_VOICES = [
  'google english (india)','raveena','heera','lekha','aditi','swara',
  'kalpana','sunali','google hindi','google telugu','female','en-in'
];
var MALE_VOICES = [
  'google english (india)','hemant','rajan','mohan','male',
  'google hindi','google telugu','en-in'
];

// ── State ──────────────────────────────────────────────────
var queue      = [];
var running    = false;
var totalChunks= 0;
var doneChunks = 0;
var curChunk   = '';
var prog       = document.getElementById('prog');
var lbl        = document.getElementById('lbl');
var live       = document.getElementById('live');

// ── Split into short, natural sentence chunks ──────────────
function chunkText(text) {{
  // Split at sentence boundaries
  var raw = text.match(/[^.!?।]+[.!?।]?/g) || [text];
  var out = []; var buf = '';
  for (var i = 0; i < raw.length; i++) {{
    var s = raw[i].trim();
    if (!s) continue;
    if ((buf + ' ' + s).trim().length > 160) {{
      if (buf) out.push(buf.trim());
      buf = s;
    }} else {{
      buf = (buf + ' ' + s).trim();
    }}
  }}
  if (buf) out.push(buf.trim());
  return out.length ? out : [text];
}}

// ── Pick best Indian voice ──────────────────────────────────
function pickVoice(voices) {{
  var priority = (GENDER === 'Female') ? FEMALE_VOICES : MALE_VOICES;
  var langBase = LANG.split('-')[0].toLowerCase();

  // Pass 1: exact lang match + Indian voice name keyword
  for (var i = 0; i < voices.length; i++) {{
    var v = voices[i];
    var vl = v.lang.toLowerCase();
    var vn = v.name.toLowerCase();
    if (vl === LANG.toLowerCase() || vl.startsWith(langBase + '-')) {{
      for (var j = 0; j < priority.length; j++) {{
        if (vn.indexOf(priority[j]) >= 0) return v;
      }}
    }}
  }}

  // Pass 2: any voice for this language
  for (var i = 0; i < voices.length; i++) {{
    var v = voices[i];
    if (v.lang.toLowerCase().startsWith(langBase)) return v;
  }}

  // Pass 3: Indian English fallback for Indian languages (Telugu/Hindi)
  if (LANG !== 'en-IN') {{
    for (var i = 0; i < voices.length; i++) {{
      if (voices[i].lang.toLowerCase() === 'en-in') return voices[i];
    }}
    for (var i = 0; i < voices.length; i++) {{
      if (voices[i].lang.toLowerCase().startsWith('en')) return voices[i];
    }}
  }}
  return null;
}}

// ── Speak one chunk ────────────────────────────────────────
function speakChunk() {{
  if (running || queue.length === 0) {{ if (!running) finish(); return; }}
  running  = true;
  curChunk = queue.shift();

  // Update live text
  live.innerHTML = '<span class="hi">' + escHtml(curChunk) + '</span>';
  lbl.textContent = '🔊 Reading — chunk ' + (doneChunks+1) + ' of ' + totalChunks;

  // Update progress bar
  var pct = Math.round((doneChunks / totalChunks) * 100);
  prog.style.width = pct + '%';

  var u   = new SpeechSynthesisUtterance(curChunk);
  u.lang  = LANG;
  u.rate  = RATE;
  u.pitch = PITCH;
  u.volume= 1.0;

  var voices = window.speechSynthesis.getVoices();
  var v = pickVoice(voices);
  if (v) u.voice = v;

  u.onend = function() {{
    running = false;
    doneChunks++;
    prog.style.width = Math.round((doneChunks / totalChunks) * 100) + '%';
    setTimeout(speakChunk, 80);
  }};
  u.onerror = function() {{
    running = false;
    doneChunks++;
    setTimeout(speakChunk, 80);
  }};

  // Chrome 15s silent cutoff fix
  var ka = setInterval(function() {{
    if (!window.speechSynthesis.speaking) {{ clearInterval(ka); return; }}
    window.speechSynthesis.pause();
    window.speechSynthesis.resume();
  }}, 10000);

  window.speechSynthesis.speak(u);
}}

function doSpeak(text) {{
  if (!window.speechSynthesis || !text || text.trim().length < 2) return;
  window.speechSynthesis.cancel();
  queue       = chunkText(text);
  totalChunks = queue.length;
  doneChunks  = 0;
  running     = false;

  function start() {{ setTimeout(speakChunk, 250); }}
  var v = window.speechSynthesis.getVoices();
  if (v.length === 0) {{ window.speechSynthesis.onvoiceschanged = start; }}
  else {{ start(); }}
}}

function stopSpeak() {{
  queue = []; running = false;
  if (window.speechSynthesis) window.speechSynthesis.cancel();
  finish();
}}

function finish() {{
  prog.style.width = '100%';
  live.innerHTML   = '<span style="color:#22D3A5;">✅ Done reading.</span>';
  lbl.textContent  = '🔊 Reading complete';
  setTimeout(function() {{
    document.getElementById('box').style.display = 'none';
  }}, 1800);
}}

function escHtml(s) {{
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}}

// ── Auto-start on load ──────────────────────────────────────
// Autoplay policy: try to start immediately; if blocked show a play button.
var autoStarted = false;

function tryAutoPlay() {{
  if (autoStarted) return;
  if (!FULL_TEXT || FULL_TEXT.trim().length < 2) return;
  try {{
    doSpeak(FULL_TEXT);
    autoStarted = true;
  }} catch(e) {{
    showPlayBtn();
  }}
}}

function showPlayBtn() {{
  var box = document.getElementById('box');
  if (!box) return;
  var pb = document.createElement('button');
  pb.textContent = '▶ Tap to hear answer';
  pb.style.cssText = 'background:linear-gradient(135deg,#22D3A5,#4F8EF7);color:#fff;border:none;border-radius:50px;padding:6px 18px;font-size:0.82rem;font-weight:700;cursor:pointer;margin-top:6px;';
  pb.onclick = function() {{
    pb.remove();
    doSpeak(FULL_TEXT);
    autoStarted = true;
  }};
  box.appendChild(pb);
}}

if (FULL_TEXT && FULL_TEXT.trim().length > 2) {{
  // Small delay lets Streamlit iframe finish mounting
  setTimeout(tryAutoPlay, 600);
  // Also trigger on any user interaction with the document (for autoplay policy)
  document.addEventListener('click', function onceClick() {{
    document.removeEventListener('click', onceClick);
    if (!autoStarted) tryAutoPlay();
  }});
}}
</script></body></html>"""

# ═══════════════════════════════════════════════════════════════
# 6. SYSTEM PROMPT
# ═══════════════════════════════════════════════════════════════
def build_system_prompt(school_name, student_name, student_class):
    return f"""
You are a warm, friendly AI Tutor from {school_name}, helping students of Telangana State Board (SCERT) for Academic Year 2025-26.

You are talking to: {student_name}, Class {student_class}.

LANGUAGE RULE — READ THIS FIRST:
Respond in the SAME language the student uses. English question gets English reply. Telugu question gets Telugu reply. Hindi question gets Hindi reply.

ENGLISH STYLE — MANDATORY INDIAN TEACHER STYLE:
You must write and speak exactly like a caring, experienced Indian teacher from Telangana. Your English must feel warm, local, and natural — not foreign.

ALWAYS use these natural Indian English patterns:
- Start with: "Arey, good question na!" or "Haan, chalo I will explain!"
- Use "na" at end of short phrases: "simple only na", "got it na"
- Use "only" for emphasis: "this is the main point only", "very easy only it is"
- Use "see": "see, what happens is...", "see na, like this only"
- Use: "Accha, so basically...", "Chalo, let us start step by step"
- Use: "No tension!", "Suno carefully", "Ekdum sahi!", "Arre wah!"
- Use: "Think of it this way na...", "Basically what happens is..."
- End with: "Got it na? Or shall I explain once more?"

STRICTLY FORBIDDEN — DO NOT USE EVER:
"Hey guys", "Awesome", "That is great", "Absolutely", "Certainly", "Of course",
"Fascinating", "Delve into", "Let us explore", "Indeed", any American/British style phrases.

TELUGU STYLE (when student writes in Telugu):
Reply fully in Telugu, like a local Telangana teacher.
Example: "అరేయ్! చాలా మంచి ప్రశ్న అడిగావు. చూడు, ఈ విషయం చాలా సులభంగా ఉంటుంది. మొదట..."

HINDI STYLE (when student writes in Hindi):
Reply fully in Hindi, natural Hyderabadi Hindi mix.
Example: "अरे यार! बहुत अच्छा सवाल पूछा। देखो, यह बात बहुत आसान है। पहले..."

TTS SPEECH FORMAT — MANDATORY (responses are read aloud):
Your response will be SPOKEN by text-to-speech. Write for ears, not eyes.
- Short sentences only. Maximum 20 words per sentence.
- No markdown: no asterisks, no hash signs, no dashes as bullets, no arrows.
- Spell numbers as words: write "six" not "6", "fifteen" not "15"
- Spell formulas as words: "H two O" for H2O, "a squared plus b squared" for a2+b2
- Spell fractions as words: "three by four" not "3/4"
- Say "Chapter one" not "Ch 1", say "page fourteen" not "pp14"
- Use "Step one... Step two... Step three..." for any list
- Put commas where you want a natural breath pause
- No abbreviations at all

═══════════════════════════════════════════════════════════════
📚 KNOWLEDGE BASE & SCOPE
═══════════════════════════════════════════════════════════════

OFFICIAL SOURCE: SCERT Telangana e-Textbooks (https://scert.telangana.gov.in/)
Academic Year: 2025-26 | Medium: English, Telugu, Hindi | Classes: 1 to 10

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
    "last_spoken_idx": -1,
    "last_input_type": "text"  # "text" or "voice" — TTS fires only for voice
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
        LANGS = ["English", "Telugu", "Hindi"]
        # Guard: reset if Urdu was previously stored
        if st.session_state.voice_lang not in LANGS:
            st.session_state.voice_lang = "English"
        voice_lang = st.selectbox(
            "🗣️ Voice Language",
            LANGS,
            index=LANGS.index(st.session_state.voice_lang)
        )
        if voice_lang != st.session_state.voice_lang:
            st.session_state.voice_lang = voice_lang
            st.rerun()

        if voice_lang in ["Telugu", "Hindi"]:
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
    # ── TTS COMPONENT — shown ABOVE chat so it plays immediately
    # ════════════════════════════════════════════════════════
    import re as _re2

    speak_content = ""
    # TTS fires ONLY when the triggering user message was voice input.
    # We check the "type" field of the last user message in session_state
    # (set by process_message using the voice flag detection).
    last_user_type = "text"
    for m in reversed(st.session_state.messages):
        if m["role"] == "user":
            last_user_type = m.get("type", "text")
            break

    is_voice_input = last_user_type == "voice"
    # ── STRICT RULE: Audio output ONLY for voice/mic input ──────────────
    # When student types text → NO audio output (only text on screen)
    # When student uses mic   → audio output plays automatically
    if st.session_state.auto_speak and is_voice_input and st.session_state.messages:
        for m in reversed(st.session_state.messages):
            if m["role"] == "assistant":
                # Use a content hash (not message count) so dedup is collision-proof
                import hashlib as _hl
                msg_hash = _hl.md5(m.get("content","").encode()).hexdigest()[:12]
                if msg_hash != st.session_state.get("last_spoken_idx", ""):
                    speak_content = strip_md_for_tts(m.get("content", ""))
                    st.session_state["last_spoken_idx"] = msg_hash
                break

    if speak_content:
        tts_html = get_tts_component_html(
            st.session_state.voice_lang,
            st.session_state.voice_gender,
            speak_content
        )
        components.html(tts_html, height=130, scrolling=False)

    # ════════════════════════════════════════════════════════
    # ── CHAT HISTORY DISPLAY
    # ════════════════════════════════════════════════════════
    if not st.session_state.messages:
        st.markdown(f"""
        <div style='text-align:center; padding:2.5rem 1rem; color:var(--text-muted);'>
            <div style='font-size:3rem; margin-bottom:0.5rem;'>📚</div>
            <div style='font-size:1.1rem; font-weight:600; color:var(--text);'>
                Ready to learn, {student_name}!
            </div>
            <div style='font-size:0.88rem; margin-top:0.4rem;'>
                Tap 🎙️ mic to speak, or type below
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
    # ── INPUT: Mic component (with preview bar) + st.chat_input
    # ════════════════════════════════════════════════════════
    #
    # HOW VOICE DETECTION WORKS:
    #   1. Mic JS captures speech and prepends "VOICE::" to the text
    #   2. JS fills + submits st.chat_input with "VOICE::<transcript>"
    #   3. Streamlit reruns from st.chat_input submit
    #   4. Python detects "VOICE::" prefix → msg_type="voice" → TTS fires
    #   5. Python strips the prefix before storing/sending to AI
    #   Text input: no prefix → msg_type="text" → NO audio output
    # ════════════════════════════════════════════════════════
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    if check_usage_limit(data, username):

        # ── Mic component ─────────────────────────────────────────────
        mic_html = get_mic_component_html(
            lang_code     = st.session_state.voice_lang,
            countdown_sec = 6
        )
        components.html(mic_html, height=58, scrolling=False)

        # ── Native chat_input (text) ──────────────────────────────────
        user_text = st.chat_input(
            f"⌨️  Type your question here... (Class {student_class} · {st.session_state.voice_lang})",
            key="main_chat_input"
        )

        if user_text and user_text.strip():
            # Detect voice origin: JS prefixes text with "VOICE::"
            raw = user_text.strip()
            if raw.startswith("VOICE::"):
                msg_type = "voice"
                cleaned_text = raw[len("VOICE::"):]
            else:
                msg_type = "text"
                cleaned_text = raw

            if cleaned_text:
                process_message(cleaned_text, msg_type, data, username,
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

    # Track whether this was voice or text — TTS fires only for voice
    st.session_state.last_input_type = msg_type

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
