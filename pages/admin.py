import streamlit as st
import pandas as pd
import sqlite3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import apply_styles

st.set_page_config(page_title="...", page_icon="🌍", layout="centered")
apply_styles()   # ← one line does everything
st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Admin Dashboard")
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

# Database Connection
conn = sqlite3.connect("tourist.db")

# -----------------------------
# Registered Users
# -----------------------------
st.subheader("👤 Registered Users")

try:
    users = pd.read_sql(
        "SELECT * FROM users",
        conn
    )
    st.dataframe(users)
except:
    st.warning("No users found.")

# -----------------------------
# Ratings
# -----------------------------
st.subheader("⭐ User Ratings")

try:
    ratings = pd.read_sql(
        "SELECT * FROM ratings",
        conn
    )
    st.dataframe(ratings)
except:
    st.warning("No ratings found.")

# -----------------------------
# Likes
# -----------------------------
st.subheader("❤️ Liked Places")

try:
    likes = pd.read_sql(
        "SELECT * FROM likes",
        conn
    )
    st.dataframe(likes)
except:
    st.warning("No likes found.")

# -----------------------------
# Most Rated Places
# -----------------------------
st.subheader("🏆 Most Rated Tourist Places")

try:
    top_places = pd.read_sql("""
        SELECT place,
               COUNT(*) AS total_ratings
        FROM ratings
        GROUP BY place
        ORDER BY total_ratings DESC
    """, conn)

    st.dataframe(top_places)

except:
    st.warning("No rating data available.")

conn.close()