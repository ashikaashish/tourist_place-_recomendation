import streamlit as st
import pandas as pd
import pickle
import sqlite3
import os

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="Tourist Place Recommendation System",
    page_icon="🌍",
    layout="wide"
)

# ---------------------------------------------------
# Use absolute path for DB so it always saves correctly
# ---------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "tourist.db")

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
        existing = cursor.fetchone()
        if existing:
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
st.write("Current User:", username)
st.write("Database:", DB_PATH)
st.write(f"👋 Welcome {username}")

if st.button("📊 Admin Dashboard"):
    st.switch_page("pages/admin.py")

# ---------------------------------------------------
# Custom CSS
# ---------------------------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #e3f2fd, #ffffff);
}
html, body, [class*="css"] { color: black; }
.main-title {
    text-align: center;
    font-size: 55px;
    font-weight: bold;
    color: #0E76A8;
}
.sub-title {
    text-align: center;
    font-size: 20px;
    color: #444444;
    margin-bottom: 30px;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(to bottom, #0E76A8, #053B50);
}
section[data-testid="stSidebar"] * { color: white !important; }
.stButton button {
    width: 100%;
    background: linear-gradient(to right, #00b4db, #0083b0);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px;
    font-size: 18px;
    font-weight: bold;
}
.stButton button:hover {
    background: linear-gradient(to right, #0083b0, #00b4db);
    color: white;
}
.recommend-card {
    background: white !important;
    color: black !important;
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 25px;
    box-shadow: 0px 5px 20px rgba(0,0,0,0.15);
}
.recommend-card * { color: black !important; opacity: 1 !important; }
h1, h2, h3, h4, h5, h6 { color: #0E76A8 !important; }
div[data-baseweb="select"] > div {
    background: white !important;
    color: black !important;
    border: 1px solid #d3d3d3 !important;
}
div[role="option"] { background: white !important; color: black !important; }
div[role="option"]:hover { background: #f0f2f6 !important; }
.footer {
    text-align: center;
    color: #0E76A8;
    font-size: 22px;
    font-weight: bold;
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
        recommended_place = data.iloc[i[0]]
        if (recommended_place["Budget"] == budget and
                recommended_place["Climate"] == climate):
            recommended_places.append(recommended_place)
        if len(recommended_places) == 3:
            break
    return recommended_places

# ---------------------------------------------------
# Crowd Prediction Function
# ---------------------------------------------------
def predict_crowd(place, month, weekend, holiday):
    high_season = ["April", "May", "June", "October", "November", "December"]
    score = 0
    if month in high_season:
        score += 2
    if weekend == "Yes":
        score += 1
    if holiday == "Yes":
        score += 2
    if place in ["Goa", "Manali", "Leh", "Kerala"]:
        score += 1
    if score >= 4:
        return "🔴 High Crowd"
    elif score >= 2:
        return "🟡 Medium Crowd"
    else:
        return "🟢 Low Crowd"

# ---------------------------------------------------
# Header
# ---------------------------------------------------
st.markdown('<div class="main-title">🌍 Tourist Place Recommendation System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Discover Amazing Destinations Using Machine Learning ✈️</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------
st.sidebar.title("🌴 Popular Destinations")
for place in ["Goa", "Kerala", "Manali", "Leh"]:
    st.sidebar.success(place)
st.sidebar.markdown("---")
st.sidebar.info("Select your preferred destination, budget and climate to get recommendations.")

# ---------------------------------------------------
# Input Section
# ---------------------------------------------------
st.markdown("## 🔍 Search Your Perfect Destination")

col1, col2 = st.columns(2)
with col1:
    selected_place = st.selectbox("📍 Select Tourist Place", data["Place"].values)
with col2:
    budget = st.selectbox("💰 Select Budget", ["Low", "Medium", "High"])

climate = st.selectbox("🌤 Select Climate", ["Hot", "Cold", "Moderate"])
month = st.selectbox("📅 Travel Month", [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
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

    st.header("✨ Recommended Places")

    if len(st.session_state["recommendations"]) == 0:
        st.warning("No matching places found. Try a different budget or climate.")

    else:
        for place in st.session_state["recommendations"]:

            place_name = place["Place"]
            image_path = os.path.join(BASE_DIR, "images", place["Image"])
            crowd_level = predict_crowd(place_name, month, weekend, holiday)

            # Initialize like state for this place
            like_key = f"liked_{place_name}"
            if like_key not in st.session_state:
                st.session_state[like_key] = False

            st.markdown('<div class="recommend-card">', unsafe_allow_html=True)

            # --- Image + Info ---
            col1, col2 = st.columns([1, 2])

            with col1:
                try:
                    st.image(image_path, use_container_width=True)
                except:
                    st.warning("Image not found.")

            with col2:
                st.markdown(f"""
                    <h2 style="color:#0E76A8;">📍 {place_name}</h2>
                    <p style="color:#000000; font-size:18px; font-weight:500;">
                        ⭐ <b>Rating:</b> {place['Rating']}<br><br>
                        🌤 <b>Climate:</b> {place['Climate']}<br><br>
                        💰 <b>Budget:</b> {place['Budget']}<br><br>
                        👥 <b>Crowd Prediction:</b> {crowd_level}
                    </p>
                """, unsafe_allow_html=True)

            st.markdown("---")

            # --- Rating Form ---
            with st.form(key=f"form_{place_name}"):
                user_rating = st.number_input(
                    f"⭐ Rate {place_name} (Enter 1 to 5)",
                    min_value=1,
                    max_value=5,
                    value=3,
                    step=1,
                    key=f"rating_{place_name}"
                )
                submit_rating = st.form_submit_button(f"Submit Rating for {place_name}")

            if submit_rating:
                success, err = save_rating(username, place_name, user_rating)
                if success:
                    st.success(f"✅ Rating {user_rating}/5 saved for {place_name}")
                else:
                    st.error(f"Database Error: {err}")

            # --- Like Button ---
            if st.button(f"❤️ Like {place_name}", key=f"like_{place_name}"):
                success, err = save_like(username, place_name)
                if success:
                    st.success(f"❤️ {place_name} liked successfully!")
                elif err == "already_liked":
                    st.info(f"You have already liked {place_name}!")
                else:
                    st.error(f"Database Error: {err}")

            # --- Google Maps ---
            st.markdown(f"""
                <a href="{place['Map']}" target="_blank">
                    <button style="background:#0E76A8; color:white; border:none;
                    padding:12px 20px; border-radius:10px; font-size:16px;
                    cursor:pointer; margin-top:10px;">
                    📍 Open in Google Maps
                    </button>
                </a>
            """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# DEBUG: Check Ratings Table
# ---------------------------------------------------
if st.button("Show Ratings Table"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ratings")
    st.write(cursor.fetchall())
    conn.close()

# ---------------------------------------------------
# Footer
# ---------------------------------------------------
st.markdown("---")
st.markdown('<div class="footer">✈️ Explore • Discover • Travel</div>', unsafe_allow_html=True)