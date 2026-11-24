"""
⚡ J.A.R.V.I.S. (Just A Rather Very Intelligent System)
Cloud & Desktop Web Voice Assistant - Powered by Streamlit
Developed for Yash Raj (Sir)
"""

import os
import re
import io
import time
import base64
import urllib.parse
import urllib.request
import json
from datetime import datetime
import streamlit as st

# Import native browser microphone component
try:
    from streamlit_mic_recorder import speech_to_text
    MIC_AVAILABLE = True
except ImportError:
    MIC_AVAILABLE = False

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="J.A.R.V.I.S. | Stark Industries AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- FUTURISTIC HUD STYLING -----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@500;600;700&display=swap');
    
    .stApp {
        background-color: #030712;
        color: #E2E8F0;
        font-family: 'Rajdhani', sans-serif;
    }
    
    .hud-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.6rem;
        font-weight: 900;
        letter-spacing: 0.15em;
        text-align: center;
        background: linear-gradient(135deg, #38BDF8 0%, #06B6D4 50%, #F59E0B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
        text-shadow: 0 0 25px rgba(6, 182, 212, 0.4);
    }
    
    .hud-subtitle {
        font-family: 'Orbitron', sans-serif;
        text-align: center;
        color: #94A3B8;
        font-size: 0.95rem;
        letter-spacing: 0.25em;
        margin-bottom: 1.5rem;
    }
    
    /* ARC REACTOR STYLING */
    .arc-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 16px 0;
    }
    
    .arc-reactor {
        position: relative;
        width: 130px;
        height: 130px;
        border-radius: 50%;
        box-shadow: 0 0 40px #06b6d4, inset 0 0 40px #06b6d4;
        border: 4px solid #38bdf8;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: pulse 2.5s infinite alternate ease-in-out;
    }
    
    .arc-core {
        width: 65px;
        height: 65px;
        background: radial-gradient(circle, #ffffff 10%, #38bdf8 60%, #0284c7 100%);
        border-radius: 50%;
        box-shadow: 0 0 25px #ffffff, 0 0 45px #38bdf8;
    }
    
    @keyframes pulse {
        0% { transform: scale(0.96); box-shadow: 0 0 25px #06b6d4, inset 0 0 25px #06b6d4; }
        100% { transform: scale(1.04); box-shadow: 0 0 55px #38bdf8, inset 0 0 45px #38bdf8; }
    }
    
    .hud-card {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 12px;
        padding: 14px 18px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
        margin-bottom: 12px;
    }
    
    .hud-label {
        font-size: 0.8rem;
        font-family: 'Orbitron', sans-serif;
        color: #38BDF8;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }
    
    .hud-value {
        font-size: 1.4rem;
        font-weight: 700;
        color: #F8FAFC;
    }
    
    .jarvis-msg {
        background: rgba(6, 182, 212, 0.1);
        border-left: 4px solid #06B6D4;
        padding: 14px 18px;
        border-radius: 0 10px 10px 0;
        margin: 10px 0;
        font-size: 1.05rem;
        color: #E2E8F0;
    }
    
    .user-msg {
        background: rgba(245, 158, 11, 0.1);
        border-right: 4px solid #F59E0B;
        padding: 14px 18px;
        border-radius: 10px 0 0 10px;
        margin: 10px 0;
        text-align: right;
        font-size: 1.05rem;
        color: #FEF3C7;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SESSION STATE -----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "jarvis", "content": "All systems online and operational, Sir. J.A.R.V.I.S. is at your service. How may I assist you today?"}
    ]

# ----------------- AUDIO SYNTHESIS (JARVIS VOICE) -----------------
def generate_jarvis_speech(text):
    """Generates UK-accented British AI voice audio using gTTS in-memory"""
    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang='en', tld='co.uk')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        audio_b64 = base64.b64encode(fp.read()).decode()
        return audio_b64
    except Exception:
        return None

# ----------------- CORE CAPABILITY ENGINES -----------------
def get_weather(city="London"):
    """Fetches real-time weather using free wttr.in JSON API"""
    try:
        clean_city = urllib.parse.quote(city.strip())
        url = f"https://wttr.in/{clean_city}?format=j1"
        req = urllib.request.Request(url, headers={'User-Agent': 'JarvisAI/1.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            current = data['current_condition'][0]
            temp = current['temp_C']
            feels = current['FeelsLikeC']
            desc = current['weatherDesc'][0]['value']
            humidity = current['humidity']
            wind = current['windspeedKmph']
            return (
                f"Atmospheric scan for **{city.title()}**: Currently **{temp}°C** ({desc}), "
                f"feels like {feels}°C with {humidity}% humidity and winds at {wind} km/h, Sir."
            )
    except Exception:
        return f"Unable to establish satellite meteorological uplink for {city.title()} at this moment, Sir."

def search_wikipedia(query):
    """Fetches instant knowledge summary via Wikipedia official REST API"""
    try:
        q = re.sub(r'^(who is|what is|tell me about|explain|search for|wikipedia)\s+', '', query, flags=re.IGNORECASE).strip()
        encoded_title = urllib.parse.quote(q.replace(' ', '_'))
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_title}"
        req = urllib.request.Request(url, headers={'User-Agent': 'JarvisAI/2.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            extract = data.get('extract')
            title = data.get('title')
            page_url = data.get('content_urls', {}).get('desktop', {}).get('page')
            if extract:
                return f"**{title}**: {extract}\n\n[Open Full Dossier]({page_url})"
    except Exception:
        pass
    return None

def calculate_expression(query):
    """Safely calculates arithmetic expressions"""
    cleaned = re.sub(r'^(calculate|what is|compute)\s+', '', query, flags=re.IGNORECASE).strip()
    if re.match(r'^[0-9\+\-\*\/\(\)\.\s\%\^]+$', cleaned):
        try:
            expr = cleaned.replace('^', '**')
            result = eval(expr, {"__builtins__": None}, {})
            return f"Calculated: **{cleaned} = {result}**, Sir."
        except Exception:
            pass
    return None

def process_jarvis_command(cmd):
    """Core Jarvis NLP and Protocol Dispatcher"""
    query = cmd.strip()
    q_lower = query.lower()
    
    # 1. Identity & Creator
    if any(k in q_lower for k in ["who are you", "what are you", "who made you", "your creator", "who created you"]):
        return (
            "I am **J.A.R.V.I.S.** (*Just A Rather Very Intelligent System*), an autonomous artificial intelligence "
            "engineered by **Sir Yash Raj**. I manage system telemetry, computations, intelligence protocols, and mission operations."
        )

    # 2. Greeting
    if any(q_lower.startswith(k) for k in ["hello", "hi", "hey", "good morning", "good evening", "wake up"]):
        return "Good day, Sir. All diagnostic subroutines are green. What are your orders?"

    # 3. Status Report
    if "status report" in q_lower or "system status" in q_lower:
        now = datetime.now().strftime("%A, %d %B %Y - %H:%M:%S UTC")
        return (
            f"**STATUS REPORT**: Timestamp: `{now}`\n"
            "- Core Arc Reactor: 100% capacity (Stable)\n"
            "- Firewall Protocols: Active & Secure\n"
            "- Systems: Fully Operational\n"
            "- All systems ready for your deployment, Sir."
        )

    # 4. Easter Eggs / Protocols
    if "house party protocol" in q_lower or "protocol house party" in q_lower:
        return "House Party Protocol initiated, Sir. Mobilizing Mark 1 through Mark 85 suits to your coordinates immediately."

    if "i am iron man" in q_lower:
        return "And I am J.A.R.V.I.S., Sir. Always at your side."

    if "joke" in q_lower:
        return "Why did the computer go to the doctor, Sir? Because it caught a virus... although I assure you my antivirus subroutines are impenetrable."

    # 5. YouTube Player Command
    yt_match = re.search(r'(?:play|watch)\s+(.*?)(?:\s+on\s+youtube)?$', q_lower)
    if ("play" in q_lower or "youtube" in q_lower) and yt_match:
        song = yt_match.group(1).replace("on youtube", "").strip()
        if song:
            encoded_song = urllib.parse.quote(song)
            return {
                "type": "youtube",
                "text": f"Locating track **'{song.title()}'** on YouTube audio feeds, Sir. Streaming now.",
                "query": song,
                "url": f"https://www.youtube.com/results?search_query={encoded_song}"
            }

    # 6. Weather Scan
    weather_match = re.search(r'weather\s+(?:in|for|at)?\s*([a-zA-Z\s]+)', q_lower)
    if "weather" in q_lower and weather_match:
        city = weather_match.group(1).strip()
        if not city:
            city = "London"
        return get_weather(city)

    # 7. Math Calculation
    calc_res = calculate_expression(query)
    if calc_res:
        return calc_res

    # 8. Wikipedia & General Knowledge
    wiki_res = search_wikipedia(query)
    if wiki_res:
        return wiki_res

    # 9. Time & Date
    if "time" in q_lower:
        return f"Current telemetry time is **{datetime.now().strftime('%H:%M:%S')}**, Sir."
    if "date" in q_lower:
        return f"Today is **{datetime.now().strftime('%A, %B %d, %Y')}**, Sir."

    # 10. Intelligent Fallback
    return (
        f"Understood, Sir. I have logged your directive: *\"{query}\"*. "
        "All subroutines are synchronized. You may command me to check the weather, query Wikipedia, calculate expressions, or play music on YouTube."
    )

# ----------------- SIDEBAR TELEMETRY -----------------
with st.sidebar:
    st.markdown('<div class="hud-label">⚡ STARK INDUSTRIES OS</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#06B6D4; font-size:1.1rem; font-weight:700; margin-bottom:12px;">SYSTEM TELEMETRY</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="hud-card">
        <div class="hud-label">OPERATIONAL STATUS</div>
        <div class="hud-value" style="color:#10B981;">ONLINE (100%)</div>
    </div>
    <div class="hud-card">
        <div class="hud-label">ARC REACTOR OUTPUT</div>
        <div class="hud-value" style="color:#38BDF8;">3.2 GIGA ожид/s</div>
    </div>
    <div class="hud-card">
        <div class="hud-label">ENVIRONMENT</div>
        <div class="hud-value" style="color:#F59E0B;">DESKTOP & CLOUD</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown('<div class="hud-label">VOICE AUDIO OUTPUT</div>', unsafe_allow_html=True)
    voice_enabled = st.checkbox("Enable J.A.R.V.I.S. Voice Response", value=True)
    
    st.markdown("---")
    st.caption("Developed by Sir Yash Raj | Stark Industries AI")

# ----------------- MAIN DISPLAY -----------------
st.markdown('<div class="hud-title">J. A. R. V. I. S.</div>', unsafe_allow_html=True)
st.markdown('<div class="hud-subtitle">STARK INDUSTRIES AUTONOMOUS INTELLIGENCE INTERFACE</div>', unsafe_allow_html=True)

# Glowing Arc Reactor Centerpiece
st.markdown("""
<div class="arc-container">
    <div class="arc-reactor">
        <div class="arc-core"></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------- NATIVE BROWSER MICROPHONE RECORDING -----------------
st.markdown("<div style='text-align: center; margin: 10px 0;'>", unsafe_allow_html=True)
voice_text = None
if MIC_AVAILABLE:
    voice_text = speech_to_text(
        start_prompt="🎙️ TAP TO SPEAK TO J.A.R.V.I.S.",
        stop_prompt="⏹️ RECORDING AUDIO... (CLICK TO SEND)",
        language="en",
        use_container_width=True,
        just_once=True,
        key="jarvis_mic"
    )
    if voice_text:
        st.success(f"Recognized Voice: \"{voice_text}\"")
else:
    st.info("💡 To enable the microphone button, ensure `streamlit-mic-recorder` is installed.")
st.markdown("</div>", unsafe_allow_html=True)

# Quick Action Chips
st.markdown('<div style="text-align:center; color:#64748B; font-size:0.85rem; margin-bottom:8px;">TACTICAL QUICK DIRECTIVES:</div>', unsafe_allow_html=True)
q_col1, q_col2, q_col3, q_col4 = st.columns(4)
quick_cmd = None
with q_col1:
    if st.button("🛡️ Status Report", use_container_width=True):
        quick_cmd = "Status report"
with q_col2:
    if st.button("🌦️ Weather in London", use_container_width=True):
        quick_cmd = "Weather in London"
with q_col3:
    if st.button("🚀 Explain Black Holes", use_container_width=True):
        quick_cmd = "Explain Black Holes"
with q_col4:
    if st.button("🎵 Play AC/DC on YouTube", use_container_width=True):
        quick_cmd = "Play Back in Black AC/DC on YouTube"

# ----------------- CHAT STREAM & MESSAGING -----------------
chat_container = st.container()

with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-msg"><b>Sir:</b> {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            content = msg["content"]
            if isinstance(content, dict) and content.get("type") == "youtube":
                st.markdown(f'<div class="jarvis-msg"><b>J.A.R.V.I.S.:</b> {content["text"]}</div>', unsafe_allow_html=True)
                st.video(content["url"])
            else:
                st.markdown(f'<div class="jarvis-msg"><b>J.A.R.V.I.S.:</b> {content}</div>', unsafe_allow_html=True)

# Command input box
user_prompt = st.chat_input("Sir, what can I do for you today?")

# Determine final input
final_input = None
if voice_text:
    final_input = voice_text
elif quick_cmd:
    final_input = quick_cmd
elif user_prompt:
    final_input = user_prompt

if final_input:
    # 1. Log User Message
    st.session_state.messages.append({"role": "user", "content": final_input})
    
    # 2. Process Command
    response = process_jarvis_command(final_input)
    st.session_state.messages.append({"role": "jarvis", "content": response})
    
    # 3. Audio Voice Synthesizer
    if voice_enabled:
        spoken_text = response["text"] if isinstance(response, dict) else re.sub(r'\[.*?\]|\(.*?\)|[\*\_]', '', response)
        audio_b64 = generate_jarvis_speech(spoken_text[:250])
        if audio_b64:
            st.markdown(f"""
            <audio autoplay style="display:none;">
                <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
            </audio>
            """, unsafe_allow_html=True)
            
    st.rerun()
