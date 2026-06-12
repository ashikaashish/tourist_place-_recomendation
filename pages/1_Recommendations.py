import streamlit as st
import pandas as pd
import pickle
import sqlite3
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import apply_styles

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="Tourist Place Recommendation System",
    page_icon="🌍",
    layout="wide"
)
apply_styles()

# ---------------------------------------------------
# CSS — same light theme as admin.py
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

/* Background */
html, body, .stApp {
    background: #f0f4fa !important;
    color: #1f2937 !important;
}
.stApp > * { position: relative; z-index: 2; }

/* Premium Ticker Bar */
.ticker-wrap {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 2000;
    background: #1a1410;
    height: 34px;
    display: flex;
    align-items: center;
    overflow: hidden;
    border-bottom: 1px solid #3b2d20;
}

.ticker-track {
    display: flex;
    white-space: nowrap;
    animation: tickerScroll 30s linear infinite;
}
.ticker-item {
    padding: 0 2rem;
    color: #c9a96e !important;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
}

@keyframes tickerScroll {
    0% {
        transform: translateX(0);
    }
    100% {
        transform: translateX(-50%);
    }
}
.ticker-item {
    padding: 0 2rem;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Prevent global span color from overriding ticker */
.ticker-wrap .ticker-item,
.ticker-wrap .ticker-item * {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}


/* Navbar */
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

/* Navbar home button */
.st-key-navhome div[data-testid="stHorizontalBlock"] {
    position: fixed !important; top: 34px !important;
    right: 2.5rem !important; height: 64px !important;
    z-index: 2000 !important; background: transparent !important;
    display: flex !important; align-items: center !important;
}
.st-key-navhome div[data-testid="stHorizontalBlock"] .stButton > button {
    width: auto !important; height: 38px !important;
    padding: 0 20px !important; font-size: 13px !important;
    font-weight: 700 !important;
    background: #f1f5f9 !important; color: #374151 !important;
    border: 1.5px solid #d1d5db !important;
    border-radius: 10px !important;
    box-shadow: none !important; animation: none !important;
    margin-top: 0 !important;
}
.st-key-navhome div[data-testid="stHorizontalBlock"] .stButton > button:hover {
    background: #e2e8f0 !important; transform: translateY(-1px) !important;
}

/* All text dark */
h1, h2, h3, h4, h5, h6,
p, span, label, div, li,
.stMarkdown, .stMarkdown *,
div[data-testid="stMarkdownContainer"],
div[data-testid="stMarkdownContainer"] * {
    color: #0f172a !important;
    -webkit-text-fill-color: #0f172a !important;
}

/* Selectbox labels */
label[data-testid="stWidgetLabel"],
label[data-testid="stWidgetLabel"] p,
div[data-testid="stTextInput"] label,
div[data-testid="stTextInput"] label p,
.stSelectbox label, .stSelectbox label p {
    color: #0f172a !important;
    -webkit-text-fill-color: #0f172a !important;
    font-weight: 700 !important;
    opacity: 1 !important;
}

/* Selectbox dropdown */
div[data-baseweb="select"] > div {
    background: #ffffff !important;
    color: #0f172a !important;
    border: 1.5px solid #cbd5e1 !important;
    border-radius: 12px !important;
}
div[data-baseweb="select"] > div * {
    color: #0f172a !important;
    -webkit-text-fill-color: #0f172a !important;
}
div[role="option"] {
    background: #ffffff !important;
    color: #0f172a !important;
}
div[role="option"]:hover {
    background: #f1f5f9 !important;
}
div[data-baseweb="popover"],
div[data-baseweb="popover"] ul,
div[data-baseweb="popover"] li,
div[data-baseweb="menu"],
ul[role="listbox"] {
    background: #ffffff !important;
}
div[data-baseweb="popover"] li,
ul[role="listbox"] li,
div[role="option"] *,
ul[role="listbox"] * {
    color: #0f172a !important;
    -webkit-text-fill-color: #0f172a !important;
    background: transparent !important;
}
ul[role="listbox"] li:hover,
div[data-baseweb="popover"] li:hover {
    background: #f1f5f9 !important;
}

/* Number input */
input[type="number"] {
    background: #ffffff !important;
    color: #0f172a !important;
    border: 1.5px solid #cbd5e1 !important;
    border-radius: 10px !important;
    text-align: center;
    font-size: 16px !important;
}

/* Welcome badge */
.welcome-badge {
    display: inline-block;
    background: #dbeafe !important;
    border: 2px solid #3b82f6 !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    font-weight: 800 !important;
    font-size: 15px !important;
    border-radius: 50px !important;
    padding: 8px 20px !important;
    margin-bottom: 16px;
}

/* Main titles */
.main-title {
    text-align: center;
    font-size: 46px;
    font-weight: 800;
    color: #0f172a !important;
    -webkit-text-fill-color: #0f172a !important;
    margin-bottom: 6px;
}
.sub-title {
    text-align: center;
    color: #374151 !important;
    -webkit-text-fill-color: #374151 !important;
    font-size: 17px;
    margin-bottom: 30px;
}

/* Section headers */
.section-header {
    font-size: 24px;
    font-weight: 800;
    color: #0f172a !important;
    -webkit-text-fill-color: #0f172a !important;
    margin: 30px 0 16px 0;
    padding-bottom: 10px;
    border-bottom: 2px solid #e2e8f0;
}

/* Recommendation card */
.rec-card {
    background: rgba(255,255,255,0.92);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.75);
    border-radius: 24px;
    padding: 28px;
    margin-bottom: 28px;
    box-shadow: 0 12px 40px rgba(0,0,0,0.10);
}
.rec-card h2, .rec-card p, .rec-card span, .rec-card b {
    color: #0f172a !important;
    -webkit-text-fill-color: #0f172a !important;
}

/* Rating block */
.rating-block {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 20px 22px;
    margin: 18px 0 14px 0;
}
.rating-label {
    font-size: 13px;
    color: #475569 !important;
    -webkit-text-fill-color: #475569 !important;
    margin-bottom: 12px;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
.star-row { display: flex; align-items: center; gap: 6px; margin-bottom: 14px; }
.star { font-size: 24px; color: #cbd5e1 !important; -webkit-text-fill-color: #cbd5e1 !important; transition: color 0.3s; }
.star.filled { color: #f59e0b !important; -webkit-text-fill-color: #f59e0b !important; }

/* Buttons */
.stButton > button {
    background: #f1f5f9 !important;
    color: #0f172a !important;
    -webkit-text-fill-color: #0f172a !important;
    border: 2px solid #e2e8f0 !important;
    border-radius: 14px !important;
    padding: 12px 20px !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    transition: all 0.25s ease !important;
}
.stButton > button:hover {
    background: #e2e8f0 !important;
    transform: translateY(-2px) !important;
}

/* Get Recommendations main button */
div[data-testid="stButton"]:not([data-testid="stHorizontalBlock"] div[data-testid="stButton"]) button[kind="primary"],
.stButton > button[data-testid="baseButton-secondary"] {
    background: linear-gradient(135deg, #2563eb, #6366f1) !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    border: none !important;
    box-shadow: 0 4px 14px rgba(37,99,235,0.30) !important;
}

/* Submit Rating form button */
.stForm button,
div[data-testid="stForm"] button {
    background: linear-gradient(135deg, #2563eb, #6366f1) !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    border: none !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 12px rgba(37,99,235,0.25) !important;
}

/* Google Maps button */
.btn-maps {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    background: linear-gradient(135deg, #2563eb, #6366f1) !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    border: none;
    border-radius: 12px;
    padding: 13px 0;
    font-size: 15px;
    font-weight: 700;
    cursor: pointer;
    text-decoration: none;
    transition: all 0.3s ease;
    width: 100%;
    text-align: center;
    box-shadow: 0 4px 14px rgba(37,99,235,0.25);
}
.btn-maps:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 22px rgba(37,99,235,0.40);
    color: #ffffff !important;
}

/* Alerts */
div[data-testid="stAlert"] {
    border-radius: 14px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
}
div[data-testid="stAlert"] * {
    color: #0f172a !important;
    font-weight: 700 !important;
}

/* Footer */
.footer {
    text-align: center;
    font-size: 13px;
    color: #64748b !important;
    -webkit-text-fill-color: #64748b !important;
    margin-top: 50px;
    padding-bottom: 30px;
    font-weight: 600;
    letter-spacing: 2px;
}

/* Scrollbar */
::-webkit-scrollbar       { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: #e2e8f0; }
::-webkit-scrollbar-thumb { background: #64748b; border-radius: 5px; }
::-webkit-scrollbar-thumb:hover { background: #475569; }
</style>
""", unsafe_allow_html=True)

# ── Ticker + Navbar ──────────────────────────────────────
st.markdown("""
<div class="ticker-wrap">
  <div class="ticker-track">
    <span class="ticker-item">🌍 Tourist Place Recommendations</span>
    <span class="ticker-item">✈️ Discover Amazing Destinations</span>
    <span class="ticker-item">⭐ Rate Your Favourite Places</span>
    <span class="ticker-item">❤️ Like & Save Places</span>
    <span class="ticker-item">📍 Open in Google Maps</span>
    <span class="ticker-item">🌍 Tourist Place Recommendations</span>
    <span class="ticker-item">✈️ Discover Amazing Destinations</span>
    <span class="ticker-item">⭐ Rate Your Favourite Places</span>
    <span class="ticker-item">❤️ Like & Save Places</span>
    <span class="ticker-item">📍 Open in Google Maps</span>
  </div>
</div>
<div class="navbar-shell"></div>
<div class="nav-brand">🌍 Smart Travel Planner</div>
""", unsafe_allow_html=True)

# ── Navbar home button ───────────────────────────────────
with st.container(key="navhome"):
    col1, col2, col3 = st.columns([10, 1, 1])
    with col3:
        if st.button("🏠 Home", key="nav_home"):
            st.switch_page("welcome.py")

st.markdown('<div class="page-spacer"></div>', unsafe_allow_html=True)

# ---------------------------------------------------
# Paths & DB
# ---------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH  = os.path.join(BASE_DIR, "tourist.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ratings (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            place   TEXT    NOT NULL,
            rating  INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS likes (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            place   TEXT    NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()

init_db()

def get_user_id(username):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE name = ?", (username,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None
    except Exception:
        return None

def save_rating(username, place, rating):
    try:
        user_id = get_user_id(username)
        if user_id is None:
            return False, "User not found in database."
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO ratings (user_id, place, rating) VALUES (?, ?, ?)",
            (user_id, place, rating)
        )
        conn.commit()
        conn.close()
        return True, None
    except Exception as e:
        return False, str(e)

def save_like(username, place):
    try:
        user_id = get_user_id(username)
        if user_id is None:
            return False, "User not found in database."
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM likes WHERE user_id=? AND place=?", (user_id, place))
        if cursor.fetchone():
            conn.close()
            return False, "already_liked"
        cursor.execute("INSERT INTO likes (user_id, place) VALUES (?, ?)", (user_id, place))
        conn.commit()
        conn.close()
        return True, None
    except Exception as e:
        return False, str(e)

# ---------------------------------------------------
# Session check
# ---------------------------------------------------
if "username" not in st.session_state:
    st.warning("Please register from Home Page first.")
    st.stop()

username = st.session_state["username"]

# ---------------------------------------------------
# Load Model
# ---------------------------------------------------
MODEL_PATH = os.path.join(BASE_DIR, "model", "recommendation_model.pkl")
with open(MODEL_PATH, "rb") as file:
    data, similarity = pickle.load(file)

# ---------------------------------------------------
# Recommendation & Crowd Functions
# ---------------------------------------------------
def recommend(place, budget, climate):
    index = data[data["Place"] == place].index[0]
    scores = list(enumerate(similarity[index]))
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    recommended_places = []
    for i in sorted_scores[1:]:
        rp = data.iloc[i[0]]
        if rp["Budget"] == budget and rp["Climate"] == climate:
            recommended_places.append(rp)
        if len(recommended_places) == 3:
            break
    return recommended_places

def predict_crowd(place, month, weekend, holiday):
    high_season = ["April","May","June","October","November","December"]
    score = 0
    if month in high_season: score += 2
    if weekend == "Yes":     score += 1
    if holiday == "Yes":     score += 2
    if place in ["Goa","Manali","Leh","Kerala"]: score += 1
    if score >= 4:   return "🔴 High Crowd"
    elif score >= 2: return "🟡 Medium Crowd"
    else:            return "🟢 Low Crowd"

# ---------------------------------------------------
# Header
# ---------------------------------------------------
st.markdown(f'<div class="welcome-badge">👋 Welcome back, {username}</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">🌍 Tourist Place Recommendation</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Discover Amazing Destinations Using Machine Learning ✈️</div>', unsafe_allow_html=True)

# Hero Banner
st.markdown("""
<div style="max-width:1000px;margin:20px auto 35px auto;
background:url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1400&q=80') center/cover no-repeat;
min-height:280px;border-radius:24px;display:flex;align-items:center;justify-content:center;position:relative;">
    <div style="position:absolute;inset:0;background:rgba(255,255,255,0.22);border-radius:24px;"></div>
    <div style="position:relative;text-align:center;">
        <div style="font-size:64px;">🌍</div>
        <h1 style="color:#111827;font-size:44px;font-weight:800;">Discover Your Next Adventure</h1>
        <p style="color:#374151;font-size:17px;font-weight:600;">AI Powered Tourist Recommendations</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Input Section
# ---------------------------------------------------
st.markdown('<div class="section-header">🔍 Search Your Perfect Destination</div>', unsafe_allow_html=True)

selected_place = st.selectbox("📍 Select Tourist Place", data["Place"].values)

col1, col2 = st.columns(2)
with col1:
    budget = st.selectbox("💰 Select Budget", ["Low", "Medium", "High"])
with col2:
    climate = st.selectbox("🌤 Select Climate", ["Hot", "Cold", "Moderate"])

month   = st.selectbox("📅 Travel Month", [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
])
weekend = st.selectbox("📆 Weekend Trip?", ["Yes", "No"])
holiday = st.selectbox("🎉 Public Holiday?", ["Yes", "No"])

# ---------------------------------------------------
# Recommendation Button
# ---------------------------------------------------
if st.button("🚀 Get Recommendations"):
    st.session_state["recommendations"] = recommend(selected_place, budget, climate)

# ---------------------------------------------------
# Display Recommendations
# ---------------------------------------------------
if "recommendations" in st.session_state:

    st.markdown('<div class="section-header">✨ Recommended Places</div>', unsafe_allow_html=True)

    if len(st.session_state["recommendations"]) == 0:
        st.warning("No matching places found. Try a different budget or climate.")
    else:
        for place in st.session_state["recommendations"]:

            place_name  = place["Place"]
            image_path  = os.path.join(BASE_DIR, "images", place["Image"])
            crowd_level = predict_crowd(place_name, month, weekend, holiday)
            map_url     = place.get("Map", f"https://maps.google.com/?q={place_name},India")

            st.markdown('<div class="rec-card">', unsafe_allow_html=True)

            col1, col2 = st.columns([1, 2])
            with col1:
                try:
                    st.image(image_path, use_container_width=True)
                except:
                    st.warning("Image not found.")
            with col2:
                st.markdown(f"""
                    <h2 style="color:#0f172a;-webkit-text-fill-color:#0f172a;font-size:28px;font-weight:800;margin-bottom:14px;">
                        📍 {place_name}
                    </h2>
                    <p style="color:#374151;font-size:16px;line-height:2.4;-webkit-text-fill-color:#374151;">
                        ⭐ <b style="color:#0f172a;">Rating:</b> <span style="color:#374151;">{place['Rating']}</span><br>
                        🌤 <b style="color:#0f172a;">Climate:</b> <span style="color:#374151;">{place['Climate']}</span><br>
                        💰 <b style="color:#0f172a;">Budget:</b> <span style="color:#374151;">{place['Budget']}</span><br>
                        👥 <b style="color:#0f172a;">Crowd:</b> <span style="color:#374151;">{crowd_level}</span>
                    </p>
                """, unsafe_allow_html=True)

            # Rating Block
            st.markdown('<div class="rating-block">', unsafe_allow_html=True)
            st.markdown(f'<p class="rating-label">⭐ Rate {place_name}</p>', unsafe_allow_html=True)

            prev_val = st.session_state.get(f"prev_rating_{place_name}", 0)

            rcol1, rcol2 = st.columns([1, 3])
            with rcol1:
                user_rating = st.number_input(
                    "Rating",
                    min_value=1, max_value=5, value=prev_val or 3, step=1,
                    key=f"rating_{place_name}",
                    label_visibility="collapsed"
                )
            with rcol2:
                st.markdown(
                    '<p style="color:#475569;font-size:14px;padding-top:8px;-webkit-text-fill-color:#475569;">out of 5</p>',
                    unsafe_allow_html=True
                )

            stars_html = "".join([
                f'<span class="star {"filled" if i <= user_rating else ""}">★</span>'
                for i in range(1, 6)
            ])
            st.markdown(f'<div class="star-row">{stars_html}</div>', unsafe_allow_html=True)

            with st.form(key=f"form_{place_name}"):
                submit_rating = st.form_submit_button(f"⭐ Submit Rating for {place_name}")

            if submit_rating:
                success, err = save_rating(username, place_name, int(user_rating))
                if success:
                    st.session_state[f"prev_rating_{place_name}"] = int(user_rating)
                    st.success(f"✅ Rating {user_rating}/5 saved for {place_name}!")
                else:
                    st.error(f"Database Error: {err}")

            st.markdown('</div>', unsafe_allow_html=True)  # close rating-block

            # Like + Maps Row
            lcol, mcol = st.columns(2)
            with lcol:
                if st.button(f"♡  Like {place_name}", key=f"like_{place_name}"):
                    success, err = save_like(username, place_name)
                    if success:
                        st.success(f"❤️ {place_name} liked!")
                    elif err == "already_liked":
                        st.info(f"You already liked {place_name}.")
                    else:
                        st.error(f"Error: {err}")
            with mcol:
                st.markdown(f"""
                    <a href="{map_url}" target="_blank" class="btn-maps">
                        📍&nbsp; Open in Google Maps
                    </a>
                """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)  # close rec-card

# ---------------------------------------------------
# Footer
# ---------------------------------------------------
st.markdown("---")
st.markdown('<div class="footer">✈️ &nbsp; EXPLORE &nbsp;•&nbsp; DISCOVER &nbsp;•&nbsp; TRAVEL &nbsp; ✈️</div>', unsafe_allow_html=True)