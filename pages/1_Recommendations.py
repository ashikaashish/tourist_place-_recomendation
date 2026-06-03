import streamlit as st
import pandas as pd
import pickle
import sqlite3
import os
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import apply_styles

st.set_page_config(page_title="...", page_icon="🌍", layout="centered")
apply_styles()   # ← one line does everything
# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="Tourist Place Recommendation System",
    page_icon="🌍",
    layout="wide"
)
st.markdown('</div>', unsafe_allow_html=True)
# Back button
if st.button("← Back to Home"):
    st.switch_page("welcome.py")
st.markdown("""
<style>
[data-testid="stSidebar"]        { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Paths
# ---------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH  = os.path.join(BASE_DIR, "tourist.db")

# ---------------------------------------------------
# Database Initialization
# ---------------------------------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            place TEXT,
            rating INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS likes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            place TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------------------------------------------------
# DB Helper Functions
# ---------------------------------------------------
def save_rating(username, place, rating):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO ratings (username, place, rating) VALUES (?, ?, ?)",
            (username, place, rating)
        )
        conn.commit()
        conn.close()
        return True, None
    except Exception as e:
        return False, str(e)

def save_like(username, place):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM likes WHERE username=? AND place=?",
            (username, place)
        )
        if cursor.fetchone():
            conn.close()
            return False, "already_liked"
        cursor.execute(
            "INSERT INTO likes (username, place) VALUES (?, ?)",
            (username, place)
        )
        conn.commit()
        conn.close()
        return True, None
    except Exception as e:
        return False, str(e)

# ---------------------------------------------------
# Session State Check
# ---------------------------------------------------
if "username" not in st.session_state:
    st.warning("Please register from Home Page first.")
    st.stop()

username = st.session_state["username"]

# ---------------------------------------------------
# Animated CSS
# ---------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

* { font-family: 'Poppins', sans-serif; }

/* ── Animated gradient background ── */
.stApp {
    background: linear-gradient(-45deg, #0f0c29, #302b63, #1a1a2e, #16213e, #0f3460);
    background-size: 400% 400%;
    animation: gradientShift 12s ease infinite;
}

@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ── Floating particles overlay ── */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-image:
        radial-gradient(circle at 20% 20%, rgba(99,102,241,0.15) 0%, transparent 50%),
        radial-gradient(circle at 80% 80%, rgba(236,72,153,0.15) 0%, transparent 50%),
        radial-gradient(circle at 50% 50%, rgba(6,182,212,0.08) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
}

html, body, [class*="css"] { color: #e2e8f0; }

/* ── Title animation ── */
.main-title {
    text-align: center;
    font-size: 52px;
    font-weight: 700;
    background: linear-gradient(135deg, #667eea, #f093fb, #4facfe, #00f2fe);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: titleGradient 5s ease infinite, fadeSlideDown 0.8s ease both;
    margin-bottom: 6px;
}

@keyframes titleGradient {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes fadeSlideDown {
    from { opacity: 0; transform: translateY(-30px); }
    to   { opacity: 1; transform: translateY(0); }
}

.sub-title {
    text-align: center;
    font-size: 17px;
    color: #94a3b8;
    margin-bottom: 40px;
    animation: fadeSlideDown 0.8s ease 0.2s both;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e1b4b 0%, #312e81 50%, #1e1b4b 100%);
    border-right: 1px solid rgba(99,102,241,0.3);
}
section[data-testid="stSidebar"] * { color: #c7d2fe !important; }
section[data-testid="stSidebar"] .stSuccess {
    background: rgba(99,102,241,0.2) !important;
    border: 1px solid rgba(99,102,241,0.4) !important;
    border-radius: 10px !important;
}

/* ── Buttons ── */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, rgba(99,102,241,0.2), rgba(168,85,247,0.2));
    color: #e2e8f0 !important;
    border: 1px solid rgba(99,102,241,0.5);
    border-radius: 12px;
    padding: 12px 20px;
    font-size: 15px;
    font-weight: 500;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
    position: relative;
    overflow: hidden;
}
.stButton > button::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 100%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    transition: left 0.5s ease;
}
.stButton > button:hover::before { left: 100%; }
.stButton > button:hover {
    background: linear-gradient(135deg, rgba(99,102,241,0.5), rgba(168,85,247,0.5));
    border-color: rgba(167,139,250,0.8);
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(99,102,241,0.4);
}

/* ── Get Recommendations button ── */
div[data-testid="stButton"]:has(button[kind="primary"]) > button,
.get-rec .stButton > button {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    border: none !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 20px rgba(102,126,234,0.5) !important;
}

/* ── Selectboxes ── */
div[data-baseweb="select"] > div {
    background: rgba(30,27,75,0.8) !important;
    color: #e2e8f0 !important;
    border: 1px solid rgba(99,102,241,0.4) !important;
    border-radius: 12px !important;
    backdrop-filter: blur(10px);
    transition: border-color 0.3s;
}
div[data-baseweb="select"] > div:hover {
    border-color: rgba(167,139,250,0.8) !important;
}
div[role="option"] {
    background: #1e1b4b !important;
    color: #e2e8f0 !important;
}
div[role="option"]:hover {
    background: rgba(99,102,241,0.3) !important;
}

/* ── Number input ── */
input[type="number"] {
    background: rgba(30,27,75,0.8) !important;
    color: #ffffff !important;
    border: 1.5px solid rgba(99,102,241,0.5) !important;
    border-radius: 10px !important;
    text-align: center;
    font-size: 16px !important;
    transition: border-color 0.3s, box-shadow 0.3s;
}
input[type="number"]:focus {
    border-color: #a78bfa !important;
    box-shadow: 0 0 0 3px rgba(167,139,250,0.2) !important;
}

/* ── Recommendation card ── */
.rec-card {
    background: rgba(15,12,41,0.7);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 24px;
    padding: 28px;
    margin-bottom: 32px;
    backdrop-filter: blur(20px);
    animation: cardFadeIn 0.6s ease both;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    box-shadow: 0 4px 30px rgba(0,0,0,0.3);
    position: relative;
    overflow: hidden;
}
.rec-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #667eea, #f093fb, #4facfe);
    border-radius: 24px 24px 0 0;
}

@keyframes cardFadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── Rating block ── */
.rating-block {
    background: rgba(30,27,75,0.6);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 16px;
    padding: 20px 22px;
    margin: 18px 0 14px 0;
    backdrop-filter: blur(10px);
}
.rating-label {
    font-size: 13px;
    color: #94a3b8;
    margin-bottom: 12px;
    font-weight: 500;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* ── Stars ── */
.star-row {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 14px;
}
.star {
    font-size: 24px;
    color: rgba(99,102,241,0.3);
    transition: color 0.3s, transform 0.2s;
}
.star.filled {
    color: #fbbf24;
    text-shadow: 0 0 10px rgba(251,191,36,0.5);
    animation: starPop 0.4s ease;
}
@keyframes starPop {
    0%   { transform: scale(1); }
    50%  { transform: scale(1.4); }
    100% { transform: scale(1); }
}

/* ── Maps link button ── */
.btn-maps {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    background: linear-gradient(135deg, rgba(6,182,212,0.2), rgba(59,130,246,0.2));
    color: #67e8f9 !important;
    border: 1px solid rgba(6,182,212,0.4);
    border-radius: 12px;
    padding: 13px 0;
    font-size: 15px;
    font-weight: 500;
    cursor: pointer;
    text-decoration: none;
    transition: all 0.3s ease;
    width: 100%;
    text-align: center;
    backdrop-filter: blur(10px);
}
.btn-maps:hover {
    background: linear-gradient(135deg, rgba(6,182,212,0.4), rgba(59,130,246,0.4));
    border-color: rgba(103,232,249,0.7);
    box-shadow: 0 4px 20px rgba(6,182,212,0.3);
    transform: translateY(-2px);
    color: #ffffff !important;
}

/* ── Section headings ── */
h1, h2, h3 {
    color: #e2e8f0 !important;
}

/* ── Welcome text ── */
.welcome-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(99,102,241,0.2), rgba(168,85,247,0.2));
    border: 1px solid rgba(99,102,241,0.4);
    border-radius: 50px;
    padding: 6px 18px;
    font-size: 14px;
    color: #c4b5fd;
    margin-bottom: 20px;
    animation: fadeSlideDown 0.6s ease both;
}

/* ── Footer ── */
.footer {
    text-align: center;
    font-size: 15px;
    margin-top: 50px;
    padding-bottom: 30px;
    background: linear-gradient(135deg, #667eea, #f093fb, #4facfe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 600;
    letter-spacing: 2px;
}

/* ── Pulse animation for get-rec button ── */
@keyframes pulse {
    0%, 100% { box-shadow: 0 4px 20px rgba(102,126,234,0.4); }
    50%       { box-shadow: 0 4px 40px rgba(102,126,234,0.8); }
}

/* ── Info/success/warning messages ── */
div[data-testid="stAlert"] {
    background: rgba(30,27,75,0.8) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(99,102,241,0.3) !important;
    backdrop-filter: blur(10px);
}

/* ── Section header style ── */
.section-header {
    font-size: 26px;
    font-weight: 600;
    background: linear-gradient(135deg, #a78bfa, #67e8f9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 30px 0 20px 0;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0f0c29; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(#667eea, #764ba2);
    border-radius: 3px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Load Model
# ---------------------------------------------------
MODEL_PATH = os.path.join(BASE_DIR, "model", "recommendation_model.pkl")
with open(MODEL_PATH, "rb") as file:
    data, similarity = pickle.load(file)

# ---------------------------------------------------
# Recommendation Function
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

# ---------------------------------------------------
# Crowd Prediction
# ---------------------------------------------------
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

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------
st.sidebar.title("🌴 Popular Destinations")
for p in ["Goa", "Kerala", "Manali", "Leh"]:
    st.sidebar.success(p)
st.sidebar.markdown("---")
st.sidebar.info("Select your preferred destination, budget and climate to get recommendations.")

# ---------------------------------------------------
# Input Section
# ---------------------------------------------------
st.markdown('<div class="section-header">🔍 Search Your Perfect Destination</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    selected_place = st.selectbox("📍 Select Tourist Place", data["Place"].values)
with col2:
    budget = st.selectbox("💰 Select Budget", ["Low", "Medium", "High"])

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

            place_name = place["Place"]
            image_path = os.path.join(BASE_DIR, "images", place["Image"])
            crowd_level = predict_crowd(place_name, month, weekend, holiday)
            map_url = place.get("Map", f"https://maps.google.com/?q={place_name},India")

            # ── Card open ──
            st.markdown('<div class="rec-card">', unsafe_allow_html=True)

            # ── Image + Info ──
            col1, col2 = st.columns([1, 2])
            with col1:
                try:
                    st.image(image_path, use_container_width=True)
                except:
                    st.warning("Image not found.")
            with col2:
                st.markdown(f"""
                    <h2 style="
                        background: linear-gradient(135deg, #a78bfa, #67e8f9);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        background-clip: text;
                        font-size: 28px;
                        font-weight: 700;
                        margin-bottom: 14px;">
                        📍 {place_name}
                    </h2>
                    <p style="color:#cbd5e1; font-size:16px; line-height:2.4;">
                        ⭐ <b style="color:#fbbf24;">Rating:</b> <span style="color:#fef3c7;">{place['Rating']}</span><br>
                        🌤 <b style="color:#67e8f9;">Climate:</b> <span style="color:#e0f2fe;">{place['Climate']}</span><br>
                        💰 <b style="color:#86efac;">Budget:</b> <span style="color:#dcfce7;">{place['Budget']}</span><br>
                        👥 <b style="color:#c4b5fd;">Crowd:</b> <span style="color:#ede9fe;">{crowd_level}</span>
                    </p>
                """, unsafe_allow_html=True)

            # ── Rating Block ──
            st.markdown('<div class="rating-block">', unsafe_allow_html=True)
            st.markdown(f'<p class="rating-label">⭐ Rate {place_name}</p>', unsafe_allow_html=True)

            prev_val = st.session_state.get(f"prev_rating_{place_name}", 0)
            stars_html = "".join([
                f'<span class="star {"filled" if i <= prev_val else ""}">★</span>'
                for i in range(1, 6)
            ])
            st.markdown(f'<div class="star-row">{stars_html}</div>', unsafe_allow_html=True)

            with st.form(key=f"form_{place_name}"):
                rcol1, rcol2 = st.columns([1, 3])
                with rcol1:
                    user_rating = st.number_input(
                        "Rating",
                        min_value=1,
                        max_value=5,
                        value=3,
                        step=1,
                        key=f"rating_{place_name}",
                        label_visibility="collapsed"
                    )
                with rcol2:
                    st.markdown(
                        '<p style="color:#94a3b8; font-size:14px; padding-top:8px;">out of 5</p>',
                        unsafe_allow_html=True
                    )
                submit_rating = st.form_submit_button(f"☆  Submit Rating for {place_name}")

            if submit_rating:
                success, err = save_rating(username, place_name, int(user_rating))
                if success:
                    st.session_state[f"prev_rating_{place_name}"] = int(user_rating)
                    st.success(f"✅ Rating {user_rating}/5 saved for {place_name}!")
                else:
                    st.error(f"Database Error: {err}")

            st.markdown('</div>', unsafe_allow_html=True)  # close rating-block

            # ── Like + Maps Row ──
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
                        ⊙&nbsp; Open in Google Maps
                    </a>
                """, unsafe_allow_html=True)

            # ── Card close ──
            st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# Footer
# ---------------------------------------------------
st.markdown("---")
st.markdown('<div class="footer">✈️ &nbsp; EXPLORE &nbsp;•&nbsp; DISCOVER &nbsp;•&nbsp; TRAVEL &nbsp; ✈️</div>', unsafe_allow_html=True)