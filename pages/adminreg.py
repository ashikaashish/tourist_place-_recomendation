import streamlit as st

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="Admin Login · Smart Travel Planner",
    page_icon="🔐",
    layout="centered"
)

# ---------------------------------------------------
# CSS — same theme as login.py
# ---------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800;900&display=swap');

* { font-family: 'Poppins', sans-serif; font-weight: 700; box-sizing: border-box; margin: 0; padding: 0; }

/* Hide Streamlit chrome */
header, [data-testid="stHeader"], [data-testid="stToolbar"],
[data-testid="stDecoration"], #MainMenu, footer,
[data-testid="stSidebar"], [data-testid="collapsedControl"] {
    display: none !important;
}
.block-container { padding-top: 0 !important; max-width: 100% !important; }

/* ── Home.py style background ── */
html, body, .stApp {
    background: #f0f4fa !important;
}
.stApp::before {
    content: '';
    position: fixed; inset: 0; z-index: 0;
    background: transparent;
}
.stApp::after {
    content: '';
    position: fixed; inset: 0; z-index: 1;
    background: transparent;
}
/* Make sure all content sits above the background layers */
.stApp > * { position: relative; z-index: 2; }

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
    font-size: 11px; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.8px;
}
@keyframes tickerScroll {
    0%   { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}

/* ── Navbar ── */
.navbar-shell {
    position: fixed; top: 34px; left: 0; right: 0; height: 64px; z-index: 1500;
    background: rgba(255,255,255,0.88);
    backdrop-filter: blur(24px);
    border-bottom: 1px solid rgba(255,255,255,0.6);
    box-shadow: 0 2px 20px rgba(0,0,0,0.12);
}
.nav-brand {
    position: fixed; top: 34px; left: 2.5rem; height: 64px;
    display: flex; align-items: center; z-index: 1600;
    font-weight: 800; font-size: 18px; color: #1a1814;
    letter-spacing: -0.3px;
}

/* Spacer under fixed bars */
.page-spacer { height: 114px; }

/* Navbar back button */
div[data-testid="stHorizontalBlock"] {
    position: fixed !important; top: 34px !important;
    right: 2.5rem !important; height: 64px !important;
    z-index: 2000 !important; background: transparent !important;
    display: flex !important; align-items: center !important;
}
div[data-testid="stHorizontalBlock"] .stButton > button {
    width: auto !important; height: 38px !important;
    padding: 0 20px !important; font-size: 13px !important;
    font-weight: 700 !important;
    background: #f1f5f9 !important; color: #374151 !important;
    border: 1.5px solid #d1d5db !important;
    border-radius: 10px !important;
    box-shadow: none !important; animation: none !important;
    margin-top: 0 !important;
}
div[data-testid="stHorizontalBlock"] .stButton > button:hover {
    background: #e2e8f0 !important; transform: translateY(-1px) !important;
}

/* ── Page outer layout ── */
.login-outer {
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    min-height: calc(100vh - 114px);
    padding: 32px 16px 48px;
}

/* ── Hero badge ── */
.hero-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(59,130,246,0.10);
    border: 1px solid rgba(59,130,246,0.25);
    border-radius: 999px;
    padding: 6px 16px;
    font-size: 12px; font-weight: 700;
    color: #3b82f6; letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 20px;
}

.login-hero{
    margin:0 auto 30px;
    max-width:900px;
    min-height:280px;
    border-radius:20px;
    overflow:hidden;
    background:url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1400&q=80') center/cover no-repeat;
    display:flex;
    align-items:center;
    justify-content:center;
    text-align:center;
    position:relative;
}
.login-hero::before{
    content:'';
    position:absolute;
    inset:0;
    background:rgba(255,255,255,0.18);
}
.hero-content{
    position:relative;
    z-index:2;
}
.hero-content h1{
    font-size:42px;
    font-weight:800;
    color:#1a1814;
}
.hero-content p{
    color:#374151;
    font-size:15px;
}

/* ── Card ── */
.login-card {
    background: rgba(255,255,255,0.92);
    backdrop-filter: blur(28px) saturate(1.4);
    -webkit-backdrop-filter: blur(28px) saturate(1.4);
    border: 1px solid rgba(255,255,255,0.75);
    border-radius: 28px;
    padding: 44px 40px 36px;
    width: 100%; max-width: 500px;
    box-shadow: 0 24px 80px rgba(0,0,0,0.35), 0 4px 16px rgba(0,0,0,0.15);
    animation: cardEntry 0.65s cubic-bezier(0.16,1,0.3,1) both;
}
@keyframes cardEntry {
    from { opacity: 0; transform: translateY(36px) scale(0.97); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
}

/* ── Globe icon ── */
.globe-wrap {
    text-align: center; margin-bottom: 14px;
}
.globe-icon {
    font-size: 64px; display: inline-block;
    filter: drop-shadow(0 4px 12px rgba(59,130,246,0.3));
    animation: globeFloat 4s ease-in-out infinite;
}
@keyframes globeFloat {
    0%, 100% { transform: translateY(0) rotate(-3deg); }
    50%       { transform: translateY(-10px) rotate(3deg); }
}

/* ── Title ── */
.login-title {
    font-size: 38px; font-weight: 900;
    color: #0f172a; text-align: center;
    margin-bottom: 6px; line-height: 1.1;
    letter-spacing: -1px;
}
.login-title .highlight { color: #3b82f6; }
.login-subtitle {
    font-size: 15px; font-weight: 500;
    color: #64748b;
    text-align: center; margin-bottom: 28px;
    letter-spacing: 0.01em;
}

/* ── Divider ── */
.divider {
    border: none; height: 1px;
    background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
    margin: 0 0 28px;
}

/* ── Stats strip ── */
.stats-strip {
    display: flex; justify-content: center; gap: 24px;
    margin-bottom: 28px;
}
.stat-pill {
    display: flex; flex-direction: column; align-items: center;
    background: #f8fafc; border: 1px solid #e2e8f0;
    border-radius: 14px; padding: 10px 20px;
    min-width: 100px;
}
.stat-num {
    font-size: 20px; font-weight: 900;
    color: #3b82f6; line-height: 1;
}
.stat-lbl {
    font-size: 10px; font-weight: 700;
    color: #94a3b8; text-transform: uppercase;
    letter-spacing: 0.06em; margin-top: 3px;
}

/* ── Input labels ── */
label, .stTextInput label {
    color: #1e293b !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
    text-transform: uppercase !important;
}

/* ── Input fields ── */
input[type="text"], input[type="password"] {
    background: #f8fafc !important;
    color: #0f172a !important;
    border: 2px solid #e2e8f0 !important;
    border-radius: 14px !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
input[type="text"]:focus, input[type="password"]:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 4px rgba(59,130,246,0.12) !important;
    outline: none !important;
    background: #ffffff !important;
}
input::placeholder { color: #94a3b8 !important; font-weight: 400 !important; }

/* ── Submit button ── */
div.stFormSubmitButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #2563eb 0%, #6366f1 100%) !important;
    color: #ffffff !important; border: none !important;
    border-radius: 16px !important; padding: 16px 24px !important;
    font-size: 16px !important; font-weight: 800 !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 6px 24px rgba(37,99,235,0.40) !important;
    margin-top: 10px !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
}
div.stFormSubmitButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 12px 32px rgba(37,99,235,0.50) !important;
}
div.stFormSubmitButton > button:active { transform: translateY(0) !important; }

/* ── Back button ── */
.stButton > button {
    width: 100% !important;
    background: #f1f5f9 !important;
    color: #475569 !important;
    border: 2px solid #e2e8f0 !important;
    border-radius: 16px !important; padding: 13px 24px !important;
    font-size: 14px !important; font-weight: 700 !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    box-shadow: none !important; margin-top: 8px !important;
    letter-spacing: 0.02em !important;
}
.stButton > button:hover {
    background: #e2e8f0 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08) !important;
}

/* ── Alerts ── */
div[data-testid="stAlert"] {
    border-radius: 14px !important; font-size: 14px !important;
    font-weight: 600 !important;
    animation: fadeUp 0.4s ease both;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── Divider text ── */
.or-divider {
    display: flex; align-items: center; gap: 12px;
    margin: 20px 0 4px; color: #94a3b8;
    font-size: 12px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.08em;
}
.or-divider::before, .or-divider::after {
    content: ''; flex: 1; height: 1px; background: #e2e8f0;
}

/* ── Footer ── */
.footer-text {
    text-align: center; font-size: 12px;
    color: #94a3b8; margin-top: 24px;
    font-weight: 500; letter-spacing: 0.04em;
}

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
    <span class="ticker-item">🔐 Restricted Access</span>
    <span class="ticker-item">🛡️ Admin Console</span>
    <span class="ticker-item">⚙️ System Control</span>
    <span class="ticker-item">📊 Manage Platform</span>
    <span class="ticker-item">⭐ 4.9 Rating</span>
    <span class="ticker-item">🔐 Restricted Access</span>
    <span class="ticker-item">🛡️ Admin Console</span>
    <span class="ticker-item">⚙️ System Control</span>
    <span class="ticker-item">📊 Manage Platform</span>
    <span class="ticker-item">⭐ 4.9 Rating</span>
  </div>
</div>
<div class="navbar-shell"></div>
<div class="nav-brand">🌍 Smart Travel Planner</div>
""", unsafe_allow_html=True)

# ── Navbar back button ───────────────────────────────────
col1, col2, col3 = st.columns([10, 1, 1])
with col3:
    if st.button("🏠 Home", key="nav_home"):
        st.switch_page("welcome.py")

st.markdown('<div class="page-spacer"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="login-hero">
    <div class="hero-content">
        <div style="font-size:70px;">🔐</div>
        <h1>Admin Portal</h1>
        <p>Restricted access · Authorised personnel only</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Admin Credentials ─────────────────────────────────────
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# ── Admin Login Form ──────────────────────────────────────
with st.form("admin_login_form"):
    username  = st.text_input("🛡️  Admin Username", placeholder="Enter admin username")
    password  = st.text_input("🔒  Admin Password", placeholder="Enter admin password", type="password")
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    login_btn = st.form_submit_button("🔓  Access Dashboard")

if login_btn:
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        st.session_state["admin"] = True
        st.success("✅ Admin verified. Redirecting to dashboard…")
        st.switch_page("pages/admin.py")
    else:
        st.error("❌ Invalid admin credentials. Access denied.")



# ── Footer ────────────────────────────────────────────────
st.markdown("""
<p class="footer-text">© 2025 Smart Travel Planner · Admin Console</p>
""", unsafe_allow_html=True)