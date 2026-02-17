"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🎓 AI SMART TUTOR - SIDEBAR LAYOUT                        ║
║                   Matching the provided screenshot design                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
from groq import Groq
import streamlit.components.v1 as components
import os
import json
import hashlib
import datetime
from dotenv import load_dotenv
from pathlib import Path
import re

# ═══════════════════════════════════════════════════════════════════════════════
# 1. ENVIRONMENT SETUP
# ═══════════════════════════════════════════════════════════════════════════════
load_dotenv()

# Groq API client
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
if GROQ_API_KEY:
    groq_client = Groq(api_key=GROQ_API_KEY)
else:
    groq_client = None

# ═══════════════════════════════════════════════════════════════════════════════
# 2. PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="School Name Smart Tutor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════════════
# 3. DATA FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def load_data():
    """Load or create default data."""
    return {
        "settings": {
            "school_name": "School Name",
            "daily_limit": 30
        },
        "users": {
            "student1": {
                "name": "Demo Student",
                "class": "10",
                "medium": "English Medium",
                "board": "SCERT Telangana"
            }
        }
    }

# ═══════════════════════════════════════════════════════════════════════════════
# 4. TTS AND VOICE HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def strip_md_for_tts(text):
    """Strip markdown formatting for TTS."""
    t = re.sub(r'\*{1,3}(.*?)\*{1,3}', r'\1', text, flags=re.DOTALL)
    t = re.sub(r'#{1,6}\s*', '', t)
    t = re.sub(r'`{1,3}.*?`{1,3}', '', t, flags=re.DOTALL)
    t = re.sub(r'[-•►▸]\s+', '', t)
    t = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', t)
    t = re.sub(r'[|]', ' ', t)
    t = re.sub(r'\s{2,}', ' ', t)
    return t.strip()

def get_mic_component_html(lang_code, countdown_sec=5):
    """Generate HTML for mic button with speech recognition."""
    lang_map = {"English": "en-IN", "Telugu": "te-IN", "Hindi": "hi-IN"}
    lang = lang_map.get(lang_code, "en-IN")
    
    return f"""<!DOCTYPE html>
<html><head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
* {{box-sizing:border-box;margin:0;padding:0;font-family:'Inter',sans-serif;}}
body {{background:transparent;padding:4px 0;}}
.mic-row {{display:flex;align-items:center;gap:10px;width:100%;}}
.mic-btn {{
  width:50px;height:50px;border-radius:50%;border:none;
  display:flex;align-items:center;justify-content:center;
  cursor:pointer;font-size:1.4rem;transition:all 0.2s;
  flex-shrink:0;-webkit-tap-highlight-color:transparent;
}}
.mic-btn:active {{transform:scale(0.9);}}
.mic-idle {{
  background:linear-gradient(135deg,rgba(6,182,212,0.15),rgba(59,130,246,0.12));
  border:2px solid rgba(6,182,212,0.4);color:#06b6d4;
}}
.mic-idle:hover {{
  background:linear-gradient(135deg,rgba(6,182,212,0.25),rgba(59,130,246,0.2));
  border-color:#06b6d4;color:#22d3ee;
}}
.mic-on {{
  background:linear-gradient(135deg,#ef4444,#dc2626);
  border:2px solid transparent;color:#fff;
  animation:pulse 0.9s infinite;box-shadow:0 0 0 4px rgba(239,68,68,0.3);
}}
@keyframes pulse {{0%,100%{{box-shadow:0 0 0 3px rgba(239,68,68,0.3);}}50%{{box-shadow:0 0 0 8px rgba(239,68,68,0.1);}}}}
.preview {{
  flex:1;min-width:0;
  background:rgba(15,23,42,0.6);border:1.5px solid rgba(51,65,85,0.5);
  border-radius:12px;padding:10px 14px;font-size:0.875rem;color:#e2e8f0;
  min-height:42px;display:flex;align-items:center;transition:border-color 0.2s;
}}
.preview.listening {{border-color:#ef4444;background:rgba(239,68,68,0.08);}}
.preview.ready {{border-color:#22d3ee;background:rgba(34,211,238,0.08);}}
.placeholder {{color:#64748b;font-size:0.8125rem;}}
.send-btn {{
  width:42px;height:42px;border-radius:50%;border:none;
  background:linear-gradient(135deg,#06b6d4,#0891b2);color:#fff;
  display:flex;align-items:center;justify-content:center;
  cursor:pointer;font-size:1.1rem;flex-shrink:0;
  transition:all 0.2s;visibility:hidden;
}}
.send-btn.show {{visibility:visible;}}
.send-btn:hover {{background:linear-gradient(135deg,#22d3ee,#06b6d4);transform:scale(1.05);}}
.send-btn:active {{transform:scale(0.95);}}
.cd-pill {{
  display:none;background:rgba(34,211,238,0.15);border:1px solid #22d3ee;
  border-radius:50px;padding:2px 10px;font-size:0.7rem;color:#22d3ee;font-weight:700;flex-shrink:0;
}}
.cd-pill.on {{display:inline-block;}}
.ldot {{display:inline-block;width:7px;height:7px;background:#ef4444;border-radius:50%;
  animation:dp 0.9s infinite;vertical-align:middle;margin-right:5px;}}
@keyframes dp {{0%,100%{{opacity:1;}}50%{{opacity:0.15;}}}}
</style></head><body>
<div class="mic-row">
  <button class="mic-btn mic-idle" id="micBtn" onclick="toggleMic()" title="Tap to speak">🎙️</button>
  <div class="preview" id="preview">
    <span class="placeholder" id="ph">Tap 🎙️ mic to speak your question</span>
  </div>
  <span class="cd-pill" id="cdPill">{countdown_sec}s</span>
  <button class="send-btn" id="sendBtn" onclick="sendNow()" title="Send now">➤</button>
</div>
<script>
var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
var rec = null;
var isListen = false;
var cdTimer = null;
var cdLeft = {countdown_sec};
var LANG = '{lang}';
var finalTxt = '';

var micBtn = document.getElementById('micBtn');
var preview = document.getElementById('preview');
var ph = document.getElementById('ph');
var cdPill = document.getElementById('cdPill');
var sendBtn = document.getElementById('sendBtn');

function setPreview(html, state) {{
  ph.style.display = 'none';
  preview.innerHTML = html;
  preview.className = 'preview' + (state ? ' ' + state : '');
}}
function resetPreview() {{
  preview.innerHTML = '';
  preview.appendChild(ph);
  ph.style.display = '';
  preview.className = 'preview';
}}

function toggleMic() {{
  if (!SR) {{ setPreview('⚠️ Use Chrome for voice', ''); return; }}
  if (isListen) {{ stopMic(); }} else {{ startMic(); }}
}}

function startMic() {{
  cancelCountdown();
  finalTxt = '';
  sendBtn.className = 'send-btn';
  rec = new SR();
  rec.lang = LANG;
  rec.continuous = false;
  rec.interimResults = true;

  rec.onstart = function() {{
    isListen = true;
    micBtn.className = 'mic-btn mic-on';
    micBtn.innerHTML = '⏹';
    setPreview('<span class="ldot"></span><em style="color:#94a3b8;">Listening...</em>', 'listening');
  }};

  rec.onresult = function(e) {{
    var interim = '', final = '';
    for (var i = e.resultIndex; i < e.results.length; i++) {{
      var t = e.results[i][0].transcript;
      if (e.results[i].isFinal) {{ final += t; }} else {{ interim += t; }}
    }}
    if (final) {{
      finalTxt = final.trim();
      setPreview('✅ ' + escHtml(finalTxt), 'ready');
      sendBtn.className = 'send-btn show';
      startCountdown();
    }} else if (interim) {{
      setPreview('<span class="ldot"></span>' + escHtml(interim), 'listening');
    }}
  }};

  rec.onerror = function(e) {{
    isListen = false;
    resetMic();
    var m = {{'no-speech': '🔇 No speech detected', 'not-allowed': '🚫 Mic blocked', 'audio-capture': '🎤 No mic found'}};
    setPreview(m[e.error] || '⚠️ Error', '');
  }};

  rec.onend = function() {{ isListen = false; resetMic(); }};

  try {{ rec.start(); }} catch (ex) {{ setPreview('Error: ' + ex.message, ''); isListen = false; resetMic(); }}
}}

function stopMic() {{
  if (rec) {{ try {{ rec.stop(); }} catch (e) {{}} }}
  isListen = false;
  resetMic();
}}

function resetMic() {{
  micBtn.className = 'mic-btn mic-idle';
  micBtn.innerHTML = '🎙️';
}}

function startCountdown() {{
  cdLeft = {countdown_sec};
  cdPill.innerText = cdLeft + 's';
  cdPill.className = 'cd-pill on';
  cdTimer = setInterval(function() {{
    cdLeft--;
    cdPill.innerText = cdLeft + 's';
    if (cdLeft <= 0) {{ clearInterval(cdTimer); cdTimer = null; cdPill.className = 'cd-pill'; sendNow(); }}
  }}, 1000);
}}

function cancelCountdown() {{
  if (cdTimer) {{ clearInterval(cdTimer); cdTimer = null; }}
  cdPill.className = 'cd-pill';
}}

function sendNow() {{
  var text = finalTxt.trim();
  if (!text) return;
  cancelCountdown();
  sendBtn.className = 'send-btn';
  setPreview('⏳ Sending...', 'ready');

  var voiceText = 'VOICE::' + text;

  setTimeout(function() {{
    try {{
      var pd = window.parent.document;
      var ta = pd.querySelector('textarea[data-testid="stChatInputTextArea"]');
      if (!ta) ta = pd.querySelector('[data-testid="stChatInput"] textarea');
      if (!ta) ta = pd.querySelector('textarea');

      if (ta) {{
        var setter = Object.getOwnPropertyDescriptor(window.parent.HTMLTextAreaElement.prototype, 'value').set;
        setter.call(ta, voiceText);
        ta.dispatchEvent(new Event('input', {{bubbles: true}}));
        ta.dispatchEvent(new Event('change', {{bubbles: true}}));

        setTimeout(function() {{
          var btn = pd.querySelector('button[data-testid="stChatInputSubmitButton"]');
          if (!btn) btn = pd.querySelector('[data-testid="stChatInput"] button');
          if (btn) {{
            btn.click();
            setPreview('✅ Sent!', 'ready');
            setTimeout(function() {{ resetPreview(); finalTxt = ''; }}, 2000);
          }}
        }}, 200);
      }}
    }} catch (ex) {{ setPreview('⚠️ Type below and press Enter', ''); }}
  }}, 80);
}}

function escHtml(s) {{ return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }}
</script></body></html>"""

def render_tts_widget(text, language, gender):
    """Render TTS widget using components.html."""
    clean_text = strip_md_for_tts(text)
    safe_text = clean_text.replace("\\", "\\\\").replace("'", "\\'").replace("\n", " ")
    pitch = "1.1" if gender == "Female" else "0.88"
    lang_code = "en-IN" if language == "English" else "hi-IN" if language == "Hindi" else "te-IN"
    
    tts_html = f"""<!DOCTYPE html>
<html><head>
<style>
* {{box-sizing:border-box;margin:0;padding:0;font-family:'Inter',sans-serif;}}
body {{background:transparent;padding:8px 0;}}
.tts-widget {{
  background:linear-gradient(135deg,rgba(6,182,212,0.12),rgba(59,130,246,0.08));
  border:1px solid rgba(6,182,212,0.35);border-radius:12px;
  padding:12px 16px;display:flex;align-items:center;gap:12px;
}}
.tts-wave {{display:flex;align-items:flex-end;gap:3px;height:20px;}}
.tts-wave-bar {{width:3px;border-radius:2px;animation:wave 0.6s ease-in-out infinite;}}
.tts-wave-bar:nth-child(1){{height:6px;background:#06b6d4;animation-delay:0s;}}
.tts-wave-bar:nth-child(2){{height:14px;background:#3b82f6;animation-delay:0.12s;}}
.tts-wave-bar:nth-child(3){{height:9px;background:#06b6d4;animation-delay:0.24s;}}
.tts-wave-bar:nth-child(4){{height:16px;background:#a855f7;animation-delay:0.36s;}}
.tts-wave-bar:nth-child(5){{height:7px;background:#06b6d4;animation-delay:0.48s;}}
@keyframes wave {{0%,100%{{transform:scaleY(0.3);}}50%{{transform:scaleY(1.0);}}}}
.tts-label {{font-size:0.8125rem;color:#06b6d4;font-weight:600;flex:1;}}
.tts-stop {{
  background:rgba(30,41,59,0.8);border:1px solid rgba(51,65,85,0.6);
  color:#f59e0b;border-radius:50px;padding:4px 16px;font-size:0.75rem;
  cursor:pointer;font-weight:600;
}}
.tts-stop:hover {{background:rgba(51,65,85,0.9);color:#fbbf24;}}
</style></head><body>
<div class="tts-widget">
  <div class="tts-wave">
    <div class="tts-wave-bar"></div><div class="tts-wave-bar"></div>
    <div class="tts-wave-bar"></div><div class="tts-wave-bar"></div>
    <div class="tts-wave-bar"></div>
  </div>
  <span class="tts-label">🔊 Reading aloud...</span>
  <button class="tts-stop" onclick="stopTTS()">⏹ Stop</button>
</div>
<script>
function stopTTS() {{ if (window.speechSynthesis) window.speechSynthesis.cancel(); }}

function speak() {{
  if (!window.speechSynthesis) return;
  window.speechSynthesis.cancel();
  
  var text = '{safe_text}';
  if (!text || text.length < 2) return;
  
  var u = new SpeechSynthesisUtterance(text);
  u.lang = '{lang_code}';
  u.rate = 0.85;
  u.pitch = {pitch};
  u.volume = 1.0;
  
  function findVoice() {{
    var voices = window.speechSynthesis.getVoices();
    var lang = '{lang_code}'.substring(0,2);
    var priority = ['{lang_code}', lang+'-IN', 'en-IN', lang];
    for (var i=0; i<priority.length; i++) {{
      var v = voices.find(function(voice) {{ return voice.lang.toLowerCase().startsWith(priority[i].toLowerCase()); }});
      if (v) return v;
    }}
    return null;
  }}
  
  var voice = findVoice();
  if (voice) u.voice = voice;
  window.speechSynthesis.speak(u);
}}

setTimeout(function() {{
  var voices = window.speechSynthesis.getVoices();
  if (voices.length === 0) {{
    window.speechSynthesis.onvoiceschanged = function() {{ speak(); }};
  }} else {{
    speak();
  }}
}}, 400);
</script></body></html>"""
    
    components.html(tts_html, height=65, scrolling=False)

# ═══════════════════════════════════════════════════════════════════════════════
# 5. AI RESPONSE FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
def get_groq_response(prompt, student_class="10"):
    """Get AI response from Groq API."""
    if not groq_client:
        return "⚠️ API service unavailable. Please add GROQ_API_KEY to your environment."
    
    system_prompt = f"""You are an expert AI tutor for Class {student_class} students following the SCERT Telangana curriculum.

Guidelines:
- Explain concepts in simple, easy-to-understand language
- Use examples relevant to Indian context
- Keep responses concise but comprehensive (2-4 paragraphs)
- Encourage critical thinking
"""
    
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error: {str(e)}. Please check your API key."

# ═══════════════════════════════════════════════════════════════════════════════
# 6. RENDER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def render_message(content, msg_type="user"):
    """Render a chat message."""
    if msg_type == "user":
        st.markdown(f'<div class="chat-user">💬 {content}</div><div class="chat-clear"></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-ai">🎓 {content}</div><div class="chat-clear"></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 7. MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    """Main application function."""
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "selected_voice" not in st.session_state:
        st.session_state.selected_voice = "Male"
    if "selected_language" not in st.session_state:
        st.session_state.selected_language = "English"
    if "auto_speak" not in st.session_state:
        st.session_state.auto_speak = True
    if "usage_today" not in st.session_state:
        st.session_state.usage_today = 6
    if "last_tts_hash" not in st.session_state:
        st.session_state.last_tts_hash = ""
    
    # Load data
    data = load_data()
    user = data["users"]["student1"]
    daily_limit = data["settings"]["daily_limit"]
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SIDEBAR
    # ═══════════════════════════════════════════════════════════════════════════
    with st.sidebar:
        # Logo and title
        st.markdown(f"""
        <div style="text-align: center; padding: 1.5rem 0 1rem 0;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🎓</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: var(--text);">{data['settings']['school_name']}</div>
            <div style="font-size: 0.8rem; color: var(--text-muted);">Smart Tutor · 2025-26</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Student profile card
        usage_pct = (st.session_state.usage_today / daily_limit) * 100
        st.markdown(f"""
        <div class="sidebar-card">
            <div class="sidebar-header">👤 STUDENT</div>
            <div class="sidebar-title">{user['name']}</div>
            <div class="sidebar-subtitle">Class {user['class']} · {user['medium']}</div>
            <div style="margin-top: 0.75rem; font-size: 0.75rem; color: var(--text-muted);">
                Daily Usage: {st.session_state.usage_today}/{daily_limit}
            </div>
            <div class="usage-bar-track">
                <div class="usage-bar-fill" style="width: {usage_pct}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Voice Settings
        st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-header">🔊 Voice Settings</div>', unsafe_allow_html=True)
        
        st.markdown("**Voice:**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👩 Female", key="voice_female", use_container_width=True,
                        type="primary" if st.session_state.selected_voice == "Female" else "secondary"):
                st.session_state.selected_voice = "Female"
                st.rerun()
        with col2:
            if st.button("👨 Male", key="voice_male", use_container_width=True,
                        type="primary" if st.session_state.selected_voice == "Male" else "secondary"):
                st.session_state.selected_voice = "Male"
                st.rerun()
        
        st.markdown(f'<p style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.5rem;">Selected: <i>{st.session_state.selected_voice}</i></p>', unsafe_allow_html=True)
        
        # Language selector
        st.markdown("**🗣️ Voice Language**", unsafe_allow_html=True)
        LANGUAGE_OPTIONS = ["English", "Telugu", "Hindi"]
        lang = st.selectbox("", LANGUAGE_OPTIONS, 
                           index=LANGUAGE_OPTIONS.index(st.session_state.selected_language),
                           label_visibility="collapsed", key="lang_select")
        if lang != st.session_state.selected_language:
            st.session_state.selected_language = lang
            st.rerun()
        
        # Auto-speak toggle
        auto_speak = st.toggle("🎧 Auto-speak Responses", value=st.session_state.auto_speak, key="auto_speak_toggle")
        if auto_speak != st.session_state.auto_speak:
            st.session_state.auto_speak = auto_speak
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Try asking card
        st.markdown("""
        <div class="sidebar-card">
            <div class="sidebar-header">💡 Try asking:</div>
            <div style="font-size: 0.8rem; color: var(--text-muted); line-height: 1.6;">
                • Explain Ch1 Social Studies<br>
                • How to solve quadratic equations?<br>
                • What is photosynthesis?<br>
                • Explain democracy<br>
                • Climate of India summary
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        if st.button("🚪 Logout", key="logout", use_container_width=True):
            st.info("Logout functionality to be implemented")
        
        if st.button("🗑️ Clear Chat", key="clear_chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # MAIN CONTENT
    # ═══════════════════════════════════════════════════════════════════════════
    
    # Header
    st.markdown(f"""
    <div class="header-card">
        <div class="header-title">
            <span>🎓</span>
            <span>{data['settings']['school_name']} Smart Tutor</span>
        </div>
        <div class="header-subtitle">
            Hello {user['name']}! · Class {user['class']} · {user['board']} 2025-26
        </div>
        <div class="header-badges">
            <span class="badge badge-cyan">📅 {st.session_state.usage_today}/{daily_limit} TODAY</span>
            <span class="badge badge-purple">🔊 {st.session_state.selected_voice} · {st.session_state.selected_language}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat area
    chat_container = st.container()
    with chat_container:
        if len(st.session_state.messages) == 0:
            # Welcome screen
            st.markdown(f"""
            <div class="welcome-screen">
                <div class="welcome-icon">📚</div>
                <h2>Ready to learn, {user['name']}!</h2>
                <p>Tap 🎙️ mic to speak, or type below</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Display messages
            for msg in st.session_state.messages:
                render_message(msg["content"], msg["type"])
            
            # Show TTS widget for latest AI message (if voice input)
            if st.session_state.auto_speak and st.session_state.messages:
                for msg in reversed(st.session_state.messages):
                    if msg["type"] == "ai":
                        if msg.get("should_speak", False):
                            msg_hash = hashlib.md5(msg["content"].encode()).hexdigest()[:12]
                            if msg_hash != st.session_state.get("last_tts_hash", ""):
                                render_tts_widget(msg["content"], st.session_state.selected_language, st.session_state.selected_voice)
                                st.session_state["last_tts_hash"] = msg_hash
                        break
    
    # Mic component
    st.markdown("<br>", unsafe_allow_html=True)
    mic_html = get_mic_component_html(st.session_state.selected_language, countdown_sec=5)
    components.html(mic_html, height=70, scrolling=False)
    
    # Chat input
    user_input = st.chat_input(
        placeholder=f"💬 Type your question here... (Class {user['class']} · {st.session_state.selected_language})",
        key="chat_input"
    )
    
    # Handle message sending
    if user_input and user_input.strip():
        # Detect voice input
        raw = user_input.strip()
        is_voice = raw.startswith("VOICE::")
        clean_text = raw[len("VOICE::"):] if is_voice else raw
        
        # Add user message
        st.session_state.messages.append({
            "type": "user",
            "content": clean_text,
            "timestamp": datetime.datetime.now()
        })
        
        # Update usage
        st.session_state.usage_today += 1
        
        # Get AI response
        with st.spinner("🤔 AI is thinking..."):
            ai_response = get_groq_response(clean_text, student_class=user["class"])
        
        # Add AI message
        st.session_state.messages.append({
            "type": "ai",
            "content": ai_response,
            "timestamp": datetime.datetime.now(),
            "should_speak": is_voice
        })
        
        st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# 8. CSS INJECTION
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
    --primary: #06b6d4;
    --primary-dk: #0891b2;
    --accent: #22d3ee;
    --bg-dark: #0f1419;
    --bg-darker: #0a0e12;
    --bg-card: #1a1f26;
    --border: #2d3748;
    --text: #e2e8f0;
    --text-muted: #94a3b8;
    --success: #22c55e;
    --warning: #f59e0b;
    --radius: 12px;
}

*, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg-dark) !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--text) !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="stSidebar"] {
    background: var(--bg-darker) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] > div:first-child {
    background: var(--bg-darker) !important;
}

.block-container {
    padding: 2rem 3rem !important;
    max-width: 100% !important;
}

.header-card {
    background: linear-gradient(135deg, rgba(6, 182, 212, 0.1) 0%, rgba(59, 130, 246, 0.08) 100%);
    border: 1px solid rgba(6, 182, 212, 0.3);
    border-radius: var(--radius);
    padding: 1.5rem 2rem;
    margin-bottom: 2rem;
}

.header-title {
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--accent);
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.5rem;
}

.header-subtitle {
    color: var(--text-muted);
    font-size: 0.9rem;
}

.header-badges {
    display: flex;
    gap: 0.75rem;
    margin-top: 1rem;
}

.badge {
    display: inline-block;
    padding: 0.35rem 0.85rem;
    border-radius: 50px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.badge-cyan {
    background: rgba(6, 182, 212, 0.15);
    color: var(--accent);
    border: 1px solid rgba(6, 182, 212, 0.3);
}

.badge-purple {
    background: rgba(168, 85, 247, 0.15);
    color: #c084fc;
    border: 1px solid rgba(168, 85, 247, 0.3);
}

.chat-user {
    background: linear-gradient(135deg, #0891b2, #06b6d4);
    color: white;
    border-radius: 16px 16px 4px 16px;
    padding: 0.9rem 1.3rem;
    margin: 0.5rem 0 0.5rem 25%;
    max-width: 70%;
    float: right;
    clear: both;
    font-size: 0.95rem;
    box-shadow: 0 4px 12px rgba(6, 182, 212, 0.2);
}

.chat-ai {
    background: var(--bg-card);
    border: 1px solid var(--border);
    color: var(--text);
    border-radius: 16px 16px 16px 4px;
    padding: 0.9rem 1.3rem;
    margin: 0.5rem 25% 0.5rem 0;
    max-width: 70%;
    float: left;
    clear: both;
    font-size: 0.95rem;
}

.chat-clear {
    clear: both;
}

.welcome-screen {
    text-align: center;
    padding: 4rem 2rem;
    color: var(--text-muted);
}

.welcome-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
}

.welcome-screen h2 {
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 0.5rem;
}

.welcome-screen p {
    font-size: 0.95rem;
    color: var(--text-muted);
}

.sidebar-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem;
    margin-bottom: 1rem;
}

.sidebar-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.75rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.75rem;
    font-weight: 600;
}

.sidebar-title {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 0.25rem;
}

.sidebar-subtitle {
    font-size: 0.8rem;
    color: var(--text-muted);
}

.usage-bar-track {
    background: rgba(45, 55, 72, 0.5);
    border-radius: 50px;
    height: 6px;
    overflow: hidden;
    margin: 0.75rem 0 0.5rem 0;
}

.usage-bar-fill {
    height: 100%;
    border-radius: 50px;
    background: linear-gradient(90deg, var(--success), var(--primary));
    transition: width 0.5s ease;
}

.stButton > button {
    background: var(--bg-card) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    transition: all 0.2s !important;
}

.stButton > button:hover {
    background: rgba(6, 182, 212, 0.1) !important;
    border-color: var(--primary) !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--primary), var(--primary-dk)) !important;
    border: none !important;
    color: white !important;
}

.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, var(--accent), var(--primary)) !important;
}

.stSelectbox > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}

[data-testid="stChatInput"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
}

[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: var(--text) !important;
}

::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

::-webkit-scrollbar-track {
    background: var(--bg-dark);
}

::-webkit-scrollbar-thumb {
    background: var(--border);
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--primary);
}

hr {
    border-color: var(--border) !important;
    margin: 1.5rem 0 !important;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 9. RUN APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    main()
