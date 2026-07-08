import streamlit as st
import sqlite3
import os

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="Smart Travel Planner",
    page_icon="🌍",
    layout="wide"
)

# ---------------------------------------------------
# CSS — Light theme matching the screenshot
# ---------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

/* ── Reset ── */
* { font-family: 'Poppins', sans-serif; box-sizing: border-box; margin: 0; padding: 0; }

/* Hide Streamlit chrome */
header, [data-testid="stHeader"], [data-testid="stToolbar"],
[data-testid="stDecoration"], #MainMenu, footer,
[data-testid="stSidebar"], [data-testid="collapsedControl"] {
    display: none !important;
}
.block-container { padding-top: 0 !important; max-width: 100% !important; }
html, body, .stApp { background: #f0f4fa !important; }

/* ── Ticker bar ── */
.ticker-wrap {
    position: fixed; top: 0; left: 0; right: 0; z-index: 2000;
    background: #1a1410;
    height: 34px; display: flex; align-items: center; overflow: hidden;
}
.ticker-track {
    display: flex; white-space: nowrap;
    animation: tickerScroll 30s linear infinite;
}
.ticker-item {
    padding: 0 2rem; color: #c9a96e;
    font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px;
}
@keyframes tickerScroll {
    0%   { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}

/* ── Navbar ── */
.navbar-shell {
    position: fixed; top: 34px; left: 0; right: 0; height: 60px; z-index: 1500;
    background: rgba(255,255,255,0.97);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid #e8e0d0;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.nav-brand {
    position: fixed; top: 34px; left: 2.5rem; height: 60px;
    display: flex; align-items: center; z-index: 1600;
    font-weight: 700; font-size: 17px; color: #1a1814;
    gap: 8px;
}

/* Spacer under fixed bars */
.page-spacer { height: 110px; }

/* ── Hero section ── */
.hero-wrap {
    margin: 0 1.5rem 24px;
    border-radius: 20px; overflow: hidden;
    position: relative; min-height: 380px;
    background: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1400&q=80') center/cover no-repeat;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    text-align: center; padding: 48px 24px 36px;
}
.hero-wrap::before {
    content: '';
    position: absolute; inset: 0;
    background: rgba(255,255,255,0.18);
}
.hero-content { position: relative; z-index: 1; }

.globe-icon { font-size: 72px; display: block; margin-bottom: 12px;
    animation: floatGlobe 3s ease-in-out infinite; }
@keyframes floatGlobe {
    0%, 100% { transform: translateY(0); }
    50%       { transform: translateY(-10px); }
}

.hero-title {
    font-size: 42px; font-weight: 800;
    color: #1a1814; line-height: 1.15; margin-bottom: 10px;
}
.hero-title span { color: #3b82f6; }
.hero-sub {
    font-size: 15px; color: #374151; margin-bottom: 22px;
}

/* Hero tags */
.tag-row { display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; }
.tag {
    padding: 7px 18px; border-radius: 50px; font-size: 13px;
    font-weight: 500; border: 1.5px solid; background: rgba(255,255,255,0.85);
    backdrop-filter: blur(6px);
}
.tag-blue  { border-color: #93c5fd; color: #2563eb; }
.tag-pink  { border-color: #f9a8d4; color: #db2777; }
.tag-cyan  { border-color: #6ee7b7; color: #059669; }
.tag-amber { border-color: #fcd34d; color: #d97706; }

/* ── Stats row ── */
.stats-row {
    display: flex; gap: 16px; margin: 0 1.5rem 28px;
}
.stat-box {
    flex: 1; background: #ffffff; border-radius: 16px;
    padding: 22px 20px; display: flex; align-items: center; gap: 18px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.07);
    transition: transform 0.25s, box-shadow 0.25s;
}
.stat-box:hover { transform: translateY(-4px); box-shadow: 0 8px 28px rgba(0,0,0,0.12); }
.stat-icon {
    width: 56px; height: 56px; border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 26px; flex-shrink: 0;
}
.stat-icon-blue   { background: #eff6ff; }
.stat-icon-green  { background: #f0fdf4; }
.stat-icon-yellow { background: #fffbeb; }
.stat-number { font-size: 30px; font-weight: 800; line-height: 1; }
.stat-num-blue   { color: #3b82f6; }
.stat-num-green  { color: #22c55e; }
.stat-num-yellow { color: #f59e0b; }
.stat-label {
    font-size: 11px; font-weight: 700; color: #6b7280;
    text-transform: uppercase; letter-spacing: 0.8px; margin-top: 4px;
}

/* ── Form card ── */
.form-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 24px; padding: 36px 32px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.08);
    max-width: 560px; margin: 0 auto 32px;
}
.form-title {
    font-size: 14px; font-weight: 700; color: #6b7280;
    text-transform: uppercase; letter-spacing: 1.2px;
    margin-bottom: 20px; display: flex; align-items: center; gap: 8px;
}

/* Light form inputs */
input[type="text"], input[type="number"], input[type="password"] {
    background: #ffffff !important;
    color: #1a1814 !important;
    border: 1.5px solid #d1d5db !important;
    border-radius: 12px !important;
    font-size: 15px !important;
    transition: border-color 0.25s, box-shadow 0.25s !important;
}
input[type="text"]:focus,
input[type="number"]:focus,
input[type="password"]:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.15) !important;
    outline: none !important;
}
input::placeholder { color: #9ca3af !important; }

label, .stTextInput label, .stNumberInput label, .stSelectbox label {
    color: #374151 !important; font-size: 13px !important;
    font-weight: 600 !important;
}

div[data-baseweb="select"] > div {
    background: #ffffff !important;
    color: #1a1814 !important;
    border: 1.5px solid #d1d5db !important;
    border-radius: 12px !important;
}
div[data-baseweb="select"] > div:hover { border-color: #3b82f6 !important; }
div[role="option"]       { background: #ffffff !important; color: #1a1814 !important; }
div[role="option"]:hover { background: #eff6ff !important; }

/* Submit button */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #3b82f6, #6366f1) !important;
    color: #ffffff !important; border: none !important;
    border-radius: 14px !important; padding: 14px 24px !important;
    font-size: 16px !important; font-weight: 700 !important;
    cursor: pointer; transition: all 0.3s ease !important;
    box-shadow: 0 4px 18px rgba(59,130,246,0.45) !important;
    margin-top: 8px;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(59,130,246,0.55) !important;
}

/* Navbar button override */
div[data-testid="stHorizontalBlock"] {
    position: fixed !important; top: 34px !important;
    right: 2.5rem !important; height: 60px !important;
    z-index: 2000 !important; background: transparent !important;
    display: flex !important; align-items: center !important;
}
div[data-testid="stHorizontalBlock"] .stButton > button {
    width: auto !important; height: 38px !important;
    padding: 0 20px !important; font-size: 13px !important;
    background: #f1f5f9 !important; color: #374151 !important;
    border: 1.5px solid #d1d5db !important;
    border-radius: 10px !important;
    box-shadow: none !important; animation: none !important;
    margin-top: 0 !important;
}
div[data-testid="stHorizontalBlock"] .stButton > button:hover {
    background: #e2e8f0 !important; transform: translateY(-1px) !important;
}

/* Alerts — dark, visible text */
div[data-testid="stAlert"] {
    border-radius: 12px !important; max-width: 560px; margin: 0 auto;
}
/* Error */
div[data-testid="stAlert"] [data-testid="stAlertContentError"],
div[data-testid="stAlert"] [data-testid="stAlertContentError"] p,
div[data-testid="stAlert"] [data-testid="stAlertContentError"] span {
    color: #7f1d1d !important; font-weight: 600 !important;
}
/* Warning */
div[data-testid="stAlert"] [data-testid="stAlertContentWarning"],
div[data-testid="stAlert"] [data-testid="stAlertContentWarning"] p,
div[data-testid="stAlert"] [data-testid="stAlertContentWarning"] span {
    color: #78350f !important; font-weight: 600 !important;
}
/* Success */
div[data-testid="stAlert"] [data-testid="stAlertContentSuccess"],
div[data-testid="stAlert"] [data-testid="stAlertContentSuccess"] p,
div[data-testid="stAlert"] [data-testid="stAlertContentSuccess"] span {
    color: #14532d !important; font-weight: 600 !important;
}
/* Info */
div[data-testid="stAlert"] [data-testid="stAlertContentInfo"],
div[data-testid="stAlert"] [data-testid="stAlertContentInfo"] p,
div[data-testid="stAlert"] [data-testid="stAlertContentInfo"] span {
    color: #1e3a5f !important; font-weight: 600 !important;
}
/* Fallback */
div[data-testid="stAlert"] p,
div[data-testid="stAlert"] span { color: inherit !important; }

/* Footer */
.footer {
    text-align: center; font-size: 13px;
    padding: 16px 0 36px; color: #9ca3af;
}
.footer span { font-weight: 600; color: #3b82f6; letter-spacing: 2px; }

/* Scrollbar */
::-webkit-scrollbar       { width: 6px; }
::-webkit-scrollbar-track { background: #f1f5f9; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Ticker + Navbar ──────────────────────────────────────
st.markdown("""
<div class="ticker-wrap">
  <div class="ticker-track">
    <span class="ticker-item">🌤 Climate Matched Trips</span>
    <span class="ticker-item">🌍 AI Powered Travel</span>
    <span class="ticker-item">✈️ Smart Planning</span>
    <span class="ticker-item">🏨 Curated Stays</span>
    <span class="ticker-item">⭐ 4.9 Rating</span>
    <span class="ticker-item">🌤 Climate Matched Trips</span>
    <span class="ticker-item">🌍 AI Powered Travel</span>
    <span class="ticker-item">✈️ Smart Planning</span>
    <span class="ticker-item">🏨 Curated Stays</span>
    <span class="ticker-item">⭐ 4.9 Rating</span>
  </div>
</div>
<div class="navbar-shell"></div>
<div class="nav-brand">🌍 Smart Travel Planner</div>
""", unsafe_allow_html=True)

# ── Navbar back button ───────────────────────────────────
col1, col2, col3 = st.columns([10, 1, 1])
with col3:
    if st.button("🏠 Home"):
        st.switch_page("welcome.py")

st.markdown('<div class="page-spacer"></div>', unsafe_allow_html=True)

# ── DB ───────────────────────────────────────────────────
PAGES_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR  = os.path.dirname(PAGES_DIR)
DB_PATH   = os.path.join(BASE_DIR, "tourist.db")

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

# ── Hero ─────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
  <div class="hero-content">
    <span class="globe-icon">🌍</span>
    <div class="hero-title">Discover Your Next<br><span>Adventure</span></div>
    <div class="hero-sub">Personalised travel recommendations powered by Machine Learning</div>
    <div class="tag-row">
      <span class="tag tag-blue">✈️ Travel Smart</span>
      <span class="tag tag-pink">🗺️ Explore India</span>
      <span class="tag tag-cyan">🤖 ML Powered</span>
      <span class="tag tag-amber">⭐ Top Rated Places</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Stats ─────────────────────────────────────────────────
st.markdown("""
<div class="stats-row">
  <div class="stat-box">
    <div class="stat-icon stat-icon-blue">📍</div>
    <div>
      <div class="stat-number stat-num-blue">500+</div>
      <div class="stat-label">Destinations</div>
    </div>
  </div>
  <div class="stat-box">
    <div class="stat-icon stat-icon-green">👥</div>
    <div>
      <div class="stat-number stat-num-green">10K+</div>
      <div class="stat-label">Travellers</div>
    </div>
  </div>
  <div class="stat-box">
    <div class="stat-icon stat-icon-yellow">⭐</div>
    <div>
      <div class="stat-number stat-num-yellow">4.9★</div>
      <div class="stat-label">Avg Rating</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Form card ─────────────────────────────────────────────
st.markdown('<div class="form-card">', unsafe_allow_html=True)
st.markdown('<div class="form-title">👤 Create Your Profile</div>', unsafe_allow_html=True)

name             = st.text_input("Full Name", placeholder="e.g. Arjun Sharma")
if name and not name.strip().replace(" ", "").isalpha():
    st.markdown(
        '<p style="color:#7f1d1d;background:#fee2e2;border:1px solid #fca5a5;'
        'border-radius:8px;padding:6px 12px;font-size:13px;font-weight:600;margin-top:-8px;">'
        '⚠️ Name must contain alphabets only — no numbers or special characters.</p>',
        unsafe_allow_html=True
    )
password         = st.text_input("🔒 Password",         type="password", placeholder="Enter password")
confirm_password = st.text_input("🔐 Confirm Password", type="password", placeholder="Confirm password")
age              = st.number_input("Age", min_value=18, max_value=80, value=25, step=1)
budget           = st.selectbox("💰 Budget",  ["Low", "Medium", "High"])
climate          = st.selectbox("🌤 Climate", ["Hot", "Cold", "Moderate"])

st.markdown("<br>", unsafe_allow_html=True)

if st.button("🚀  Start Exploring →"):
    if not name.strip():
        st.warning("⚠️ Please enter your name to continue.")
    elif not name.strip().replace(" ", "").isalpha():
        st.error("❌ Name must contain alphabets only — no numbers or special characters.")
    elif not password:
        st.warning("⚠️ Please enter a password.")
    elif password != confirm_password:
        st.error("❌ Passwords do not match.")
    else:
        try:
            conn   = sqlite3.connect(DB_PATH)
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

# ── Footer ────────────────────────────────────────────────
st.markdown('<div class="footer"><span>✈️  EXPLORE  •  DISCOVER  •  TRAVEL</span></div>', unsafe_allow_html=True)