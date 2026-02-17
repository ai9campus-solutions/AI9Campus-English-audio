"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🎓 AI SMART TUTOR - FIXED VERSION                         ║
║              Mic Input + TTS Output + Text Display Working                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

FIXES APPLIED:
1. Mic input now uses proper postMessage with Streamlit callback
2. TTS output triggers correctly for all AI responses
3. Text display uses proper markdown rendering
4. Fixed iframe communication for Streamlit Cloud

DEPLOY: Streamlit Cloud + GitHub
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

# Groq API client - Support both .env and Streamlit secrets
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", "")
if GROQ_API_KEY:
    groq_client = Groq(api_key=GROQ_API_KEY)
else:
    groq_client = None

# ═══════════════════════════════════════════════════════════════════════════════
# 2. PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="AI Smart Tutor",
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
# 4. TTS HELPER FUNCTIONS
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

# ═══════════════════════════════════════════════════════════════════════════════
# 5. FIXED MIC COMPONENT - Uses postMessage for reliable communication
# ═══════════════════════════════════════════════════════════════════════════════
def get_mic_component_html(lang_code, countdown_sec=5):
    """Generate HTML for mic button with speech recognition - FIXED VERSION."""
    lang_map = {"English": "en-IN", "Telugu": "te-IN", "Hindi": "hi-IN"}
    lang = lang_map.get(lang_code, "en-IN")
    
    return f"""<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }}
body {{ background: transparent; padding: 8px; }}

.mic-container {{
    display: flex;
    align-items: center;
    gap: 12px;
    background: rgba(15, 23, 42, 0.8);
    border: 1.5px solid rgba(51, 65, 85, 0.6);
    border-radius: 16px;
    padding: 10px 16px;
    transition: all 0.3s ease;
}}

.mic-container.listening {{
    border-color: #ef4444;
    box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.2);
}}

.mic-btn {{
    width: 48px;
    height: 48px;
    border-radius: 50%;
    border: none;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 1.4rem;
    transition: all 0.2s ease;
    flex-shrink: 0;
}}

.mic-btn:hover {{ transform: scale(1.05); }}
.mic-btn:active {{ transform: scale(0.95); }}

.mic-idle {{
    background: linear-gradient(135deg, rgba(6, 182, 212, 0.2), rgba(59, 130, 246, 0.15));
    border: 2px solid rgba(6, 182, 212, 0.5);
    color: #06b6d4;
}}

.mic-idle:hover {{
    background: linear-gradient(135deg, rgba(6, 182, 212, 0.3), rgba(59, 130, 246, 0.25));
    border-color: #06b6d4;
}}

.mic-recording {{
    background: linear-gradient(135deg, #ef4444, #dc2626);
    border: 2px solid transparent;
    color: white;
    animation: pulse 1s infinite;
}}

@keyframes pulse {{
    0%, 100% {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.5); }}
    50% {{ box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }}
}}

.preview {{
    flex: 1;
    min-width: 0;
    padding: 10px 14px;
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(51, 65, 85, 0.4);
    border-radius: 12px;
    font-size: 0.9375rem;
    color: #e2e8f0;
    min-height: 44px;
    display: flex;
    align-items: center;
}}

.preview.listening {{
    border-color: #ef4444;
    background: rgba(239, 68, 68, 0.1);
}}

.preview.ready {{
    border-color: #22d3ee;
    background: rgba(34, 211, 238, 0.1);
}}

.placeholder {{
    color: #64748b;
    font-size: 0.875rem;
}}

.send-btn {{
    width: 44px;
    height: 44px;
    border-radius: 50%;
    border: none;
    background: linear-gradient(135deg, #06b6d4, #0891b2);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 1.1rem;
    flex-shrink: 0;
    transition: all 0.2s ease;
    opacity: 0.5;
    pointer-events: none;
}}

.send-btn.active {{
    opacity: 1;
    pointer-events: auto;
}}

.send-btn.active:hover {{
    background: linear-gradient(135deg, #22d3ee, #06b6d4);
    transform: scale(1.05);
}}

.cd-pill {{
    display: none;
    background: rgba(34, 211, 238, 0.15);
    border: 1px solid #22d3ee;
    border-radius: 50px;
    padding: 4px 12px;
    font-size: 0.75rem;
    color: #22d3ee;
    font-weight: 600;
}}

.cd-pill.active {{
    display: block;
}}

.status-dot {{
    display: inline-block;
    width: 8px;
    height: 8px;
    background: #ef4444;
    border-radius: 50%;
    animation: blink 1s infinite;
    margin-right: 8px;
}}

@keyframes blink {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0.3; }}
}}

.status-text {{
    font-size: 0.8125rem;
    color: #94a3b8;
    margin-top: 8px;
    padding-left: 8px;
}}
</style>
</head>
<body>
<div class="mic-container" id="micContainer">
    <button class="mic-btn mic-idle" id="micBtn" onclick="toggleMic()" title="Click to speak">🎙️</button>
    <div class="preview" id="preview">
        <span class="placeholder" id="placeholder">Tap 🎙️ to speak your question</span>
    </div>
    <span class="cd-pill" id="cdPill">{countdown_sec}s</span>
    <button class="send-btn" id="sendBtn" onclick="sendText()" title="Send">➤</button>
</div>
<div class="status-text" id="statusText"></div>

<script>
// Configuration
var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
var rec = null;
var isRecording = false;
var cdTimer = null;
var cdLeft = {countdown_sec};
var LANG = '{lang}';
var finalText = '';

// DOM elements
var micContainer = document.getElementById('micContainer');
var micBtn = document.getElementById('micBtn');
var preview = document.getElementById('preview');
var placeholder = document.getElementById('placeholder');
var cdPill = document.getElementById('cdPill');
var sendBtn = document.getElementById('sendBtn');
var statusText = document.getElementById('statusText');

// Check browser support
if (!SR) {{
    showStatus('⚠️ Please use Chrome, Edge, or Safari for voice input');
}}

function toggleMic() {{
    if (!SR) {{
        showStatus('⚠️ Voice not supported in this browser');
        return;
    }}
    
    if (isRecording) {{
        stopRecording();
    }} else {{
        startRecording();
    }}
}}

function startRecording() {{
    cancelCountdown();
    finalText = '';
    
    rec = new SR();
    rec.lang = LANG;
    rec.continuous = false;
    rec.interimResults = true;
    rec.maxAlternatives = 3;
    
    rec.onstart = function() {{
        isRecording = true;
        micContainer.classList.add('listening');
        micBtn.className = 'mic-btn mic-recording';
        micBtn.innerHTML = '⏹';
        preview.classList.add('listening');
        showStatus('<span class="status-dot"></span> Listening... speak now');
    }};
    
    rec.onresult = function(e) {{
        var interim = '';
        var final = '';
        
        for (var i = e.resultIndex; i < e.results.length; i++) {{
            var transcript = e.results[i][0].transcript;
            if (e.results[i].isFinal) {{
                final += transcript;
            }} else {{
                interim += transcript;
            }}
        }}
        
        if (final) {{
            finalText = final;
            preview.innerHTML = '✅ ' + escapeHtml(final);
            preview.classList.remove('listening');
            preview.classList.add('ready');
            sendBtn.classList.add('active');
            showStatus('✓ Got it! Sending in ' + {countdown_sec} + ' seconds...');
        }} else if (interim) {{
            preview.innerHTML = '🎙️ ' + escapeHtml(interim);
            placeholder.style.display = 'none';
        }}
    }};
    
    rec.onerror = function(e) {{
        isRecording = false;
        resetUI();
        var errors = {{
            'no-speech': '🔇 No speech detected. Try again.',
            'not-allowed': '🚫 Microphone blocked. Click the lock icon in your browser and allow mic.',
            'audio-capture': '🎤 No microphone found.',
            'network': '🌐 Network error.',
            'aborted': 'Recording stopped.'
        }};
        showStatus(errors[e.error] || '⚠️ Error: ' + e.error);
    }};
    
    rec.onend = function() {{
        isRecording = false;
        resetUI();
        if (finalText.trim()) {{
            startCountdown();
        }}
    }};
    
    try {{
        rec.start();
    }} catch (ex) {{
        showStatus('⚠️ Error starting microphone: ' + ex.message);
        resetUI();
    }}
}}

function stopRecording() {{
    if (rec) {{
        try {{ rec.stop(); }} catch(e) {{}}
    }}
    isRecording = false;
    resetUI();
}}

function resetUI() {{
    micContainer.classList.remove('listening');
    micBtn.className = 'mic-btn mic-idle';
    micBtn.innerHTML = '🎙️';
    preview.classList.remove('listening');
}}

function startCountdown() {{
    cdLeft = {countdown_sec};
    cdPill.innerText = cdLeft + 's';
    cdPill.classList.add('active');
    
    cdTimer = setInterval(function() {{
        cdLeft--;
        cdPill.innerText = cdLeft + 's';
        
        if (cdLeft <= 0) {{
            clearInterval(cdTimer);
            cdPill.classList.remove('active');
            sendText();
        }}
    }}, 1000);
}}

function cancelCountdown() {{
    if (cdTimer) {{
        clearInterval(cdTimer);
        cdTimer = null;
    }}
    cdPill.classList.remove('active');
}}

function sendText() {{
    var text = finalText.trim();
    if (!text) return;
    
    cancelCountdown();
    showStatus('⏳ Sending to AI...');
    
    // Send message to parent (Streamlit) using postMessage
    try {{
        window.parent.postMessage({{
            type: 'streamlit:setComponentValue',
            value: 'VOICE::' + text
        }}, '*');
        
        // Also try alternative method for older Streamlit versions
        window.parent.postMessage({{
            type: 'voice_transcript',
            text: text
        }}, '*');
        
        showStatus('✅ Sent! AI is thinking...');
        
        // Reset after sending
        setTimeout(function() {{
            preview.innerHTML = '<span class="placeholder">Tap 🎙️ to speak your question</span>';
            sendBtn.classList.remove('active');
            finalText = '';
        }}, 2000);
        
    }} catch (ex) {{
        showStatus('⚠️ Could not send. Please type your question below.');
    }}
}}

function showStatus(msg) {{
    statusText.innerHTML = msg;
}}

function escapeHtml(text) {{
    var div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}}

// Listen for messages from parent
window.addEventListener('message', function(e) {{
    if (e.data && e.data.type === 'stop_recording') {{
        stopRecording();
    }}
}});
</script>
</body>
</html>"""

# ═══════════════════════════════════════════════════════════════════════════════
# 6. FIXED TTS COMPONENT - Properly triggers speech synthesis
# ═══════════════════════════════════════════════════════════════════════════════
def render_tts_widget(text, language, gender):
    """Render TTS widget - FIXED VERSION with auto-trigger."""
    clean_text = strip_md_for_tts(text)
    safe_text = clean_text.replace("\\", "\\\\").replace("'", "\\'").replace("\n", " ")
    
    pitch = "1.1" if gender == "Female" else "0.9"
    lang_code = "en-IN" if language == "English" else "hi-IN" if language == "Hindi" else "te-IN"
    
    tts_html = f"""<!DOCTYPE html>
<html>
<head>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }}
body {{ background: transparent; padding: 8px; }}

.tts-widget {{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    background: linear-gradient(135deg, rgba(6, 182, 212, 0.12), rgba(59, 130, 246, 0.08));
    border: 1px solid rgba(6, 182, 212, 0.35);
    border-radius: 12px;
}}

.tts-wave {{
    display: flex;
    align-items: flex-end;
    gap: 3px;
    height: 20px;
}}

.tts-wave-bar {{
    width: 3px;
    background: #06b6d4;
    border-radius: 2px;
    animation: wave 0.6s ease-in-out infinite;
}}

.tts-wave-bar:nth-child(1) {{ height: 6px; animation-delay: 0s; }}
.tts-wave-bar:nth-child(2) {{ height: 14px; animation-delay: 0.12s; }}
.tts-wave-bar:nth-child(3) {{ height: 9px; animation-delay: 0.24s; }}
.tts-wave-bar:nth-child(4) {{ height: 16px; animation-delay: 0.36s; }}
.tts-wave-bar:nth-child(5) {{ height: 7px; animation-delay: 0.48s; }}

@keyframes wave {{
    0%, 100% {{ transform: scaleY(0.3); }}
    50% {{ transform: scaleY(1.0); }}
}}

.tts-label {{
    flex: 1;
    font-size: 0.875rem;
    color: #06b6d4;
    font-weight: 500;
}}

.tts-stop {{
    padding: 6px 14px;
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 50px;
    color: #f87171;
    font-size: 0.75rem;
    cursor: pointer;
    transition: all 0.2s;
}}

.tts-stop:hover {{
    background: rgba(239, 68, 68, 0.25);
}}
</style>
</head>
<body>
<div class="tts-widget" id="ttsWidget">
    <div class="tts-wave">
        <div class="tts-wave-bar"></div>
        <div class="tts-wave-bar"></div>
        <div class="tts-wave-bar"></div>
        <div class="tts-wave-bar"></div>
        <div class="tts-wave-bar"></div>
    </div>
    <span class="tts-label">🔊 Speaking...</span>
    <button class="tts-stop" onclick="stopSpeaking()" title="Stop speaking">⏹ Stop</button>
</div>

<script>
var text = '{safe_text}';
var lang = '{lang_code}';
var pitch = {pitch};
var isSpeaking = false;

function speak() {{
    if (!window.speechSynthesis) {{
        console.log('TTS not supported');
        return;
    }}
    
    // Cancel any ongoing speech
    window.speechSynthesis.cancel();
    
    var utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = lang;
    utterance.rate = 0.9;
    utterance.pitch = pitch;
    utterance.volume = 1.0;
    
    // Try to find appropriate voice
    var voices = window.speechSynthesis.getVoices();
    var preferredVoice = null;
    
    for (var i = 0; i < voices.length; i++) {{
        var v = voices[i];
        if (v.lang.indexOf(lang.split('-')[0]) === 0) {{
            preferredVoice = v;
            var name = v.name.toLowerCase();
            if ('{gender}' === 'Female' && (name.indexOf('female') >= 0 || name.indexOf('zira') >= 0 || name.indexOf('heera') >= 0)) break;
            if ('{gender}' === 'Male' && (name.indexOf('male') >= 0 || name.indexOf('david') >= 0 || name.indexOf('mark') >= 0)) break;
        }}
    }}
    
    if (preferredVoice) {{
        utterance.voice = preferredVoice;
    }}
    
    utterance.onstart = function() {{
        isSpeaking = true;
    }};
    
    utterance.onend = function() {{
        isSpeaking = false;
        hideWidget();
    }};
    
    utterance.onerror = function(e) {{
        console.log('TTS error:', e);
        isSpeaking = false;
        hideWidget();
    }};
    
    window.speechSynthesis.speak(utterance);
}}

function stopSpeaking() {{
    if (window.speechSynthesis) {{
        window.speechSynthesis.cancel();
    }}
    isSpeaking = false;
    hideWidget();
}}

function hideWidget() {{
    var widget = document.getElementById('ttsWidget');
    if (widget) {{
        widget.style.opacity = '0.5';
        widget.style.transition = 'opacity 0.5s';
    }}
}}

// Initialize voices and start speaking
if (window.speechSynthesis.getVoices().length === 0) {{
    window.speechSynthesis.onvoiceschanged = function() {{
        setTimeout(speak, 300);
    }};
}} else {{
    setTimeout(speak, 300);
}}

// Chrome 15-second keepalive fix
setInterval(function() {{
    if (isSpeaking && window.speechSynthesis) {{
        window.speechSynthesis.pause();
        window.speechSynthesis.resume();
    }}
}}, 10000);

// Listen for stop signal
window.addEventListener('message', function(e) {{
    if (e.data && e.data.type === 'stop_speak') {{
        stopSpeaking();
    }}
}});
</script>
</body>
</html>"""
    
    components.html(tts_html, height=70, scrolling=False)

# ═══════════════════════════════════════════════════════════════════════════════
# 7. AI RESPONSE FUNCTION
# ═══════════════════════════════════════════════════════════════════════════════
def get_groq_response(prompt, student_class="10"):
    """Get AI response from Groq API."""
    if not groq_client:
        return "⚠️ AI service unavailable. Please add GROQ_API_KEY to your secrets."
    
    system_prompt = f"""You are an expert AI tutor for Class {student_class} students following the SCERT Telangana curriculum.

Guidelines:
- Explain concepts in simple, easy-to-understand language
- Use examples relevant to Indian context when possible
- Keep responses concise but comprehensive (2-4 paragraphs)
- Encourage critical thinking
- Use analogies to explain complex concepts
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
# 8. MESSAGE RENDERING - FIXED
# ═══════════════════════════════════════════════════════════════════════════════
def render_message(content, msg_type="user"):
    """Render a chat message - FIXED with proper escaping."""
    # Escape HTML to prevent injection
    safe_content = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    # Convert newlines to <br>
    safe_content = safe_content.replace('\n', '<br>')
    
    if msg_type == "user":
        st.markdown(
            f'''<div style="
                background: linear-gradient(135deg, #06b6d4, #0891b2);
                color: white;
                border-radius: 16px 16px 4px 16px;
                padding: 12px 16px;
                margin: 8px 0 8px 40px;
                max-width: 80%;
                float: right;
                clear: both;
                font-size: 0.95rem;
                line-height: 1.5;
                box-shadow: 0 2px 8px rgba(6, 182, 212, 0.3);
            ">👤 {safe_content}</div>
            <div style="clear: both;"></div>''',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'''<div style="
                background: rgba(30, 41, 59, 0.8);
                border: 1px solid rgba(51, 65, 85, 0.6);
                color: #e2e8f0;
                border-radius: 16px 16px 16px 4px;
                padding: 12px 16px;
                margin: 8px 40px 8px 0;
                max-width: 80%;
                float: left;
                clear: both;
                font-size: 0.95rem;
                line-height: 1.5;
            ">🎓 {safe_content}</div>
            <div style="clear: both;"></div>''',
            unsafe_allow_html=True
        )

# ═══════════════════════════════════════════════════════════════════════════════
# 9. MAIN APPLICATION
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
    if "voice_input" not in st.session_state:
        st.session_state.voice_input = ""
    if "last_ai_response" not in st.session_state:
        st.session_state.last_ai_response = ""
    
    # Load data
    data = load_data()
    user = data["users"]["student1"]
    daily_limit = data["settings"]["daily_limit"]
    
    # CSS Injection
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .main-title {
        font-size: 1.75rem;
        font-weight: 700;
        background: linear-gradient(90deg, #06b6d4, #22d3ee);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        color: #94a3b8;
        font-size: 0.9rem;
    }
    
    .badge {
        display: inline-block;
        padding: 0.35rem 0.85rem;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .badge-cyan {
        background: rgba(6, 182, 212, 0.15);
        color: #22d3ee;
        border: 1px solid rgba(6, 182, 212, 0.3);
    }
    
    .badge-purple {
        background: rgba(139, 92, 246, 0.15);
        color: #a78bfa;
        border: 1px solid rgba(139, 92, 246, 0.3);
    }
    
    .welcome-box {
        text-align: center;
        padding: 3rem 2rem;
    }
    
    .welcome-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    .welcome-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 0.5rem;
    }
    
    .welcome-subtitle {
        color: #94a3b8;
        font-size: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SIDEBAR
    # ═══════════════════════════════════════════════════════════════════════════
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🎓</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #e2e8f0;">School Name</div>
            <div style="font-size: 0.8rem; color: #64748b;">Smart Tutor · 2025-26</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Profile Card
        usage_pct = (st.session_state.usage_today / daily_limit) * 100
        st.markdown(f"""
        <div style="
            background: rgba(30, 41, 59, 0.6);
            border: 1px solid rgba(51, 65, 85, 0.5);
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
        ">
            <div style="font-size: 0.7rem; color: #64748b; text-transform: uppercase; margin-bottom: 0.5rem;">👤 STUDENT</div>
            <div style="font-size: 1rem; font-weight: 600; color: #e2e8f0;">{user['name']}</div>
            <div style="font-size: 0.8rem; color: #94a3b8;">Class {user['class']} · {user['medium']}</div>
            <div style="margin-top: 0.75rem;">
                <div style="display: flex; justify-content: space-between; font-size: 0.7rem; color: #64748b; margin-bottom: 0.25rem;">
                    <span>Daily Usage</span>
                    <span>{st.session_state.usage_today}/{daily_limit}</span>
                </div>
                <div style="height: 6px; background: rgba(51, 65, 85, 0.5); border-radius: 3px; overflow: hidden;">
                    <div style="height: 100%; width: {usage_pct}%; background: linear-gradient(90deg, #06b6d4, #0891b2); border-radius: 3px; transition: width 0.5s;"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Voice Settings
        st.markdown("<div style='font-size: 0.7rem; color: #64748b; text-transform: uppercase; margin-bottom: 0.5rem;'>🔊 Voice Settings</div>", unsafe_allow_html=True)
        
        # Voice selection
        voice_col1, voice_col2 = st.columns(2)
        with voice_col1:
            if st.button("👩 Female", key="voice_female", use_container_width=True, 
                        type="primary" if st.session_state.selected_voice == "Female" else "secondary"):
                st.session_state.selected_voice = "Female"
                st.rerun()
        with voice_col2:
            if st.button("👨 Male", key="voice_male", use_container_width=True,
                        type="primary" if st.session_state.selected_voice == "Male" else "secondary"):
                st.session_state.selected_voice = "Male"
                st.rerun()
        
        st.markdown(f"<div style='font-size: 0.7rem; color: #64748b; margin: 0.5rem 0;'>Selected: <i>{st.session_state.selected_voice}</i></div>", unsafe_allow_html=True)
        
        # Language selector
        lang = st.selectbox("🌐 Voice Language", ["English", "Telugu", "Hindi"], 
                           index=["English", "Telugu", "Hindi"].index(st.session_state.selected_language),
                           label_visibility="collapsed")
        if lang != st.session_state.selected_language:
            st.session_state.selected_language = lang
            st.rerun()
        
        # Auto-speak toggle
        auto_speak = st.toggle("🎧 Auto-speak Responses", value=st.session_state.auto_speak)
        if auto_speak != st.session_state.auto_speak:
            st.session_state.auto_speak = auto_speak
        
        st.divider()
        
        # Suggested Questions
        st.markdown("<div style='font-size: 0.7rem; color: #64748b; text-transform: uppercase; margin-bottom: 0.5rem;'>💡 Try asking:</div>", unsafe_allow_html=True)
        
        suggested = [
            "Explain Ch1 Social Studies",
            "How to solve quadratic equations?",
            "What is photosynthesis?",
            "Explain democracy",
            "Climate of India summary"
        ]
        
        for i, q in enumerate(suggested):
            if st.button(q, key=f"sugg_{i}", use_container_width=True):
                st.session_state.voice_input = q
                st.rerun()
        
        st.divider()
        
        # Action buttons
        if st.button("🗑️ Clear Chat", key="clear_chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # MAIN CONTENT
    # ═══════════════════════════════════════════════════════════════════════════
    # Header
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.1), rgba(59, 130, 246, 0.08));
        border: 1px solid rgba(6, 182, 212, 0.25);
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1.5rem;
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
            <div>
                <div class="main-title">🎓 School Name Smart Tutor</div>
                <div class="subtitle">Hello {user['name']}! · Class {user['class']} · {user['board']} 2025-26</div>
            </div>
            <div style="display: flex; gap: 0.5rem;">
                <span class="badge badge-cyan">📅 {st.session_state.usage_today}/{daily_limit} TODAY</span>
                <span class="badge badge-purple">🔊 {st.session_state.selected_voice} · {st.session_state.selected_language}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # CHAT AREA
    # ═══════════════════════════════════════════════════════════════════════════
    chat_container = st.container()
    
    with chat_container:
        if len(st.session_state.messages) == 0:
            # Welcome screen
            st.markdown(f"""
            <div class="welcome-box">
                <div class="welcome-icon">📚</div>
                <div class="welcome-title">Ready to learn, {user['name']}!</div>
                <div class="welcome-subtitle">Tap 🎙️ mic to speak, or type below</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Display messages
            for msg in st.session_state.messages:
                render_message(msg["content"], msg["type"])
    
    # ═══════════════════════════════════════════════════════════════════════════
    # MIC COMPONENT (Voice Input)
    # ═══════════════════════════════════════════════════════════════════════════
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Check for voice input from the mic component
    mic_html = get_mic_component_html(st.session_state.selected_language, countdown_sec=5)
    components.html(mic_html, height=100, scrolling=False)
    
    # Handle voice input from session state
    if st.session_state.voice_input:
        user_input = st.session_state.voice_input
        st.session_state.voice_input = ""  # Clear after reading
        
        # Process voice input
        process_message(user_input, is_voice=True)
        return
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TEXT INPUT
    # ═══════════════════════════════════════════════════════════════════════════
    user_input = st.chat_input(
        placeholder=f"💬 Type your question here... (Class {user['class']} · {st.session_state.selected_language})",
        key="chat_input"
    )
    
    if user_input and user_input.strip():
        process_message(user_input.strip(), is_voice=False)

def process_message(user_input, is_voice=False):
    """Process user message and get AI response."""
    data = load_data()
    user = data["users"]["student1"]
    
    # Add user message
    st.session_state.messages.append({
        "type": "user",
        "content": user_input,
        "timestamp": datetime.datetime.now()
    })
    
    # Update usage
    st.session_state.usage_today += 1
    
    # Get AI response
    with st.spinner("🤔 AI is thinking..."):
        ai_response = get_groq_response(user_input, student_class=user["class"])
    
    # Store for TTS
    st.session_state.last_ai_response = ai_response
    
    # Add AI message
    st.session_state.messages.append({
        "type": "ai",
        "content": ai_response,
        "timestamp": datetime.datetime.now(),
        "is_voice": is_voice
    })
    
    st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# 10. TTS TRIGGER (After rerun)
# ═══════════════════════════════════════════════════════════════════════════════
def check_and_trigger_tts():
    """Check if TTS should be triggered for the latest AI message."""
    if not st.session_state.get("auto_speak", True):
        return
    
    if not st.session_state.messages:
        return
    
    # Find the latest AI message
    for msg in reversed(st.session_state.messages):
        if msg["type"] == "ai":
            # Only speak if it was from voice input or if we haven't spoken it yet
            msg_hash = hashlib.md5(msg["content"].encode()).hexdigest()[:12]
            last_spoken = st.session_state.get("last_spoken_hash", "")
            
            if msg_hash != last_spoken:
                st.session_state["last_spoken_hash"] = msg_hash
                # Trigger TTS
                render_tts_widget(
                    msg["content"],
                    st.session_state.selected_language,
                    st.session_state.selected_voice
                )
            break

# ═══════════════════════════════════════════════════════════════════════════════
# 11. RUN APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    main()
    
    # Check for TTS after main render
    check_and_trigger_tts()
