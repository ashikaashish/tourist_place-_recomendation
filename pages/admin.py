import streamlit as st
import pandas as pd
import sqlite3
import os

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="Admin Dashboard · Smart Travel Planner",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------
# CSS — same theme as login.py / adminreg.py
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

/* ── Background ── */
html, body, .stApp {
    background: #f0f4fa !important;
}
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

/* ── Hero ── */
.dash-hero{
    margin: 0 auto 30px;
    max-width: 1200px;
    min-height: 220px;
    border-radius: 20px;
    overflow: hidden;
    background: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1400&q=80') center/cover no-repeat;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    position: relative;
}
.dash-hero::before{
    content: '';
    position: absolute;
    inset: 0;
    background: rgba(255,255,255,0.30);
}
.hero-content{
    position: relative;
    z-index: 2;
}
.hero-content h1{
    font-size: 38px;
    font-weight: 800;
    color: #1a1814;
}
.hero-content p{
    color: #374151;
    font-size: 15px;
}

/* ── Content container ── */
.dash-wrap {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 16px 60px;
}

/* ── Section cards ── */
.section-card {
    background: rgba(255,255,255,0.92);
    backdrop-filter: blur(20px) saturate(1.4);
    -webkit-backdrop-filter: blur(20px) saturate(1.4);
    border: 1px solid rgba(255,255,255,0.75);
    border-radius: 20px;
    padding: 24px 28px;
    margin-bottom: 28px;
    box-shadow: 0 12px 40px rgba(0,0,0,0.10);
}

.section-card h3,
.section-card div[data-testid="stMarkdownContainer"] h3,
div[data-testid="stMarkdownContainer"] h3,
.stMarkdown h3,
h3 {
    font-size: 22px !important;
    font-weight: 800 !important;
    color: #0f172a !important;
    margin-bottom: 16px !important;
    letter-spacing: -0.3px !important;
    padding-bottom: 10px !important;
    border-bottom: 2px solid #e2e8f0 !important;
    opacity: 1 !important;
}

.section-card .stTextInput input {
    margin-bottom: 4px !important;
}

/* Search label text color */
.section-card .stTextInput label,
.stTextInput label,
label[data-testid="stWidgetLabel"],
div[data-testid="stTextInput"] label,
div[data-testid="stTextInput"] label p {
    color: #0f172a !important;
    font-weight: 700 !important;
    opacity: 1 !important;
}

.section-card .stDownloadButton > button {
    background: linear-gradient(135deg, #2563eb 0%, #6366f1 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 10px 20px !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
    box-shadow: 0 4px 14px rgba(37,99,235,0.30) !important;
    margin-top: 10px !important;
    transition: all 0.25s ease !important;
}
.section-card .stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 22px rgba(37,99,235,0.40) !important;
}

/* ── Dataframe styling ── */
[data-testid="stDataFrame"] {
    border-radius: 14px !important;
    overflow: hidden !important;
    border: 2px solid #e2e8f0 !important;
}

/* ── Alerts ── */
div[data-testid="stAlert"] {
    border-radius: 14px !important; font-size: 14px !important;
    font-weight: 600 !important;
}

/* ── Back button ── */
.stButton > button {
    background: #f1f5f9 !important;
    color: #475569 !important;
    border: 2px solid #e2e8f0 !important;
    border-radius: 16px !important; padding: 13px 24px !important;
    font-size: 14px !important; font-weight: 700 !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    box-shadow: none !important;
    letter-spacing: 0.02em !important;
}
.stButton > button:hover {
    background: #e2e8f0 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08) !important;
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
    <span class="ticker-item">📊 Admin Dashboard</span>
    <span class="ticker-item">👤 User Management</span>
    <span class="ticker-item">⭐ Ratings Overview</span>
    <span class="ticker-item">❤️ Liked Places</span>
    <span class="ticker-item">🏆 Top Destinations</span>
    <span class="ticker-item">📊 Admin Dashboard</span>
    <span class="ticker-item">👤 User Management</span>
    <span class="ticker-item">⭐ Ratings Overview</span>
    <span class="ticker-item">❤️ Liked Places</span>
    <span class="ticker-item">🏆 Top Destinations</span>
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

# ── Hero ──────────────────────────────────────────────────
st.markdown("""
<div class="dash-hero">
    <div class="hero-content">
        <div style="font-size:60px;">📊</div>
        <h1>Admin Dashboard</h1>
        <p>Overview of users, ratings, likes and top destinations</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="dash-wrap">', unsafe_allow_html=True)

# Database Connection
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH  = os.path.join(BASE_DIR, "tourist.db")
conn = sqlite3.connect(DB_PATH)

# -----------------------------
# Registered Users
# -----------------------------
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<h3>👤 Registered Users</h3>', unsafe_allow_html=True)
try:
    users = pd.read_sql("SELECT * FROM users", conn)

    search_users = st.text_input("🔍 Search users", key="search_users", placeholder="Search by any field…")
    if search_users:
        mask = users.apply(lambda row: row.astype(str).str.contains(search_users, case=False, na=False).any(), axis=1)
        filtered_users = users[mask]
    else:
        filtered_users = users

    st.dataframe(filtered_users, use_container_width=True)

    st.download_button(
        "⬇️ Download Users CSV",
        data=filtered_users.to_csv(index=False).encode("utf-8"),
        file_name="users.csv",
        mime="text/csv",
        key="download_users"
    )
except Exception:
    st.warning("No users found.")
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Ratings
# -----------------------------
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<h3>⭐ User Ratings</h3>', unsafe_allow_html=True)
try:
    ratings = pd.read_sql("SELECT * FROM ratings", conn)

    search_ratings = st.text_input("🔍 Search ratings", key="search_ratings", placeholder="Search by any field…")
    if search_ratings:
        mask = ratings.apply(lambda row: row.astype(str).str.contains(search_ratings, case=False, na=False).any(), axis=1)
        filtered_ratings = ratings[mask]
    else:
        filtered_ratings = ratings

    st.dataframe(filtered_ratings, use_container_width=True)

    st.download_button(
        "⬇️ Download Ratings CSV",
        data=filtered_ratings.to_csv(index=False).encode("utf-8"),
        file_name="ratings.csv",
        mime="text/csv",
        key="download_ratings"
    )
except Exception:
    st.warning("No ratings found.")
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Likes
# -----------------------------
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<h3>❤️ Liked Places</h3>', unsafe_allow_html=True)
try:
    likes = pd.read_sql("SELECT * FROM likes", conn)

    search_likes = st.text_input("🔍 Search likes", key="search_likes", placeholder="Search by any field…")
    if search_likes:
        mask = likes.apply(lambda row: row.astype(str).str.contains(search_likes, case=False, na=False).any(), axis=1)
        filtered_likes = likes[mask]
    else:
        filtered_likes = likes

    st.dataframe(filtered_likes, use_container_width=True)

    st.download_button(
        "⬇️ Download Likes CSV",
        data=filtered_likes.to_csv(index=False).encode("utf-8"),
        file_name="likes.csv",
        mime="text/csv",
        key="download_likes"
    )
except Exception:
    st.warning("No likes found.")
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Most Rated Places
# -----------------------------
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<h3>🏆 Most Rated Tourist Places</h3>', unsafe_allow_html=True)
try:
    top_places = pd.read_sql("""
        SELECT place,
               COUNT(*) AS total_ratings
        FROM ratings
        GROUP BY place
        ORDER BY total_ratings DESC
    """, conn)

    search_top = st.text_input("🔍 Search places", key="search_top", placeholder="Search by place name…")
    if search_top:
        mask = top_places.apply(lambda row: row.astype(str).str.contains(search_top, case=False, na=False).any(), axis=1)
        filtered_top = top_places[mask]
    else:
        filtered_top = top_places

    st.dataframe(filtered_top, use_container_width=True)

    st.download_button(
        "⬇️ Download Top Places CSV",
        data=filtered_top.to_csv(index=False).encode("utf-8"),
        file_name="top_places.csv",
        mime="text/csv",
        key="download_top_places"
    )
except Exception:
    st.warning("No rating data available.")
st.markdown('</div>', unsafe_allow_html=True)

conn.close()

st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────
st.markdown("""
<p class="footer-text">© 2025 Smart Travel Planner · Admin Console</p>
""", unsafe_allow_html=True)