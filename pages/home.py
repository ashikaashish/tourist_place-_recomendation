import streamlit as st
import sqlite3
import os

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="Tourist Place Recommendation",
    page_icon="🌍",
    layout="centered"
)
st.markdown("""
<style>
[data-testid="stSidebar"]        { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
</style>
""", unsafe_allow_html=True)


PAGES_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PAGES_DIR)  # go up from pages/ to project root
DB_PATH  = os.path.join(BASE_DIR, "tourist.db")

# ---------------------------------------------------
# DB Init  ← FIX 1: added password column (was missing)
# ---------------------------------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            age      INTEGER,
            budget   TEXT,
            climate  TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------------------------------------------------
# Full Animated CSS
# ---------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

* { font-family: 'Poppins', sans-serif; box-sizing: border-box; }

.stApp {
    background: linear-gradient(-45deg, #0f0c29, #302b63, #1a1a2e, #16213e, #0f3460);
    background-size: 400% 400%;
    animation: gradientShift 10s ease infinite;
    min-height: 100vh;
}
@keyframes gradientShift {
    0%   { background-position: 0%   50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0%   50%; }
}
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(circle at 15% 25%, rgba(99,102,241,0.25) 0%, transparent 45%),
        radial-gradient(circle at 85% 75%, rgba(236,72,153,0.2)  0%, transparent 45%),
        radial-gradient(circle at 50% 90%, rgba(6,182,212,0.15)  0%, transparent 40%),
        radial-gradient(circle at 70% 10%, rgba(251,191,36,0.1)  0%, transparent 35%);
    pointer-events: none;
    z-index: 0;
    animation: orbPulse 8s ease-in-out infinite;
}
@keyframes orbPulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.6; }
}
html, body, [class*="css"] { color: #e2e8f0; }

.particles { position: fixed; inset: 0; pointer-events: none; z-index: 0; overflow: hidden; }
.particle {
    position: absolute;
    border-radius: 50%;
    opacity: 0;
    animation: floatUp linear infinite;
}
.particle:nth-child(1)  { width:6px;  height:6px;  left:10%; background:#667eea; animation-duration:9s;  animation-delay:0s;   }
.particle:nth-child(2)  { width:4px;  height:4px;  left:25%; background:#f093fb; animation-duration:12s; animation-delay:2s;   }
.particle:nth-child(3)  { width:8px;  height:8px;  left:40%; background:#4facfe; animation-duration:10s; animation-delay:1s;   }
.particle:nth-child(4)  { width:5px;  height:5px;  left:55%; background:#fbbf24; animation-duration:14s; animation-delay:3s;   }
.particle:nth-child(5)  { width:6px;  height:6px;  left:70%; background:#34d399; animation-duration:11s; animation-delay:0.5s; }
.particle:nth-child(6)  { width:4px;  height:4px;  left:85%; background:#f472b6; animation-duration:13s; animation-delay:4s;   }
.particle:nth-child(7)  { width:7px;  height:7px;  left:5%;  background:#a78bfa; animation-duration:15s; animation-delay:1.5s; }
.particle:nth-child(8)  { width:5px;  height:5px;  left:90%; background:#67e8f9; animation-duration:9s;  animation-delay:2.5s; }
@keyframes floatUp {
    0%   { bottom: -20px; opacity: 0;   transform: translateX(0)    rotate(0deg);   }
    20%  {                opacity: 0.7;                                              }
    80%  {                opacity: 0.4;                                              }
    100% { bottom: 110%;  opacity: 0;   transform: translateX(60px) rotate(360deg); }
}

.hero { text-align: center; padding: 40px 0 10px; animation: fadeSlideDown 0.8s ease both; }
@keyframes fadeSlideDown {
    from { opacity: 0; transform: translateY(-30px); }
    to   { opacity: 1; transform: translateY(0);     }
}
.globe-icon {
    font-size: 80px; display: block; margin: 0 auto 16px;
    animation: floatGlobe 3s ease-in-out infinite;
    filter: drop-shadow(0 0 20px rgba(99,102,241,0.6));
}
@keyframes floatGlobe {
    0%, 100% { transform: translateY(0px)   rotate(0deg);  }
    33%       { transform: translateY(-12px) rotate(5deg);  }
    66%       { transform: translateY(-6px)  rotate(-3deg); }
}
.hero-title {
    font-size: 44px; font-weight: 800;
    background: linear-gradient(135deg, #667eea, #f093fb, #4facfe, #00f2fe, #fbbf24);
    background-size: 300% 300%;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    animation: titleGradient 5s ease infinite; line-height: 1.2; margin-bottom: 10px;
}
@keyframes titleGradient {
    0%   { background-position: 0%   50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0%   50%; }
}
.hero-subtitle { font-size: 16px; color: #94a3b8; margin-bottom: 12px; }

.tag-row {
    display: flex; justify-content: center; gap: 10px; flex-wrap: wrap;
    margin-bottom: 36px; animation: fadeSlideDown 0.8s ease 0.3s both;
}
.tag { padding: 5px 14px; border-radius: 50px; font-size: 12px; font-weight: 500; border: 1px solid; animation: tagGlow 3s ease-in-out infinite; }
.tag-blue   { background: rgba(99,102,241,0.15);  border-color: rgba(99,102,241,0.5);  color: #a5b4fc; }
.tag-pink   { background: rgba(236,72,153,0.15);  border-color: rgba(236,72,153,0.5);  color: #f9a8d4; animation-delay: 0.5s; }
.tag-cyan   { background: rgba(6,182,212,0.15);   border-color: rgba(6,182,212,0.5);   color: #67e8f9; animation-delay: 1s;   }
.tag-amber  { background: rgba(251,191,36,0.15);  border-color: rgba(251,191,36,0.5);  color: #fde68a; animation-delay: 1.5s; }
@keyframes tagGlow {
    0%, 100% { box-shadow: none; }
    50%       { box-shadow: 0 0 10px currentColor; }
}

.form-card {
    background: rgba(15,12,41,0.75);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 28px; padding: 40px 36px;
    backdrop-filter: blur(24px);
    box-shadow: 0 8px 40px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.05);
    animation: cardRise 0.8s ease 0.2s both;
    position: relative; overflow: hidden; max-width: 540px; margin: 0 auto 30px;
}
@keyframes cardRise {
    from { opacity: 0; transform: translateY(40px) scale(0.96); }
    to   { opacity: 1; transform: translateY(0)    scale(1);    }
}
.form-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #667eea, #f093fb, #4facfe, #00f2fe, #fbbf24, #667eea);
    background-size: 300% 100%; animation: borderRun 3s linear infinite;
    border-radius: 28px 28px 0 0;
}
@keyframes borderRun {
    0%   { background-position: 0%   0%; }
    100% { background-position: 300% 0%; }
}
.form-card::after {
    content: ''; position: absolute; inset: 0; border-radius: 28px;
    background: radial-gradient(circle at 50% 0%, rgba(99,102,241,0.08) 0%, transparent 60%);
    pointer-events: none;
}
.form-section-title {
    font-size: 13px; font-weight: 600; color: #c4b5fd;
    letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 20px;
    display: flex; align-items: center; gap: 8px;
}
.form-section-title::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, rgba(99,102,241,0.4), transparent);
}

input[type="text"], input[type="number"], input[type="password"] {
    background: rgba(30,27,75,0.8) !important;
    color: #ffffff !important;
    border: 1.5px solid rgba(99,102,241,0.35) !important;
    border-radius: 14px !important;
    font-size: 15px !important;
    padding: 12px 16px !important;
    transition: border-color 0.3s, box-shadow 0.3s, transform 0.2s !important;
}
input[type="text"]:focus, input[type="number"]:focus, input[type="password"]:focus {
    border-color: #a78bfa !important;
    box-shadow: 0 0 0 4px rgba(167,139,250,0.18), 0 4px 16px rgba(99,102,241,0.2) !important;
    transform: translateY(-1px) !important;
    outline: none !important;
}
input::placeholder { color: #475569 !important; }

label, .stTextInput label, .stNumberInput label, .stSelectbox label {
    color: #c4b5fd !important; font-size: 13px !important;
    font-weight: 600 !important; letter-spacing: 0.4px !important;
    text-transform: uppercase !important;
}

div[data-baseweb="select"] > div {
    background: rgba(30,27,75,0.8) !important; color: #e2e8f0 !important;
    border: 1.5px solid rgba(99,102,241,0.35) !important;
    border-radius: 14px !important; backdrop-filter: blur(10px);
    transition: border-color 0.3s, box-shadow 0.3s, transform 0.2s;
}
div[data-baseweb="select"] > div:hover {
    border-color: rgba(167,139,250,0.7) !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(99,102,241,0.2) !important;
}
div[role="option"]       { background: #1e1b4b !important; color: #e2e8f0 !important; }
div[role="option"]:hover { background: rgba(99,102,241,0.3) !important; }

.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%) !important;
    background-size: 200% 200% !important;
    color: #ffffff !important; border: none !important;
    border-radius: 16px !important; padding: 16px 24px !important;
    font-size: 17px !important; font-weight: 700 !important;
    letter-spacing: 0.5px; cursor: pointer;
    transition: all 0.3s ease !important;
    box-shadow: 0 6px 24px rgba(102,126,234,0.55) !important;
    animation: buttonPulse 3s ease-in-out infinite;
    position: relative !important; overflow: hidden !important; margin-top: 10px;
}
@keyframes buttonPulse {
    0%, 100% { box-shadow: 0 6px 24px rgba(102,126,234,0.55); }
    50%       { box-shadow: 0 6px 36px rgba(240,147,251,0.65); }
}
.stButton > button::before {
    content: ''; position: absolute; top: 0; left: -100%;
    width: 100%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left 0.5s ease;
}
.stButton > button:hover::before { left: 100%; }
.stButton > button:hover {
    transform: translateY(-3px) scale(1.01) !important;
    box-shadow: 0 12px 40px rgba(102,126,234,0.75) !important;
    background-position: right center !important;
}
/* Make back button smaller and left-aligned */
div[data-testid="stButton"]:first-of-type > button {
    width: auto !important;
    padding: 8px 20px !important;
    font-size: 13px !important;
    background: rgba(99,102,241,0.15) !important;
    box-shadow: none !important;
    border: 1px solid rgba(99,102,241,0.3) !important;
    animation: none !important;
}
.stButton > button:active { transform: translateY(0px) scale(0.99) !important; }

div[data-testid="stAlert"] {
    background: rgba(30,27,75,0.85) !important; border-radius: 14px !important;
    border: 1px solid rgba(99,102,241,0.35) !important;
    backdrop-filter: blur(10px); color: #e2e8f0 !important;
    animation: fadeSlideDown 0.4s ease both;
}

.stats-row {
    display: flex; justify-content: center; gap: 16px;
    margin-bottom: 30px; animation: fadeSlideDown 0.8s ease 0.5s both;
}
.stat-box {
    background: rgba(15,12,41,0.6); border: 1px solid rgba(99,102,241,0.2);
    border-radius: 16px; padding: 16px 20px; text-align: center;
    backdrop-filter: blur(10px); flex: 1; transition: transform 0.3s, box-shadow 0.3s;
}
.stat-box:hover { transform: translateY(-4px); box-shadow: 0 8px 24px rgba(99,102,241,0.3); }
.stat-number {
    font-size: 26px; font-weight: 700;
    background: linear-gradient(135deg, #667eea, #f093fb);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.stat-label { font-size: 11px; color: #64748b; font-weight: 500; letter-spacing: 0.5px; text-transform: uppercase; margin-top: 2px; }

.footer { text-align: center; font-size: 13px; margin-top: 30px; padding-bottom: 30px; color: #334155; animation: fadeSlideDown 1s ease 0.6s both; }
.footer span {
    background: linear-gradient(135deg, #667eea, #f093fb, #4facfe);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; font-weight: 600; letter-spacing: 2px;
}

::-webkit-scrollbar       { width: 6px; }
::-webkit-scrollbar-track { background: #0f0c29; }
::-webkit-scrollbar-thumb { background: linear-gradient(#667eea, #764ba2); border-radius: 3px; }
</style>

<div class="particles">
  <div class="particle"></div><div class="particle"></div>
  <div class="particle"></div><div class="particle"></div>
  <div class="particle"></div><div class="particle"></div>
  <div class="particle"></div><div class="particle"></div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Hero Section
# ---------------------------------------------------
st.markdown("""
<div class="hero">
    <span class="globe-icon">🌍</span>
    <div class="hero-title">Discover Your Next<br>Adventure</div>
    <div class="hero-subtitle">Personalised travel recommendations powered by Machine Learning</div>
</div>
<div class="tag-row">
    <span class="tag tag-blue">✈️ Travel Smart</span>
    <span class="tag tag-pink">🗺️ Explore India</span>
    <span class="tag tag-cyan">🤖 ML Powered</span>
    <span class="tag tag-amber">⭐ Top Rated Places</span>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Stats Row
# ---------------------------------------------------
st.markdown("""
<div class="stats-row">
    <div class="stat-box">
        <div class="stat-number">500+</div>
        <div class="stat-label">Destinations</div>
    </div>
    <div class="stat-box">
        <div class="stat-number">10K+</div>
        <div class="stat-label">Travellers</div>
    </div>
    <div class="stat-box">
        <div class="stat-number">4.9★</div>
        <div class="stat-label">Avg Rating</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Registration Form Card
# ---------------------------------------------------
st.markdown('<div class="form-card">', unsafe_allow_html=True)
st.markdown('<div class="form-section-title">👤 Create Your Profile</div>', unsafe_allow_html=True)

name             = st.text_input("Full Name", placeholder="e.g. Arjun Sharma")
password         = st.text_input("🔒 Password",         type="password", placeholder="Enter password")
confirm_password = st.text_input("🔐 Confirm Password", type="password", placeholder="Confirm password")
age              = st.number_input("Age", min_value=18, max_value=80, value=25, step=1)

col1, col2 = st.columns(2)
with col1:
    budget  = st.selectbox("💰 Budget",  ["Low", "Medium", "High"])
with col2:
    climate = st.selectbox("🌤 Climate", ["Hot", "Cold", "Moderate"])

st.markdown("<br>", unsafe_allow_html=True)

if st.button("🚀  Start Exploring →"):
    # ── FIX 2: validate all required fields ──────────────────────────────────
    if not name.strip():
        st.warning("⚠️ Please enter your name to continue.")
    elif not password:
        st.warning("⚠️ Please enter a password.")
    elif password != confirm_password:
        st.error("❌ Passwords do not match.")
    else:
        try:
            # ── FIX 3: correct indentation — all DB code is inside the else block ──
            # ✅ CORRECT — uses get_connection() pointing to root tourist.db
            
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO users (name, password, age, budget, climate) VALUES (?,?,?,?,?)",
                (name.strip(), password, int(age), budget, climate)
            )

            conn.commit()
            conn.close()

            st.session_state["username"] = name.strip()
            st.success(f"🎉 Welcome {name.strip()}!")
            st.switch_page("pages/1_Recommendations.py")

        except Exception as e:
            st.error(f"❌ Database Error: {e}")

st.markdown('</div>', unsafe_allow_html=True)
# Back button
if st.button("← Back to Home"):
    st.switch_page("welcome.py")
# ---------------------------------------------------
# Footer
# ---------------------------------------------------
st.markdown('<div class="footer"><span>✈️  EXPLORE  •  DISCOVER  •  TRAVEL</span></div>', unsafe_allow_html=True)