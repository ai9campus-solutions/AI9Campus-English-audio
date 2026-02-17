"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🎓 AI SMART TUTOR - PREMIUM EDITION                       ║
║              Single-Screen Glassmorphism Design with Classroom BG            ║
╚══════════════════════════════════════════════════════════════════════════════╝

FEATURES:
- Full-screen futuristic classroom background with gradient overlays
- Glassmorphism UI (frosted glass panels)
- Voice input with speech recognition
- Text-to-Speech (TTS) with Indian voices
- Groq AI integration for educational responses
- Single-screen layout (chat area scrolls, rest fixed)
- Real-time chat with animated message bubbles
- Daily usage tracking
- Responsive design

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
import base64
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
# 2. PAGE CONFIGURATION - SINGLE SCREEN FULL WIDTH
# ═══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="AI Smart Tutor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════════════════════════════════════════════
# 3. BACKGROUND IMAGE ENCODER
# ═══════════════════════════════════════════════════════════════════════════════
def get_base64_image(image_path):
    """Convert image to base64 for CSS background."""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

# ═══════════════════════════════════════════════════════════════════════════════
# 4. PREMIUM CUSTOM CSS - GLASSMORPHISM + CLASSROOM BACKGROUND
# ═══════════════════════════════════════════════════════════════════════════════
def inject_premium_css():
    """Inject premium glassmorphism CSS with classroom background."""
    
    # Try to load local background image, fallback to URL
    bg_image_base64 = get_base64_image("classroom_bg.jpg")
    
    if bg_image_base64:
        bg_style = f"""
        background-image: 
            linear-gradient(135deg, rgba(13, 17, 35, 0.92) 0%, rgba(15, 23, 42, 0.88) 50%, rgba(13, 17, 35, 0.92) 100%),
            linear-gradient(to top, rgba(6, 182, 212, 0.15) 0%, transparent 50%),
            url('data:image/jpeg;base64,{bg_image_base64}');
        """
    else:
        # Fallback - use a dark gradient if image not found
        bg_style = """
        background-image: 
            linear-gradient(135deg, rgba(13, 17, 35, 0.98) 0%, rgba(15, 23, 42, 0.95) 50%, rgba(13, 17, 35, 0.98) 100%),
            radial-gradient(ellipse at 20% 20%, rgba(6, 182, 212, 0.15) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 80%, rgba(59, 130, 246, 0.1) 0%, transparent 50%);
        """
    
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* ═══════════════════════════════════════════════════════════════════════
       ROOT VARIABLES - CYAN/BLUE PREMIUM THEME
       ═══════════════════════════════════════════════════════════════════════ */
    :root {{
        --primary:      #06b6d4;
        --primary-dk:   #0891b2;
        --primary-lg:   #22d3ee;
        --accent:       #3b82f6;
        --accent-lg:    #60a5fa;
        --success:      #10b981;
        --warning:      #f59e0b;
        --danger:       #ef4444;
        --bg-dark:      #0f172a;
        --bg-panel:     rgba(15, 23, 42, 0.75);
        --bg-card:      rgba(30, 41, 59, 0.6);
        --border:       rgba(255, 255, 255, 0.1);
        --border-hover: rgba(6, 182, 212, 0.4);
        --text:         #f8fafc;
        --text-muted:   #94a3b8;
        --radius:       16px;
        --radius-sm:    12px;
        --shadow:       0 8px 32px rgba(0, 0, 0, 0.4);
        --shadow-glow:  0 0 40px rgba(6, 182, 212, 0.2);
    }}
    
    /* ═══════════════════════════════════════════════════════════════════════
       BASE STYLES & BACKGROUND
       ═══════════════════════════════════════════════════════════════════════ */
    *, *::before, *::after {{ 
        box-sizing: border-box; 
        margin: 0; 
        padding: 0; 
    }}
    
    html, body {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: var(--text) !important;
        overflow: hidden !important;
    }}
    
    [data-testid="stAppViewContainer"] {{
        {bg_style}
        background-size: cover, cover, cover;
        background-position: center, center, center;
        background-attachment: fixed;
        background-repeat: no-repeat;
        min-height: 100vh !important;
    }}
    
    /* Hide default Streamlit elements */
    [data-testid="stHeader"] {{ display: none !important; }}
    [data-testid="stToolbar"] {{ display: none !important; }}
    #MainMenu {{ display: none !important; }}
    footer {{ display: none !important; }}
    
    /* ═══════════════════════════════════════════════════════════════════════
       GLASSMORPHISM PANEL
       ═══════════════════════════════════════════════════════════════════════ */
    .glass-panel {{
        background: var(--bg-panel) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius) !important;
        box-shadow: var(--shadow) !important;
    }}
    
    .glass-card {{
        background: var(--bg-card) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    .glass-card:hover {{
        border-color: var(--border-hover) !important;
        box-shadow: var(--shadow-glow) !important;
        transform: translateY(-2px);
    }}
    
    /* ═══════════════════════════════════════════════════════════════════════
       MAIN LAYOUT - SINGLE SCREEN
       ═══════════════════════════════════════════════════════════════════════ */
    .main-container {{
        display: flex;
        flex-direction: column;
        height: 100vh;
        max-height: 100vh;
        overflow: hidden;
        padding: 0 !important;
    }}
    
    .header-section {{
        flex-shrink: 0;
        padding: 1rem 1.5rem;
        margin: 0.5rem 1rem 0 1rem;
    }}
    
    .content-section {{
        flex: 1;
        display: flex;
        gap: 1rem;
        padding: 0 1rem 0.5rem 1rem;
        overflow: hidden;
        min-height: 0;
    }}
    
    .sidebar-panel {{
        width: 320px;
        flex-shrink: 0;
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
        overflow-y: auto;
        padding-right: 0.25rem;
    }}
    
    .chat-panel {{
        flex: 1;
        display: flex;
        flex-direction: column;
        min-width: 0;
        overflow: hidden;
    }}
    
    .input-section {{
        flex-shrink: 0;
        padding: 0.75rem 1rem 1rem 1rem;
    }}
    
    /* ═══════════════════════════════════════════════════════════════════════
       HEADER STYLES
       ═══════════════════════════════════════════════════════════════════════ */
    .header-logo {{
        display: flex;
        align-items: center;
        gap: 0.875rem;
    }}
    
    .logo-icon {{
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, var(--primary), var(--accent));
        border-radius: var(--radius-sm);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        box-shadow: 0 4px 20px rgba(6, 182, 212, 0.35);
    }}
    
    .logo-text h1 {{
        font-size: 1.375rem;
        font-weight: 700;
        color: var(--text);
        margin: 0;
        line-height: 1.2;
    }}
    
    .logo-text h1 span {{
        background: linear-gradient(90deg, var(--primary-lg), var(--accent-lg));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    
    .logo-text p {{
        font-size: 0.8125rem;
        color: var(--text-muted);
        margin: 0;
    }}
    
    .header-badges {{
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }}
    
    .badge {{
        display: inline-flex;
        align-items: center;
        gap: 0.375rem;
        padding: 0.375rem 0.875rem;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 600;
    }}
    
    .badge-cyan {{
        background: rgba(6, 182, 212, 0.15);
        color: var(--primary-lg);
        border: 1px solid rgba(6, 182, 212, 0.3);
    }}
    
    .badge-purple {{
        background: rgba(139, 92, 246, 0.15);
        color: #a78bfa;
        border: 1px solid rgba(139, 92, 246, 0.3);
    }}
    
    /* ═══════════════════════════════════════════════════════════════════════
       SIDEBAR STYLES
       ═══════════════════════════════════════════════════════════════════════ */
    .profile-card {{
        padding: 1.25rem;
    }}
    
    .profile-header {{
        display: flex;
        align-items: center;
        gap: 0.875rem;
        margin-bottom: 1rem;
    }}
    
    .profile-avatar {{
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, var(--primary), var(--accent));
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        font-weight: 600;
        color: white;
        border: 2px solid rgba(255, 255, 255, 0.2);
    }}
    
    .profile-info h3 {{
        font-size: 1rem;
        font-weight: 600;
        color: var(--text);
        margin: 0;
    }}
    
    .profile-info p {{
        font-size: 0.75rem;
        color: var(--text-muted);
        margin: 0.125rem 0 0 0;
    }}
    
    .usage-bar-container {{
        margin-top: 0.75rem;
    }}
    
    .usage-bar-header {{
        display: flex;
        justify-content: space-between;
        font-size: 0.6875rem;
        color: var(--text-muted);
        margin-bottom: 0.375rem;
    }}
    
    .usage-bar-track {{
        height: 6px;
        background: rgba(255, 255, 255, 0.08);
        border-radius: 3px;
        overflow: hidden;
    }}
    
    .usage-bar-fill {{
        height: 100%;
        background: linear-gradient(90deg, var(--primary), var(--accent));
        border-radius: 3px;
        transition: width 0.5s ease;
    }}
    
    .section-title {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.8125rem;
        font-weight: 600;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin: 0.5rem 0 0.75rem 0;
        padding: 0 0.5rem;
    }}
    
    /* Voice Settings */
    .voice-selector {{
        display: flex;
        gap: 0.5rem;
        margin-bottom: 0.75rem;
    }}
    
    .voice-btn {{
        flex: 1;
        padding: 0.625rem;
        border-radius: 10px;
        border: 1.5px solid var(--border);
        background: rgba(255, 255, 255, 0.03);
        color: var(--text-muted);
        font-size: 0.8125rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s;
        text-align: center;
    }}
    
    .voice-btn.active {{
        border-color: var(--primary);
        background: rgba(6, 182, 212, 0.15);
        color: var(--primary-lg);
    }}
    
    .voice-btn:hover:not(.active) {{
        border-color: rgba(255, 255, 255, 0.2);
        background: rgba(255, 255, 255, 0.06);
    }}
    
    .language-dropdown {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.625rem 0.875rem;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid var(--border);
        border-radius: 10px;
        color: var(--text);
        font-size: 0.8125rem;
        cursor: pointer;
        transition: all 0.2s;
    }}
    
    .language-dropdown:hover {{
        border-color: rgba(255, 255, 255, 0.2);
    }}
    
    .toggle-row {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.625rem 0;
    }}
    
    .toggle-label {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.8125rem;
        color: var(--text);
    }}
    
    /* Suggested Questions */
    .suggested-list {{
        display: flex;
        flex-direction: column;
        gap: 0.375rem;
    }}
    
    .suggested-item {{
        padding: 0.625rem 0.875rem;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid transparent;
        border-radius: 10px;
        color: var(--text-muted);
        font-size: 0.75rem;
        cursor: pointer;
        transition: all 0.2s;
        text-align: left;
    }}
    
    .suggested-item:hover {{
        background: rgba(6, 182, 212, 0.08);
        border-color: rgba(6, 182, 212, 0.3);
        color: var(--primary-lg);
    }}
    
    .suggested-item::before {{
        content: "•";
        margin-right: 0.5rem;
        color: var(--primary);
    }}
    
    /* Action Buttons */
    .action-btn {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        width: 100%;
        padding: 0.625rem;
        border-radius: 10px;
        border: none;
        font-size: 0.8125rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s;
    }}
    
    .action-btn-secondary {{
        background: rgba(255, 255, 255, 0.06);
        color: var(--text-muted);
        border: 1px solid var(--border);
    }}
    
    .action-btn-secondary:hover {{
        background: rgba(255, 255, 255, 0.1);
        color: var(--text);
    }}
    
    .action-btn-danger {{
        background: rgba(239, 68, 68, 0.1);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.2);
    }}
    
    .action-btn-danger:hover {{
        background: rgba(239, 68, 68, 0.15);
    }}
    
    /* ═══════════════════════════════════════════════════════════════════════
       CHAT AREA STYLES
       ═══════════════════════════════════════════════════════════════════════ */
    .chat-container {{
        flex: 1;
        overflow-y: auto;
        padding: 1rem 1.25rem;
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }}
    
    .welcome-screen {{
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 2rem;
    }}
    
    .welcome-icon {{
        width: 96px;
        height: 96px;
        background: linear-gradient(135deg, var(--primary), var(--accent), #8b5cf6);
        border-radius: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 40px rgba(6, 182, 212, 0.35);
        animation: float 3s ease-in-out infinite;
    }}
    
    @keyframes float {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-10px); }}
    }}
    
    .welcome-screen h2 {{
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text);
        margin: 0 0 0.5rem 0;
    }}
    
    .welcome-screen p {{
        font-size: 0.9375rem;
        color: var(--text-muted);
        margin: 0 0 1.5rem 0;
    }}
    
    .quick-chips {{
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 0.5rem;
        max-width: 500px;
    }}
    
    .quick-chip {{
        padding: 0.5rem 1rem;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid var(--border);
        border-radius: 50px;
        color: var(--text-muted);
        font-size: 0.8125rem;
        cursor: pointer;
        transition: all 0.2s;
    }}
    
    .quick-chip:hover {{
        background: rgba(6, 182, 212, 0.1);
        border-color: rgba(6, 182, 212, 0.4);
        color: var(--primary-lg);
    }}
    
    /* Message Bubbles */
    .message-row {{
        display: flex;
        gap: 0.875rem;
        animation: messageIn 0.3s ease-out;
    }}
    
    .message-row.user {{
        flex-direction: row-reverse;
    }}
    
    @keyframes messageIn {{
        from {{ opacity: 0; transform: translateY(10px) scale(0.98); }}
        to {{ opacity: 1; transform: translateY(0) scale(1); }}
    }}
    
    .message-avatar {{
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.875rem;
        flex-shrink: 0;
    }}
    
    .message-avatar.user {{
        background: linear-gradient(135deg, var(--primary), var(--accent));
    }}
    
    .message-avatar.ai {{
        background: linear-gradient(135deg, #8b5cf6, #a78bfa);
    }}
    
    .message-bubble {{
        max-width: 75%;
        padding: 0.875rem 1.125rem;
        border-radius: 18px;
        font-size: 0.9375rem;
        line-height: 1.6;
    }}
    
    .message-bubble.user {{
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.2), rgba(59, 130, 246, 0.15));
        border: 1px solid rgba(6, 182, 212, 0.3);
        color: var(--text);
        border-bottom-right-radius: 4px;
    }}
    
    .message-bubble.ai {{
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid var(--border);
        color: var(--text);
        border-bottom-left-radius: 4px;
    }}
    
    .message-time {{
        font-size: 0.6875rem;
        color: var(--text-muted);
        margin-top: 0.375rem;
        padding: 0 0.25rem;
    }}
    
    .message-row.user .message-time {{
        text-align: right;
    }}
    
    /* ═══════════════════════════════════════════════════════════════════════
       INPUT AREA STYLES
       ═══════════════════════════════════════════════════════════════════════ */
    .input-container {{
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.75rem;
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(12px);
        border: 1px solid var(--border);
        border-radius: var(--radius);
    }}
    
    .mic-button {{
        width: 44px;
        height: 44px;
        border-radius: 12px;
        border: none;
        background: rgba(255, 255, 255, 0.06);
        color: var(--text-muted);
        font-size: 1.25rem;
        cursor: pointer;
        transition: all 0.2s;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }}
    
    .mic-button:hover {{
        background: rgba(255, 255, 255, 0.1);
        color: var(--text);
    }}
    
    .mic-button.recording {{
        background: rgba(239, 68, 68, 0.2);
        color: #ef4444;
        animation: recordingPulse 1.5s ease-in-out infinite;
    }}
    
    @keyframes recordingPulse {{
        0%, 100% {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }}
        50% {{ box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }}
    }}
    
    .text-input-wrapper {{
        flex: 1;
        position: relative;
    }}
    
    .text-input-wrapper input {{
        width: 100%;
        height: 44px;
        padding: 0 1rem;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid var(--border);
        border-radius: 12px;
        color: var(--text);
        font-size: 0.9375rem;
        outline: none;
        transition: all 0.2s;
    }}
    
    .text-input-wrapper input::placeholder {{
        color: var(--text-muted);
    }}
    
    .text-input-wrapper input:focus {{
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.15);
    }}
    
    .send-button {{
        width: 44px;
        height: 44px;
        border-radius: 12px;
        border: none;
        background: linear-gradient(135deg, var(--primary), var(--accent));
        color: white;
        font-size: 1.125rem;
        cursor: pointer;
        transition: all 0.2s;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }}
    
    .send-button:hover:not(:disabled) {{
        transform: scale(1.05);
        box-shadow: 0 4px 20px rgba(6, 182, 212, 0.4);
    }}
    
    .send-button:disabled {{
        opacity: 0.5;
        cursor: not-allowed;
    }}
    
    .input-footer {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 0.5rem;
        padding: 0 0.5rem;
        font-size: 0.6875rem;
        color: var(--text-muted);
    }}
    
    .input-footer span {{
        display: flex;
        align-items: center;
        gap: 0.375rem;
    }}
    
    /* ═══════════════════════════════════════════════════════════════════════
       TTS WIDGET STYLES
       ═══════════════════════════════════════════════════════════════════════ */
    .tts-widget {{
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.625rem 0.875rem;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(59, 130, 246, 0.08));
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 12px;
        margin-top: 0.5rem;
    }}
    
    .tts-wave {{
        display: flex;
        align-items: flex-end;
        gap: 2px;
        height: 16px;
    }}
    
    .tts-wave-bar {{
        width: 3px;
        background: var(--success);
        border-radius: 2px;
        animation: wave 0.6s ease-in-out infinite;
    }}
    
    .tts-wave-bar:nth-child(1) {{ height: 6px; animation-delay: 0s; }}
    .tts-wave-bar:nth-child(2) {{ height: 14px; animation-delay: 0.1s; }}
    .tts-wave-bar:nth-child(3) {{ height: 10px; animation-delay: 0.2s; }}
    .tts-wave-bar:nth-child(4) {{ height: 16px; animation-delay: 0.3s; }}
    .tts-wave-bar:nth-child(5) {{ height: 8px; animation-delay: 0.4s; }}
    
    @keyframes wave {{
        0%, 100% {{ transform: scaleY(0.4); }}
        50% {{ transform: scaleY(1); }}
    }}
    
    .tts-label {{
        flex: 1;
        font-size: 0.75rem;
        color: var(--success);
        font-weight: 500;
    }}
    
    .tts-stop {{
        padding: 0.25rem 0.75rem;
        background: rgba(239, 68, 68, 0.15);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 50px;
        color: #f87171;
        font-size: 0.6875rem;
        cursor: pointer;
        transition: all 0.2s;
    }}
    
    .tts-stop:hover {{
        background: rgba(239, 68, 68, 0.25);
    }}
    
    /* ═══════════════════════════════════════════════════════════════════════
       SCROLLBAR STYLES
       ═══════════════════════════════════════════════════════════════════════ */
    ::-webkit-scrollbar {{
        width: 5px;
        height: 5px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: transparent;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: rgba(255, 255, 255, 0.15);
        border-radius: 3px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: rgba(255, 255, 255, 0.25);
    }}
    
    /* ═══════════════════════════════════════════════════════════════════════
       STREAMLIT OVERRIDES
       ═══════════════════════════════════════════════════════════════════════ */
    .block-container {{
        padding: 0 !important;
        max-width: 100% !important;
    }}
    
    div[data-testid="stVerticalBlock"] {{
        gap: 0 !important;
    }}
    
    /* Hide Streamlit's default chat input - we use custom */
    div[data-testid="stChatInput"] {{
        display: none !important;
    }}
    
    /* Custom radio buttons for voice selection */
    div[data-testid="stRadio"] > div {{
        display: flex;
        gap: 0.5rem;
    }}
    
    div[data-testid="stRadio"] label {{
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        padding: 0.5rem 1rem !important;
    }}
    
    div[data-testid="stRadio"] label[data-checked="true"] {{
        background: rgba(6, 182, 212, 0.15) !important;
        border-color: var(--primary) !important;
    }}
    
    /* ═══════════════════════════════════════════════════════════════════════
       RESPONSIVE STYLES
       ═══════════════════════════════════════════════════════════════════════ */
    @media (max-width: 1024px) {{
        .sidebar-panel {{
            width: 280px;
        }}
    }}
    
    @media (max-width: 768px) {{
        .content-section {{
            flex-direction: column;
        }}
        
        .sidebar-panel {{
            width: 100%;
            max-height: 200px;
        }}
        
        .header-section {{
            padding: 0.75rem 1rem;
        }}
        
        .logo-text h1 {{
            font-size: 1.125rem;
        }}
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 5. DATA STORAGE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
DATA_FILE = "school_data.json"

def load_data():
    """Load user data from JSON file."""
    if Path(DATA_FILE).exists():
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return get_default_data()

def save_data(data):
    """Save user data to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_default_data():
    """Get default data structure."""
    return {
        "users": {
            "student1": {
                "password": hashlib.sha256("student123".encode()).hexdigest(),
                "role": "student",
                "name": "Demo Student",
                "class": "10",
                "medium": "English",
                "board": "SCERT Telangana",
                "usage_today": 6,
                "total_usage": 156,
                "last_active": str(datetime.datetime.now()),
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
    """Hash password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def check_usage_limit(data, username):
    """Check if user has exceeded daily usage limit."""
    if username not in data["users"]:
        return True
    user = data["users"][username]
    if user["role"] == "teacher":
        return True
    daily_limit = data["settings"]["daily_limit"]
    return user["usage_today"] < daily_limit

# ═══════════════════════════════════════════════════════════════════════════════
# 6. GROQ AI FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def get_groq_response(prompt, student_class="10", subject=""):
    """Get AI response from Groq API."""
    if not groq_client:
        return "⚠️ AI service is temporarily unavailable. Please try again later."
    
    system_prompt = f"""You are an expert AI tutor for Class {student_class} students following the SCERT Telangana curriculum. 
    Provide clear, educational responses that help students understand concepts.
    
    Guidelines:
    - Explain concepts in simple, easy-to-understand language
    - Use examples relevant to Indian context when possible
    - Keep responses concise but comprehensive (2-4 paragraphs)
    - Encourage critical thinking
    - If the question is unclear, ask for clarification
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
        return f"⚠️ Error: {str(e)}. Please try again."

# ═══════════════════════════════════════════════════════════════════════════════
# 7. TTS TEXT PROCESSING
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
# 8. UI COMPONENT RENDERERS
# ═══════════════════════════════════════════════════════════════════════════════
def render_header(school_name, student_name, student_class, board, year, usage_today, daily_limit, voice, language):
    """Render the header section."""
    usage_percent = (usage_today / daily_limit) * 100
    
    header_html = f"""
    <div class="glass-panel header-section">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div class="header-logo">
                <div class="logo-icon">🎓</div>
                <div class="logo-text">
                    <h1><span>{school_name}</span> Smart Tutor</h1>
                    <p>Hello {student_name}! · {student_class} · {board} {year}</p>
                </div>
            </div>
            <div class="header-badges">
                <span class="badge badge-cyan">📅 {usage_today}/{daily_limit} TODAY</span>
                <span class="badge badge-purple">🔊 {voice} · {language}</span>
            </div>
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

def render_profile_card(student_name, student_class, medium, usage_today, daily_limit):
    """Render student profile card."""
    usage_percent = (usage_today / daily_limit) * 100
    initials = "".join([n[0] for n in student_name.split()[:2]])
    
    profile_html = f"""
    <div class="glass-card profile-card">
        <div class="profile-header">
            <div class="profile-avatar">{initials}</div>
            <div class="profile-info">
                <h3>{student_name}</h3>
                <p>{student_class} · {medium}</p>
            </div>
        </div>
        <div class="usage-bar-container">
            <div class="usage-bar-header">
                <span>Daily Usage</span>
                <span>{usage_today}/{daily_limit}</span>
            </div>
            <div class="usage-bar-track">
                <div class="usage-bar-fill" style="width: {usage_percent}%"></div>
            </div>
        </div>
    </div>
    """
    st.markdown(profile_html, unsafe_allow_html=True)

def render_message(message, msg_type="user"):
    """Render a chat message bubble."""
    avatar = "👤" if msg_type == "user" else "🤖"
    time_str = datetime.datetime.now().strftime("%I:%M %p")
    
    message_html = f"""
    <div class="message-row {msg_type}">
        <div class="message-avatar {msg_type}">{avatar}</div>
        <div>
            <div class="message-bubble {msg_type}">{message}</div>
            <div class="message-time">{time_str}</div>
        </div>
    </div>
    """
    st.markdown(message_html, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# VOICE INPUT COMPONENT (Mic Button with Speech Recognition)
# ═══════════════════════════════════════════════════════════════════════════════
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
    <span class="placeholder" id="ph">Tap 🎙️ mic → speak your question</span>
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
  if (!SR) {{ setPreview('⚠️ Use <b>Chrome</b> for voice input', ''); return; }}
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
  rec.maxAlternatives = 3;

  rec.onstart = function() {{
    isListen = true;
    micBtn.className = 'mic-btn mic-on';
    micBtn.innerHTML = '⏹';
    setPreview('<span class="ldot"></span><em style="color:#94a3b8;">Listening in {lang_code}...</em>', 'listening');
  }};

  rec.onresult = function(e) {{
    var interim = '', final = '';
    for (var i = e.resultIndex; i < e.results.length; i++) {{
      var t = e.results[i][0].transcript;
      if (e.results[i].isFinal) {{
        final += t;
      }} else {{
        interim += t;
      }}
    }}
    if (final) {{
      finalTxt = final.trim();
      setPreview('✅ <span style="color:#22d3ee;font-weight:600;">' + escHtml(finalTxt) + '</span>', 'ready');
      sendBtn.className = 'send-btn show';
      startCountdown();
    }} else if (interim) {{
      setPreview('<span class="ldot"></span><span style="color:#e2e8f0;">' + escHtml(interim) + '</span>', 'listening');
    }}
  }};

  rec.onerror = function(e) {{
    isListen = false;
    resetMic();
    var m = {{
      'no-speech': '🔇 No speech detected. Try again.',
      'not-allowed': '🚫 Microphone blocked — allow in browser.',
      'audio-capture': '🎤 No microphone found.'
    }};
    setPreview(m[e.error] || '⚠️ Error: ' + e.error, '');
  }};

  rec.onend = function() {{
    isListen = false;
    resetMic();
  }};

  try {{ rec.start(); }} catch (ex) {{
    setPreview('Mic error: ' + ex.message, '');
    isListen = false;
    resetMic();
  }}
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
    if (cdLeft <= 0) {{
      clearInterval(cdTimer);
      cdTimer = null;
      cdPill.className = 'cd-pill';
      sendNow();
    }}
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
  setPreview('⏳ <span style="color:#22d3ee;">Sending...</span>', 'ready');

  // Prefix "VOICE::" so Python knows this was voice input
  var voiceText = 'VOICE::' + text;

  setTimeout(function() {{
    try {{
      var pd = window.parent.document;
      var ta = pd.querySelector('textarea[data-testid="stChatInputTextArea"]');
      if (!ta) ta = pd.querySelector('[data-testid="stChatInput"] textarea');
      if (!ta) ta = pd.querySelector('textarea');

      if (ta) {{
        var setter = Object.getOwnPropertyDescriptor(
          window.parent.HTMLTextAreaElement.prototype, 'value'
        ).set;
        setter.call(ta, voiceText);
        ta.dispatchEvent(new Event('input', {{bubbles: true}}));
        ta.dispatchEvent(new Event('change', {{bubbles: true}}));

        setTimeout(function() {{
          var btn = pd.querySelector('button[data-testid="stChatInputSubmitButton"]');
          if (!btn) btn = pd.querySelector('[data-testid="stChatInput"] button');
          if (btn) {{
            btn.click();
            setPreview('✅ <span style="color:#22d3ee;">Sent! AI is thinking...</span>', 'ready');
            setTimeout(function() {{ resetPreview(); finalTxt = ''; }}, 3000);
          }}
        }}, 250);
      }} else {{
        setPreview('⚠️ Please type below and press Enter', '');
      }}
    }} catch (ex) {{
      setPreview('⚠️ Please type: ' + escHtml(text), '');
      console.warn('Send error:', ex);
    }}
  }}, 80);
}}

function escHtml(s) {{
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}}
</script></body></html>"""


def render_tts_widget(text, language, gender):
    """Render TTS widget with waveform animation using components.html."""
    # Prepare text for JS (escape properly)
    clean_text = strip_md_for_tts(text)
    safe_text = clean_text.replace("\\", "\\\\").replace("'", "\\'").replace("\n", " ")
    pitch = "1.1" if gender == "Female" else "0.88"
    lang_code = "en-IN" if language == "English" else "hi-IN" if language == "Hindi" else "te-IN"
    
    # Full HTML with embedded CSS and JS (works in components.html iframe)
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
  cursor:pointer;font-weight:600;flex-shrink:0;
}}
.tts-stop:hover {{background:rgba(51,65,85,0.9);color:#fbbf24;}}
</style>
</head><body>
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
function stopTTS() {{
  if (window.speechSynthesis) window.speechSynthesis.cancel();
}}

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
    // Prefer Indian voices
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

// Auto-start after short delay
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

def render_welcome_screen(student_name, quick_questions, key_prefix=""):
    """Render welcome screen when no messages."""
    welcome_html = f"""
    <div class="welcome-screen">
        <div class="welcome-icon">📚</div>
        <h2>Ready to learn, {student_name}!</h2>
        <p>Tap 🎙️ mic to speak, or type below</p>
    </div>
    """
    st.markdown(welcome_html, unsafe_allow_html=True)
    
    # Quick question chips
    cols = st.columns(min(len(quick_questions), 3))
    for i, q in enumerate(quick_questions[:3]):
        with cols[i]:
            if st.button(q, key=f"{key_prefix}quick_{i}", use_container_width=True):
                return q
    return None

# ═══════════════════════════════════════════════════════════════════════════════
# 9. MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    """Main application function."""
    
    # Inject premium CSS
    inject_premium_css()
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "input_text" not in st.session_state:
        st.session_state.input_text = ""
    if "selected_voice" not in st.session_state:
        st.session_state.selected_voice = "Male"
    if "selected_language" not in st.session_state:
        st.session_state.selected_language = "English"
    if "auto_speak" not in st.session_state:
        st.session_state.auto_speak = True
    if "is_recording" not in st.session_state:
        st.session_state.is_recording = False
    if "usage_today" not in st.session_state:
        st.session_state.usage_today = 6
    if "last_tts_hash" not in st.session_state:
        st.session_state.last_tts_hash = ""
    
    # Load data
    data = load_data()
    user = data["users"]["student1"]
    
    # Constants
    SUGGESTED_QUESTIONS = [
        "Explain Ch1 Social Studies",
        "How to solve quadratic equations?",
        "What is photosynthesis?",
        "Explain democracy",
        "Climate of India - summary",
    ]
    
    VOICE_OPTIONS = ["Female", "Male"]
    LANGUAGE_OPTIONS = ["English", "Telugu", "Hindi"]
    
    # ═══════════════════════════════════════════════════════════════════════════
    # HEADER SECTION
    # ═══════════════════════════════════════════════════════════════════════════
    render_header(
        school_name=data["settings"]["school_name"],
        student_name=user["name"],
        student_class=f"Class {user['class']}",
        board=user["board"],
        year="2025-26",
        usage_today=st.session_state.usage_today,
        daily_limit=data["settings"]["daily_limit"],
        voice=st.session_state.selected_voice,
        language=st.session_state.selected_language
    )
    
    # ═══════════════════════════════════════════════════════════════════════════
    # MAIN CONTENT AREA
    # ═══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    
    # ─────────────────────────────────────────────────────────────────────────
    # SIDEBAR PANEL
    # ─────────────────────────────────────────────────────────────────────────
    st.markdown('<div class="sidebar-panel">', unsafe_allow_html=True)
    
    # Profile Card
    render_profile_card(
        student_name=user["name"],
        student_class=f"Class {user['class']}",
        medium=user["medium"],
        usage_today=st.session_state.usage_today,
        daily_limit=data["settings"]["daily_limit"]
    )
    
    # Voice Settings
    st.markdown('<div class="glass-card" style="padding: 1rem;">', unsafe_allow_html=True)
    
    # Voice selection
    st.markdown('<p style="font-size: 0.75rem; color: #94a3b8; margin-bottom: 0.5rem;">Voice</p>', unsafe_allow_html=True)
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
    
    st.markdown(f'<p style="font-size: 0.6875rem; color: #64748b; margin-top: 0.5rem;">Selected: <i>{st.session_state.selected_voice}</i></p>', unsafe_allow_html=True)
    
    # Language selector
    st.markdown('<p style="font-size: 0.75rem; color: #94a3b8; margin: 0.75rem 0 0.5rem 0;">🌐 Voice Language</p>', unsafe_allow_html=True)
    lang = st.selectbox("", LANGUAGE_OPTIONS, index=LANGUAGE_OPTIONS.index(st.session_state.selected_language), 
                        label_visibility="collapsed", key="lang_select")
    if lang != st.session_state.selected_language:
        st.session_state.selected_language = lang
        st.rerun()
    
    # Auto-speak toggle
    auto_speak = st.toggle("🎧 Auto-speak Responses", value=st.session_state.auto_speak, key="auto_speak_toggle")
    if auto_speak != st.session_state.auto_speak:
        st.session_state.auto_speak = auto_speak
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Suggested Questions
    st.markdown('<div class="glass-card" style="padding: 1rem; flex: 1;">', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 0.75rem; color: #94a3b8; margin-bottom: 0.75rem;">✨ Try asking:</p>', unsafe_allow_html=True)
    
    for i, q in enumerate(SUGGESTED_QUESTIONS):
        if st.button(q, key=f"sugg_q_{i}", use_container_width=True):
            st.session_state.input_text = q
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Action Buttons
    st.markdown('<div style="display: flex; flex-direction: column; gap: 0.5rem;">', unsafe_allow_html=True)
    if st.button("🗑️ Clear Chat", key="clear_chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    if st.button("🚪 Logout", key="logout", use_container_width=True):
        st.warning("Logout functionality to be implemented")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # End sidebar-panel
    
    # ─────────────────────────────────────────────────────────────────────────
    # CHAT PANEL
    # ─────────────────────────────────────────────────────────────────────────
    st.markdown('<div class="chat-panel glass-panel">', unsafe_allow_html=True)
    
    # Chat container with messages
    chat_container = st.container()
    with chat_container:
        if len(st.session_state.messages) == 0:
            # Welcome screen
            result = render_welcome_screen(user["name"], SUGGESTED_QUESTIONS, key_prefix="welcome_")
            if result:
                st.session_state.input_text = result
                st.rerun()
        else:
            # Display messages
            for msg in st.session_state.messages:
                render_message(msg["content"], msg["type"])
            
            # Show TTS widget for the LATEST AI message (ONLY if input was voice)
            if st.session_state.auto_speak and st.session_state.messages:
                # Find last AI message
                for msg in reversed(st.session_state.messages):
                    if msg["type"] == "ai":
                        # Only speak if: (1) should_speak flag is True AND (2) not already spoken
                        if msg.get("should_speak", False):
                            import hashlib
                            msg_hash = hashlib.md5(msg["content"].encode()).hexdigest()[:12]
                            if msg_hash != st.session_state.get("last_tts_hash", ""):
                                render_tts_widget(msg["content"], st.session_state.selected_language, st.session_state.selected_voice)
                                st.session_state["last_tts_hash"] = msg_hash
                        break
    
    st.markdown('</div>', unsafe_allow_html=True)  # End chat-panel
    
    st.markdown('</div>', unsafe_allow_html=True)  # End content-section
    
    # ═══════════════════════════════════════════════════════════════════════════
    # INPUT SECTION - ChatGPT-style single bar with mic icon
    # ═══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    
    # Render mic component for voice input (shows above chat_input)
    mic_html = get_mic_component_html(
        lang_code=st.session_state.selected_language,
        countdown_sec=5
    )
    components.html(mic_html, height=70, scrolling=False)
    
    # Chat input bar (native Streamlit - works with Enter key)
    user_input = st.chat_input(
        placeholder=f"💬 Type your question or use 🎙️ mic above... (Class {user['class']} · {st.session_state.selected_language})",
        key="chat_input"
    )
    
    # Input footer
    footer_html = """
    <div class="input-footer">
        <span>⚙️ Press Enter to send · 🎙️ Tap mic for voice</span>
        <span>✨ Powered by AI · SCERT Telangana Curriculum</span>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # End input-section
    
    # ═══════════════════════════════════════════════════════════════════════════
    # HANDLE MESSAGE SENDING (st.chat_input returns value when Enter pressed)
    # ═══════════════════════════════════════════════════════════════════════════
    if user_input and user_input.strip():
        # Detect voice input (mic JS prefixes with "VOICE::")
        raw = user_input.strip()
        is_voice = raw.startswith("VOICE::")
        clean_text = raw[len("VOICE::"):] if is_voice else raw
        
        # Add user message
        st.session_state.messages.append({
            "type": "user",
            "content": clean_text,
            "timestamp": datetime.datetime.now(),
            "input_type": "voice" if is_voice else "text"
        })
        
        # Update usage
        st.session_state.usage_today += 1
        
        # Get AI response
        with st.spinner("🤔 AI is thinking..."):
            ai_response = get_groq_response(
                clean_text,
                student_class=user["class"],
                subject=""
            )
        
        # Add AI message - TTS only if input was voice
        st.session_state.messages.append({
            "type": "ai",
            "content": ai_response,
            "timestamp": datetime.datetime.now(),
            "should_speak": is_voice  # Only speak for voice input
        })
        
        st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# 10. RUN APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    main()
