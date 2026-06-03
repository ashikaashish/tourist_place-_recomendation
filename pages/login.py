import streamlit as st
import sqlite3
import os
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import apply_styles

st.set_page_config(page_title="...", page_icon="🌍", layout="centered")
apply_styles()   # ← one line does everything
st.set_page_config(
    page_title="User Login",
    page_icon="🔑",
    layout="centered"
)
st.markdown("""
<style>
[data-testid="stSidebar"]        { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "tourist.db")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0f1e !important;
    font-family: 'DM Sans', sans-serif;
    overflow-x: hidden;
}

/* ── Animated background glow ── */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 70% 50% at 30% 0%,   rgba(56,189,248,0.16) 0%, transparent 65%),
        radial-gradient(ellipse 55% 40% at 80% 100%, rgba(99,102,241,0.13) 0%, transparent 65%),
        radial-gradient(ellipse 45% 35% at 5%  70%,  rgba(16,185,129,0.09) 0%, transparent 60%);
    animation: bgPulse 9s ease-in-out infinite alternate;
    pointer-events: none;
    z-index: 0;
}

@keyframes bgPulse {
    0%   { opacity: 0.6; transform: scale(1); }
    100% { opacity: 1;   transform: scale(1.05); }
}

/* Drifting star strip */
[data-testid="stAppViewContainer"]::after {
    content: '✦ ✧ ✦ ✧ ✦ ✧ ✦ ✧ ✦ ✧ ✦';
    position: fixed;
    top: 6%;
    left: 0; right: 0;
    text-align: center;
    font-size: 0.62rem;
    letter-spacing: 2.8rem;
    color: rgba(148,163,184,0.2);
    animation: drift 14s linear infinite;
    pointer-events: none;
    z-index: 0;
}

@keyframes drift {
    0%   { transform: translateX(-40px); opacity: 0.25; }
    50%  { opacity: 0.5; }
    100% { transform: translateX(40px);  opacity: 0.25; }
}

[data-testid="stVerticalBlock"] { position: relative; z-index: 1; }

/* ── Card ── */
.login-card {
    background: rgba(15, 23, 42, 0.84);
    border: 1px solid rgba(148,163,184,0.11);
    border-radius: 24px;
    padding: 2.8rem 2.4rem 2.4rem;
    margin: 1.5rem auto;
    max-width: 480px;
    box-shadow:
        0 0 0 1px rgba(56,189,248,0.05),
        0 30px 70px rgba(0,0,0,0.55),
        inset 0 1px 0 rgba(255,255,255,0.05);
    backdrop-filter: blur(22px);
    animation: cardEntry 0.85s cubic-bezier(0.16,1,0.3,1) both;
}

@keyframes cardEntry {
    from { opacity: 0; transform: translateY(44px) scale(0.97); }
    to   { opacity: 1; transform: translateY(0)    scale(1); }
}

/* ── Key icon ── */
.key-wrap {
    text-align: center;
    margin-bottom: 1rem;
    animation: keyDrop 0.7s cubic-bezier(0.34,1.56,0.64,1) 0.25s both;
}

@keyframes keyDrop {
    from { opacity: 0; transform: translateY(-28px) rotate(-20deg) scale(0.5); }
    to   { opacity: 1; transform: translateY(0)      rotate(0deg)   scale(1); }
}

.key-icon {
    font-size: 3.4rem;
    display: inline-block;
    filter: drop-shadow(0 0 16px rgba(56,189,248,0.5));
    animation: keyFloat 5s ease-in-out infinite;
}

@keyframes keyFloat {
    0%, 100% { transform: translateY(0px)   rotate(0deg); }
    50%       { transform: translateY(-8px)  rotate(6deg); }
}

/* ── Title ── */
.login-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(1.7rem, 3.5vw, 2.2rem);
    font-weight: 900;
    text-align: center;
    background: linear-gradient(135deg, #e0f2fe 0%, #38bdf8 50%, #818cf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: titleReveal 0.8s ease 0.4s both;
}

@keyframes titleReveal {
    from { opacity: 0; transform: translateY(14px); letter-spacing: 0.25em; }
    to   { opacity: 1; transform: translateY(0);    letter-spacing: normal; }
}

.login-subtitle {
    font-size: 0.82rem;
    font-weight: 500;
    color: #38bdf8;
    text-align: center;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-top: 0.3rem;
    animation: fadeUp 0.8s ease 0.55s both;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── Divider ── */
.divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(56,189,248,0.3), transparent);
    margin: 1.6rem 0 1.8rem;
    animation: fadeUp 0.8s ease 0.65s both;
}

/* ── Input labels ── */
.stTextInput label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    color: rgba(148,163,184,0.75) !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    margin-bottom: 0.3rem !important;
}

/* ── Input fields ── */
.stTextInput input {
    background: rgba(30,41,59,0.75) !important;
    border: 1px solid rgba(56,189,248,0.18) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.7rem 1rem !important;
    transition: border-color 0.25s ease, box-shadow 0.25s ease, background 0.25s ease !important;
    caret-color: #38bdf8 !important;
}

.stTextInput input:focus {
    border-color: rgba(56,189,248,0.6) !important;
    box-shadow: 0 0 0 3px rgba(56,189,248,0.12), 0 4px 16px rgba(56,189,248,0.1) !important;
    background: rgba(30,41,59,0.95) !important;
    outline: none !important;
}

.stTextInput input::placeholder { color: rgba(100,116,139,0.5) !important; }

/* Input wrapper slide-in */
div[data-testid="stTextInput"]:nth-of-type(1) { animation: fadeUp 0.8s ease 0.7s both; }
div[data-testid="stTextInput"]:nth-of-type(2) { animation: fadeUp 0.8s ease 0.82s both; }

/* ── Submit button ── */
div.stFormSubmitButton > button {
    width: 100% !important;
    padding: 0.88rem !important;
    border-radius: 14px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    background: linear-gradient(135deg, rgba(56,189,248,0.28), rgba(14,165,233,0.18)) !important;
    border: 1px solid rgba(56,189,248,0.45) !important;
    color: #7dd3fc !important;
    cursor: pointer !important;
    position: relative !important;
    overflow: hidden !important;
    box-shadow: 0 4px 20px rgba(56,189,248,0.16) !important;
    transition: all 0.3s cubic-bezier(0.34,1.56,0.64,1) !important;
    animation: fadeUp 0.8s ease 0.95s both;
}

div.stFormSubmitButton > button::before {
    content: '';
    position: absolute;
    top: 0; left: -100%; width: 60%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    transition: left 0.55s ease;
}

div.stFormSubmitButton > button:hover {
    background: linear-gradient(135deg, rgba(56,189,248,0.45), rgba(14,165,233,0.3)) !important;
    border-color: rgba(56,189,248,0.72) !important;
    color: #e0f2fe !important;
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 8px 30px rgba(56,189,248,0.3) !important;
}

div.stFormSubmitButton > button:hover::before { left: 160%; }

div.stFormSubmitButton > button:active {
    transform: translateY(-1px) scale(0.99) !important;
}

/* ── Alerts ── */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    animation: fadeUp 0.5s ease both;
}

/* ── Back link ── */
.back-link {
    text-align: center;
    font-size: 0.82rem;
    color: rgba(100,116,139,0.7);
    margin-top: 1.4rem;
    animation: fadeUp 0.8s ease 1.1s both;
}

.back-link a {
    color: #38bdf8;
    text-decoration: none;
    font-weight: 500;
    transition: color 0.2s;
}

.back-link a:hover { color: #7dd3fc; }

/* ── Footer ── */
.footer-text {
    text-align: center;
    font-size: 0.72rem;
    color: rgba(100,116,139,0.45);
    margin-top: 1.6rem;
    letter-spacing: 0.06em;
    animation: fadeUp 0.8s ease 1.2s both;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; }

.block-container {
    padding-top: 3.5rem !important;
    padding-bottom: 2rem !important;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────
st.markdown('<div class="key-wrap"><span class="key-icon">🔑</span></div>', unsafe_allow_html=True)
st.markdown('<h1 class="login-title">Welcome Back</h1>', unsafe_allow_html=True)
st.markdown('<p class="login-subtitle">Sign in to your account</p>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Login Form ────────────────────────────────────────────
with st.form("login_form"):
    username = st.text_input("👤  Username", placeholder="Enter your username")
    password = st.text_input("🔒  Password", placeholder="Enter your password", type="password")
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    login_btn = st.form_submit_button("🚀  Sign In")

if login_btn:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM users
        WHERE name=? AND password=?
    """, (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        st.session_state["username"] = username
        st.success(f"✅ Welcome back, {username}! Redirecting…")
        st.switch_page("pages/1_Recommendations.py")
    else:
        st.error("❌ Invalid username or password. Please try again.")
        st.markdown('</div>', unsafe_allow_html=True)
# Back button
if st.button("← Back to Home"):
    st.switch_page("welcome.py")

st.markdown("""
<p class="footer-text">© 2025 Smart Travel Planner · All rights reserved</p>
""", unsafe_allow_html=True)