import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import apply_styles

st.set_page_config(page_title="...", page_icon="🌍", layout="centered")
apply_styles()   # ← one line does everything
st.set_page_config(
    page_title="Tourist Recommendation System",
    page_icon="🌍",
    layout="centered"
)
st.markdown("""
<style>
[data-testid="stSidebar"]        { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0f1e !important;
    font-family: 'DM Sans', sans-serif;
    overflow-x: hidden;
}

/* ── Animated starfield background ── */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 60% at 50% -10%, rgba(56,189,248,0.18) 0%, transparent 70%),
        radial-gradient(ellipse 60% 40% at 90% 100%, rgba(99,102,241,0.14) 0%, transparent 70%),
        radial-gradient(ellipse 50% 30% at 0% 80%, rgba(16,185,129,0.10) 0%, transparent 60%);
    animation: bgPulse 8s ease-in-out infinite alternate;
    pointer-events: none;
    z-index: 0;
}

@keyframes bgPulse {
    0%   { opacity: 0.7; transform: scale(1); }
    100% { opacity: 1;   transform: scale(1.04); }
}

/* Floating particles */
[data-testid="stAppViewContainer"]::after {
    content: '✦ ✧ ✦ ✧ ✦ ✧ ✦ ✧ ✦ ✧ ✦';
    position: fixed;
    top: 8%;
    left: 0;
    right: 0;
    text-align: center;
    font-size: 0.65rem;
    letter-spacing: 2.5rem;
    color: rgba(148,163,184,0.25);
    animation: drift 12s linear infinite;
    pointer-events: none;
    z-index: 0;
}

@keyframes drift {
    0%   { transform: translateX(-40px); opacity: 0.3; }
    50%  { opacity: 0.6; }
    100% { transform: translateX(40px);  opacity: 0.3; }
}

/* ── Main block wrapper ── */
[data-testid="stVerticalBlock"] {
    position: relative;
    z-index: 1;
}

/* ── Card container ── */
.main-card {
    background: rgba(15, 23, 42, 0.82);
    border: 1px solid rgba(148,163,184,0.12);
    border-radius: 24px;
    padding: 3rem 2.5rem 2.5rem;
    margin: 2rem auto;
    max-width: 640px;
    box-shadow:
        0 0 0 1px rgba(56,189,248,0.06),
        0 25px 60px rgba(0,0,0,0.55),
        inset 0 1px 0 rgba(255,255,255,0.06);
    backdrop-filter: blur(20px);
    animation: cardEntry 0.9s cubic-bezier(0.16,1,0.3,1) both;
}

@keyframes cardEntry {
    from { opacity: 0; transform: translateY(40px) scale(0.97); }
    to   { opacity: 1; transform: translateY(0)   scale(1); }
}

/* ── Globe icon ── */
.globe-wrap {
    text-align: center;
    margin-bottom: 1.2rem;
    animation: globeSpin 0.7s cubic-bezier(0.34,1.56,0.64,1) 0.3s both;
}

@keyframes globeSpin {
    from { opacity: 0; transform: scale(0.4) rotate(-30deg); }
    to   { opacity: 1; transform: scale(1)   rotate(0deg); }
}

.globe-icon {
    font-size: 4rem;
    display: inline-block;
    animation: float 5s ease-in-out infinite;
    filter: drop-shadow(0 0 18px rgba(56,189,248,0.55));
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50%       { transform: translateY(-10px); }
}

/* ── Title ── */
.main-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(1.8rem, 4vw, 2.6rem);
    font-weight: 900;
    text-align: center;
    line-height: 1.15;
    background: linear-gradient(135deg, #e0f2fe 0%, #38bdf8 45%, #818cf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: titleReveal 0.9s ease 0.45s both;
}

@keyframes titleReveal {
    from { opacity: 0; transform: translateY(16px); letter-spacing: 0.3em; }
    to   { opacity: 1; transform: translateY(0);    letter-spacing: normal; }
}

/* ── Subtitle ── */
.sub-title {
    font-family: 'DM Sans', sans-serif;
    font-size: 1rem;
    font-weight: 500;
    text-align: center;
    color: #38bdf8;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-top: 0.4rem;
    animation: fadeUp 0.8s ease 0.6s both;
}

/* ── Description ── */
.desc-text {
    font-size: 0.95rem;
    color: rgba(148,163,184,0.85);
    text-align: center;
    line-height: 1.7;
    margin: 1.4rem auto 0.5rem;
    max-width: 420px;
    animation: fadeUp 0.8s ease 0.75s both;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── Divider ── */
.divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(56,189,248,0.35), transparent);
    margin: 1.8rem 0 2rem;
    animation: fadeUp 0.8s ease 0.85s both;
}

/* ── Feature pills ── */
.pills-row {
    display: flex;
    justify-content: center;
    gap: 0.6rem;
    flex-wrap: wrap;
    margin-bottom: 2rem;
    animation: fadeUp 0.8s ease 0.9s both;
}

.pill {
    background: rgba(56,189,248,0.09);
    border: 1px solid rgba(56,189,248,0.22);
    color: #7dd3fc;
    border-radius: 100px;
    padding: 0.3rem 0.9rem;
    font-size: 0.78rem;
    font-weight: 500;
    letter-spacing: 0.04em;
    transition: background 0.2s, border-color 0.2s;
}

.pill:hover {
    background: rgba(56,189,248,0.18);
    border-color: rgba(56,189,248,0.5);
}

/* ── Button label ── */
.btn-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.72rem;
    font-weight: 500;
    color: rgba(148,163,184,0.5);
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    margin-bottom: 0.8rem;
    animation: fadeUp 0.8s ease 1s both;
}

/* ── Streamlit button overrides ── */
[data-testid="stHorizontalBlock"] {
    gap: 1rem !important;
    animation: fadeUp 0.8s ease 1.05s both;
}

div.stButton > button {
    width: 100% !important;
    padding: 0.85rem 1rem !important;
    border-radius: 14px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.93rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.03em !important;
    border: 1px solid rgba(148,163,184,0.15) !important;
    background: rgba(30,41,59,0.7) !important;
    color: #e2e8f0 !important;
    cursor: pointer !important;
    transition: all 0.28s cubic-bezier(0.34,1.56,0.64,1) !important;
    position: relative !important;
    overflow: hidden !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
}

/* Shimmer sweep on hover */
div.stButton > button::before {
    content: '';
    position: absolute;
    top: 0; left: -100%; width: 60%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
    transition: left 0.5s ease;
}

div.stButton > button:hover::before { left: 160%; }

/* Register button */
[data-testid="stHorizontalBlock"] > div:nth-child(1) button {
    background: linear-gradient(135deg, rgba(16,185,129,0.25), rgba(6,148,105,0.15)) !important;
    border-color: rgba(16,185,129,0.45) !important;
    color: #6ee7b7 !important;
    box-shadow: 0 4px 20px rgba(16,185,129,0.18) !important;
}

[data-testid="stHorizontalBlock"] > div:nth-child(1) button:hover {
    background: linear-gradient(135deg, rgba(16,185,129,0.4), rgba(6,148,105,0.25)) !important;
    border-color: rgba(16,185,129,0.7) !important;
    transform: translateY(-3px) scale(1.03) !important;
    box-shadow: 0 8px 28px rgba(16,185,129,0.32) !important;
}

/* Login button */
[data-testid="stHorizontalBlock"] > div:nth-child(2) button {
    background: linear-gradient(135deg, rgba(56,189,248,0.22), rgba(14,165,233,0.12)) !important;
    border-color: rgba(56,189,248,0.42) !important;
    color: #7dd3fc !important;
    box-shadow: 0 4px 20px rgba(56,189,248,0.15) !important;
}

[data-testid="stHorizontalBlock"] > div:nth-child(2) button:hover {
    background: linear-gradient(135deg, rgba(56,189,248,0.38), rgba(14,165,233,0.22)) !important;
    border-color: rgba(56,189,248,0.68) !important;
    transform: translateY(-3px) scale(1.03) !important;
    box-shadow: 0 8px 28px rgba(56,189,248,0.3) !important;
}

/* Admin Login button */
[data-testid="stHorizontalBlock"] > div:nth-child(3) button {
    background: linear-gradient(135deg, rgba(99,102,241,0.22), rgba(79,70,229,0.12)) !important;
    border-color: rgba(99,102,241,0.42) !important;
    color: #a5b4fc !important;
    box-shadow: 0 4px 20px rgba(99,102,241,0.15) !important;
}

[data-testid="stHorizontalBlock"] > div:nth-child(3) button:hover {
    background: linear-gradient(135deg, rgba(99,102,241,0.38), rgba(79,70,229,0.22)) !important;
    border-color: rgba(99,102,241,0.68) !important;
    transform: translateY(-3px) scale(1.03) !important;
    box-shadow: 0 8px 28px rgba(99,102,241,0.3) !important;
}

div.stButton > button:active {
    transform: translateY(-1px) scale(0.99) !important;
}

/* ── Footer ── */
.footer-text {
    text-align: center;
    font-size: 0.75rem;
    color: rgba(100,116,139,0.6);
    margin-top: 1.8rem;
    letter-spacing: 0.06em;
    animation: fadeUp 0.8s ease 1.2s both;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; }

/* Tighten up Streamlit's default padding */
.block-container {
    padding-top: 3rem !important;
    padding-bottom: 2rem !important;
}
</style>
""", unsafe_allow_html=True)

# ── Hero section ──────────────────────────────────────────
st.markdown('<div class="globe-wrap"><span class="globe-icon">🌍</span></div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">Tourist Recommendation<br>System</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Smart Travel Planner</p>', unsafe_allow_html=True)

st.markdown("""
<center>
    <p class="desc-text">
        Discover destinations tailored to your budget,
        climate preference, and travel dreams.
    </p>
</center>
""", unsafe_allow_html=True)

st.markdown("""
<div class="pills-row">
    <span class="pill">🗺️ Destinations</span>
    <span class="pill">💰 Budget Filter</span>
    <span class="pill">🌤️ Climate Match</span>
    <span class="pill">📅 Trip Planner</span>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Action buttons ────────────────────────────────────────
st.markdown('<p class="btn-label">Get started</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📝  Register"):
        st.switch_page("pages/home.py")

with col2:
    if st.button("👤  Login"):
        st.switch_page("pages/login.py")

with col3:
    if st.button("🔐  Admin"):
        st.switch_page("pages/adminreg.py")

st.markdown('<p class="footer-text">© 2025 Smart Travel Planner · All rights reserved</p>', unsafe_allow_html=True)