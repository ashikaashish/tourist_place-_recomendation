import streamlit as st
import sqlite3
import os

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="Tourist Place Recommendation",
    page_icon="🌍",
    layout="wide"
)
st.markdown("""
<style>
[data-testid="stSidebar"]        { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }

/* ===== Welcome Page Ticker + Navbar ===== */
.ticker-wrap{
position:fixed;top:0;left:0;right:0;z-index:2000;
background:linear-gradient(90deg,#1a1410,#2d2218,#1a1410);
height:34px;display:flex;align-items:center;overflow:hidden;
border-bottom:1px solid rgba(201,169,110,0.3);
}
.ticker-track{display:flex;white-space:nowrap;animation:tickerScroll 30s linear infinite;}
.ticker-item{padding:0 2rem;color:#c9a96e;font-size:12px;text-transform:uppercase;}
@keyframes tickerScroll{0%{transform:translateX(0);}100%{transform:translateX(-50%);}}

.navbar-shell{
position:fixed;top:34px;left:0;right:0;height:66px;z-index:1500;
background:rgba(250,250,248,0.95);
backdrop-filter:blur(20px);
border-bottom:1px solid rgba(201,169,110,0.18);
}
.nav-brand{
position:fixed;top:34px;left:3rem;height:66px;
display:flex;align-items:center;z-index:1600;
font-weight:600;color:#1a1814;
}


/* ===== WELCOME THEME OVERRIDES ===== */
header,[data-testid="stHeader"],[data-testid="stToolbar"],
[data-testid="stDecoration"],#MainMenu,footer{
display:none !important;
}

.block-container{
padding-top:0 !important;
}

html,body,.stApp{
background:#fafaf8 !important;
color:#1a1814 !important;
}

.form-card{
background:#ffffff !important;
border:1px solid rgba(201,169,110,0.20) !important;
box-shadow:0 20px 60px rgba(0,0,0,0.08) !important;
}

.hero-title,.hero-subtitle,label,p,h1,h2,h3{
color:#1a1814 !important;
}

input, textarea{
color:#1a1814 !important;
}


/* ===== FIXED NAVBAR BUTTON ===== */
div[data-testid="stHorizontalBlock"]{
    align-items:center !important;
}
div[data-testid="stHorizontalBlock"] .stButton button[key="top_home"]{
}

/* Top home button */
div[data-testid="stButton"] > button[kind="secondary"],
div[data-testid="stButton"] > button{
}

/* Light form fields */
input[type="text"], input[type="number"], input[type="password"]{
    background:#ffffff !important;
    color:#1a1814 !important;
    border:1px solid #d4c09a !important;
}

div[data-baseweb="select"] > div{
    background:#ffffff !important;
    color:#1a1814 !important;
    border:1px solid #d4c09a !important;
}

label, .stTextInput label, .stNumberInput label, .stSelectbox label{
    color:#4a3d2a !important;
}

.form-card{
    background:#ffffff !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown('''
<style>
.hero{
background-image:url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1920&q=90');
background-size:cover;
background-position:center;
min-height:460px;
border-radius:28px;
display:flex;
flex-direction:column;
justify-content:center;
align-items:center;
position:relative;
overflow:hidden;
}
.hero::before{
content:'';
position:absolute;
inset:0;
background:rgba(255,255,255,0.15);
animation:kenburns 20s ease-in-out infinite alternate;
}
@keyframes kenburns{
from{transform:scale(1);}
to{transform:scale(1.1);}
}
</style>
''', unsafe_allow_html=True)


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
/* Navbar button styling */
div[data-testid="stHorizontalBlock"]{
    position:fixed !important;
    top:34px !important;
    right:40px !important;
    z-index:2000 !important;
    background:transparent !important;
}
div[data-testid="stHorizontalBlock"] .stButton button{
    width:auto !important;
    height:38px !important;
    padding:0 20px !important;
    background:rgba(30,20,10,0.05) !important;
    color:#4a3d2a !important;
    border:1.5px solid rgba(60,40,20,0.15) !important;
    border-radius:8px !important;
    box-shadow:none !important;
    animation:none !important;
}
div[data-testid="stHorizontalBlock"] .stButton button:hover{
    background:rgba(30,20,10,0.10) !important;
    border-color:rgba(60,40,20,0.30) !important;
    transform:translateY(-2px) !important;
}
.stButton > button:active { transform: translateY(0px) scale(0.99) !important; }

div[data-testid="stAlert"] {
    background: rgba(30,27,75,0.85) !important; border-radius: 14px !important;
    border: 1px solid rgba(99,102,241,0.35) !important;
    backdrop-filter: blur(10px); color: #e2e8f0 !important;
    animation: fadeSlideDown 0.4s ease both;
}

/* ===== PREMIUM STATS CARDS ===== */

.stats-row{
    display:flex;
    justify-content:center;
    gap:30px;
    margin:45px 0;
}

.stat-box{
    flex:1;
    background:#ffffff !important;
    border-radius:24px;
    padding:35px 25px;
    text-align:center;
    border:1px solid #edf2f7;
    box-shadow:0 12px 30px rgba(0,0,0,0.08);
}

.stat-icon{
    width:90px;
    height:90px;
    margin:0 auto 20px;
    border-radius:22px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:46px;
}

.icon-blue{
    background:#eef6ff;
}

.icon-green{
    background:#ecfdf3;
}

.icon-gold{
    background:#fff8e7;
}

.stat-number{
    font-size:60px;
    font-weight:900;
    line-height:1;
    margin-bottom:10px;
}

.blue{
    color:#2196f3;
}

.green{
    color:#22c55e;
}

.gold{
    color:#fbbf24;
}

.stat-label{
    font-size:20px;
    font-weight:800;
    color:#16213e;
    text-transform:uppercase;
    letter-spacing:1px;
}

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


st.markdown("""
<div class="ticker-wrap">
<div class="ticker-track">
<span class="ticker-item">🌍 AI Powered Travel</span>
<span class="ticker-item">✈️ Smart Planning</span>
<span class="ticker-item">🏨 Curated Stays</span>
<span class="ticker-item">⭐ 4.9 Rating</span>
<span class="ticker-item">🌤 Climate Matched Trips</span>
<span class="ticker-item">🌍 AI Powered Travel</span>
<span class="ticker-item">✈️ Smart Planning</span>
<span class="ticker-item">🏨 Curated Stays</span>
<span class="ticker-item">⭐ 4.9 Rating</span>
<span class="ticker-item">🌤 Climate Matched Trips</span>
</div>
</div>
<div class="navbar-shell"></div>
<div class="nav-brand">🌍 Smart Travel Planner</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([10,1,1])

with col3:
    if st.button("🏠 Back to Home"):
        st.switch_page("welcome.py")

st.markdown("<div style='height:110px'></div>", unsafe_allow_html=True)

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
        <div class="stat-icon icon-blue">📍</div>
        <div class="stat-number blue">500+</div>
        <div class="stat-label">DESTINATIONS</div>
    </div>

    <div class="stat-box">
        <div class="stat-icon icon-green">👥</div>
        <div class="stat-number green">10K+</div>
        <div class="stat-label">TRAVELLERS</div>
    </div>

    <div class="stat-box">
        <div class="stat-icon icon-gold">⭐</div>
        <div class="stat-number gold">4.9★</div>
        <div class="stat-label">AVG RATING</div>
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
age = st.number_input("Age", min_value=18, max_value=80, value=25, step=1)

# Budget below Age
budget = st.selectbox(
    "💰 Budget",
    ["Low", "Medium", "High"]
)

# Climate below Budget
climate = st.selectbox(
    "🌤 Climate",
    ["Hot", "Cold", "Moderate"]
)

st.markdown("<br>", unsafe_allow_html=True)

if st.button("🚀 Register→"):
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

# ---------------------------------------------------
# Footer
# ---------------------------------------------------
st.markdown('<div class="footer"><span>✈️  EXPLORE  •  DISCOVER  •  TRAVEL</span></div>', unsafe_allow_html=True)