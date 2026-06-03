import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import apply_styles

st.set_page_config(page_title="...", page_icon="🌍", layout="centered")
apply_styles()   # ← one line does everything
st.set_page_config(
    page_title="Admin Login",
    page_icon="🔐",
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
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0f1e !important;
    font-family: 'DM Sans', sans-serif;
    overflow-x: hidden;
}

/* ── Background glows — violet/indigo tones for admin ── */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 70% 50% at 70%  0%,  rgba(99,102,241,0.20) 0%, transparent 65%),
        radial-gradient(ellipse 55% 40% at 20% 100%, rgba(168,85,247,0.14) 0%, transparent 65%),
        radial-gradient(ellipse 45% 35% at 95%  60%, rgba(56,189,248,0.09) 0%, transparent 60%);
    animation: bgPulse 9s ease-in-out infinite alternate;
    pointer-events: none;
    z-index: 0;
}

@keyframes bgPulse {
    0%   { opacity: 0.65; transform: scale(1); }
    100% { opacity: 1;    transform: scale(1.05); }
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
    color: rgba(148,163,184,0.18);
    animation: drift 14s linear infinite;
    pointer-events: none;
    z-index: 0;
}

@keyframes drift {
    0%   { transform: translateX(-40px); opacity: 0.2; }
    50%  { opacity: 0.45; }
    100% { transform: translateX(40px);  opacity: 0.2; }
}

[data-testid="stVerticalBlock"] { position: relative; z-index: 1; }

/* ── Card ── */
.admin-card {
    background: rgba(15, 23, 42, 0.86);
    border: 1px solid rgba(99,102,241,0.18);
    border-radius: 24px;
    padding: 2.8rem 2.4rem 2.4rem;
    margin: 1.5rem auto;
    max-width: 480px;
    box-shadow:
        0 0 0 1px rgba(99,102,241,0.07),
        0 30px 70px rgba(0,0,0,0.55),
        inset 0 1px 0 rgba(255,255,255,0.05);
    backdrop-filter: blur(22px);
    animation: cardEntry 0.85s cubic-bezier(0.16,1,0.3,1) both;
}

@keyframes cardEntry {
    from { opacity: 0; transform: translateY(44px) scale(0.97); }
    to   { opacity: 1; transform: translateY(0)    scale(1); }
}

/* ── Shield / lock icon ── */
.shield-wrap {
    text-align: center;
    margin-bottom: 1rem;
    animation: shieldDrop 0.75s cubic-bezier(0.34,1.56,0.64,1) 0.25s both;
}

@keyframes shieldDrop {
    from { opacity: 0; transform: translateY(-30px) scale(0.4); }
    to   { opacity: 1; transform: translateY(0)      scale(1); }
}

.shield-icon {
    font-size: 3.4rem;
    display: inline-block;
    filter: drop-shadow(0 0 18px rgba(99,102,241,0.65));
    animation: shieldPulse 4s ease-in-out infinite;
}

@keyframes shieldPulse {
    0%, 100% { transform: scale(1);    filter: drop-shadow(0 0 18px rgba(99,102,241,0.65)); }
    50%       { transform: scale(1.07); filter: drop-shadow(0 0 28px rgba(168,85,247,0.75)); }
}

/* ── Title ── */
.admin-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(1.7rem, 3.5vw, 2.2rem);
    font-weight: 900;
    text-align: center;
    background: linear-gradient(135deg, #e0e7ff 0%, #a5b4fc 45%, #c084fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: titleReveal 0.8s ease 0.4s both;
}

@keyframes titleReveal {
    from { opacity: 0; transform: translateY(14px); letter-spacing: 0.25em; }
    to   { opacity: 1; transform: translateY(0);    letter-spacing: normal; }
}

.admin-subtitle {
    font-size: 0.8rem;
    font-weight: 500;
    color: #a5b4fc;
    text-align: center;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    margin-top: 0.35rem;
    animation: fadeUp 0.8s ease 0.55s both;
}

/* ── Access badge ── */
.access-badge {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    background: rgba(99,102,241,0.1);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 100px;
    padding: 0.35rem 1.1rem;
    width: fit-content;
    margin: 1rem auto 0;
    font-size: 0.75rem;
    font-weight: 500;
    color: #a5b4fc;
    letter-spacing: 0.1em;
    animation: fadeUp 0.8s ease 0.65s both;
}

.badge-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #a5b4fc;
    box-shadow: 0 0 6px rgba(165,180,252,0.8);
    animation: dotBlink 2s ease-in-out infinite;
}

@keyframes dotBlink {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.4; transform: scale(0.7); }
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── Divider ── */
.divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,102,241,0.35), transparent);
    margin: 1.6rem 0 1.8rem;
    animation: fadeUp 0.8s ease 0.72s both;
}

/* ── Input labels ── */
.stTextInput label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    color: rgba(148,163,184,0.7) !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    margin-bottom: 0.3rem !important;
}

/* ── Input fields ── */
.stTextInput input {
    background: rgba(30,41,59,0.75) !important;
    border: 1px solid rgba(99,102,241,0.2) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.7rem 1rem !important;
    transition: border-color 0.25s ease, box-shadow 0.25s ease, background 0.25s ease !important;
    caret-color: #a5b4fc !important;
}

.stTextInput input:focus {
    border-color: rgba(99,102,241,0.65) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.13), 0 4px 16px rgba(99,102,241,0.12) !important;
    background: rgba(30,41,59,0.95) !important;
    outline: none !important;
}

.stTextInput input::placeholder { color: rgba(100,116,139,0.45) !important; }

div[data-testid="stTextInput"]:nth-of-type(1) { animation: fadeUp 0.8s ease 0.78s both; }
div[data-testid="stTextInput"]:nth-of-type(2) { animation: fadeUp 0.8s ease 0.9s  both; }

/* ── Submit button ── */
div.stFormSubmitButton > button {
    width: 100% !important;
    padding: 0.88rem !important;
    border-radius: 14px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.94rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.07em !important;
    text-transform: uppercase !important;
    background: linear-gradient(135deg, rgba(99,102,241,0.3), rgba(79,70,229,0.18)) !important;
    border: 1px solid rgba(99,102,241,0.48) !important;
    color: #a5b4fc !important;
    cursor: pointer !important;
    position: relative !important;
    overflow: hidden !important;
    box-shadow: 0 4px 20px rgba(99,102,241,0.18) !important;
    transition: all 0.3s cubic-bezier(0.34,1.56,0.64,1) !important;
    animation: fadeUp 0.8s ease 1.02s both;
}

div.stFormSubmitButton > button::before {
    content: '';
    position: absolute;
    top: 0; left: -100%; width: 60%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    transition: left 0.55s ease;
}

div.stFormSubmitButton > button:hover {
    background: linear-gradient(135deg, rgba(99,102,241,0.48), rgba(79,70,229,0.3)) !important;
    border-color: rgba(99,102,241,0.75) !important;
    color: #e0e7ff !important;
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 8px 30px rgba(99,102,241,0.32) !important;
}

div.stFormSubmitButton > button:hover::before { left: 160%; }
div.stFormSubmitButton > button:active { transform: translateY(-1px) scale(0.99) !important; }

/* ── Alerts ── */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    animation: fadeUp 0.5s ease both;
}

/* ── Footer ── */
.footer-text {
    text-align: center;
    font-size: 0.72rem;
    color: rgba(100,116,139,0.4);
    margin-top: 1.6rem;
    letter-spacing: 0.06em;
    animation: fadeUp 0.8s ease 1.15s both;
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
st.markdown('<div class="shield-wrap"><span class="shield-icon">🔐</span></div>', unsafe_allow_html=True)
st.markdown('<h1 class="admin-title">Admin Portal</h1>', unsafe_allow_html=True)
st.markdown('<p class="admin-subtitle">Restricted Access</p>', unsafe_allow_html=True)
st.markdown("""
<div class="access-badge">
    <span class="badge-dot"></span>
    Authorised Personnel Only
</div>
""", unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Admin Credentials ─────────────────────────────────────
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# ── Form ──────────────────────────────────────────────────
with st.form("admin_login_form"):
    username = st.text_input("🛡️  Admin Username", placeholder="Enter admin username")
    password = st.text_input("🔒  Admin Password", placeholder="Enter admin password", type="password")
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    login_btn = st.form_submit_button("🔓  Access Dashboard")

if login_btn:
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        st.session_state["admin"] = True
        st.success("✅ Admin verified. Redirecting to dashboard…")
        st.switch_page("pages/admin.py")
    else:
        st.error("❌ Invalid admin credentials. Access denied.")
        st.markdown('</div>', unsafe_allow_html=True)
# Back button
if st.button("← Back to Home"):
    st.switch_page("welcome.py")

st.markdown('<p class="footer-text">© 2025 Smart Travel Planner · Admin Console</p>', unsafe_allow_html=True)