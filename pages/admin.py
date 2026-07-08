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
# CSS — sidebar + KPI card + bar-chart theme
# ---------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800;900&display=swap');

* { font-family: 'Poppins', sans-serif; font-weight: 600; box-sizing: border-box; margin: 0; padding: 0; }

/* Hide Streamlit chrome */
header, [data-testid="stHeader"], [data-testid="stToolbar"],
[data-testid="stDecoration"], #MainMenu, footer,
[data-testid="collapsedControl"] {
    display: none !important;
}
.block-container { padding: 0 !important; max-width: 100% !important; }

html, body, .stApp {
    background: #f0f4fa !important;
}

/* ── Custom dark icon sidebar (replaces Streamlit's native sidebar) ── */
[data-testid="stSidebar"] {
    background: #15192b !important;
    width: 76px !important;
    min-width: 76px !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.18);
}
[data-testid="stSidebar"] > div {
    padding-top: 28px !important;
}
[data-testid="stSidebarNav"] { display: none !important; }

.sb-logo {
    width: 40px; height: 40px; border-radius: 12px;
    background: linear-gradient(135deg, #6366f1, #818cf8);
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; margin: 0 auto 28px;
}
.sb-icon {
    width: 44px; height: 44px; border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 19px; margin: 0 auto 14px;
    color: #6b7280; background: transparent;
    transition: all 0.2s ease; cursor: pointer;
}
.sb-icon.active {
    background: rgba(99,102,241,0.18);
    color: #818cf8;
    box-shadow: inset 0 0 0 1.5px rgba(129,140,248,0.4);
}

/* ── Top bar ── */
.topbar {
    background: #ffffff; border-bottom: 1px solid #e5e9f2;
    padding: 18px 32px; display: flex; align-items: center;
    justify-content: space-between;
}
.topbar-title { font-size: 19px; font-weight: 800; color: #0f172a; }
.topbar-sub { font-size: 12px; font-weight: 500; color: #94a3b8; margin-top: 2px; }

/* Home button placed top-right via Streamlit columns */
div[data-testid="stHorizontalBlock"] {
    padding: 14px 32px 0 0 !important;
}
div[data-testid="stHorizontalBlock"] .stButton > button {
    width: auto !important; height: 36px !important;
    padding: 0 18px !important; font-size: 12px !important;
    font-weight: 700 !important;
    background: #f1f5f9 !important; color: #374151 !important;
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 10px !important;
    box-shadow: none !important;
}
div[data-testid="stHorizontalBlock"] .stButton > button:hover {
    background: #e2e8f0 !important; transform: translateY(-1px) !important;
}

/* ── Page padding wrapper ── */
.dash-wrap { padding: 24px 32px 50px; }

/* ── KPI cards row ── */
.kpi-card {
    background: #ffffff; border-radius: 16px; padding: 20px 22px;
    box-shadow: 0 4px 18px rgba(15,23,42,0.06);
    border: 1px solid #eef1f7;
    height: 100%;
}
.kpi-icon {
    width: 34px; height: 34px; border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 15px; margin-bottom: 14px;
}
.kpi-icon.blue   { background: #e0e9ff; }
.kpi-icon.yellow { background: #fff3d6; }
.kpi-icon.pink   { background: #ffe3e9; }
.kpi-icon.green  { background: #d9f7e8; }

.kpi-label { font-size: 12px; color: #64748b; font-weight: 600; margin-bottom: 6px; }
.kpi-value { font-size: 26px; color: #0f172a; font-weight: 800; line-height: 1.1; }
.kpi-delta { font-size: 11.5px; color: #94a3b8; font-weight: 600; margin-top: 4px; }

.kpi-bar-track {
    width: 100%; height: 6px; border-radius: 4px;
    background: #eef1f7; margin-top: 14px; overflow: hidden;
}
.kpi-bar-fill { height: 100%; border-radius: 4px; }
.kpi-bar-fill.blue   { background: #4f6df5; }
.kpi-bar-fill.yellow { background: #f4b740; }
.kpi-bar-fill.pink   { background: #f15b7e; }
.kpi-bar-fill.green  { background: #22c08e; }

/* ── Top destinations bar chart card ── */
.dest-card {
    background: #ffffff; border-radius: 16px; padding: 22px 24px;
    box-shadow: 0 4px 18px rgba(15,23,42,0.06);
    border: 1px solid #eef1f7; margin-bottom: 26px;
}
.dest-title { font-size: 14px; font-weight: 800; color: #0f172a; margin-bottom: 16px; }
.dest-row { display: flex; align-items: center; margin-bottom: 12px; }
.dest-name { width: 70px; font-size: 12.5px; color: #475569; font-weight: 700; }
.dest-track { flex: 1; height: 9px; background: #eef1f7; border-radius: 5px; overflow: hidden; margin-right: 10px; }
.dest-fill { height: 100%; border-radius: 5px; }
.dest-count { width: 34px; font-size: 12px; color: #94a3b8; font-weight: 700; text-align: right; }

/* ── Section cards (data tables) ── */
.section-card {
    background: #ffffff;
    border: 1px solid #eef1f7;
    border-radius: 16px;
    padding: 22px 24px;
    margin-bottom: 24px;
    box-shadow: 0 4px 18px rgba(15,23,42,0.06);
}
.section-card h3, div[data-testid="stMarkdownContainer"] h3 {
    font-size: 16px !important;
    font-weight: 800 !important;
    color: #0f172a !important;
    margin-bottom: 14px !important;
    padding-bottom: 10px !important;
    border-bottom: 1px solid #eef1f7 !important;
}

.section-card .stTextInput label, label[data-testid="stWidgetLabel"] {
    color: #475569 !important; font-weight: 600 !important; font-size: 12.5px !important;
}

.section-card .stDownloadButton > button {
    background: linear-gradient(135deg, #4f6df5 0%, #6366f1 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 9px 18px !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
    box-shadow: 0 4px 14px rgba(79,109,245,0.28) !important;
    margin-top: 8px !important;
    transition: all 0.25s ease !important;
}
.section-card .stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(79,109,245,0.38) !important;
}

[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid #eef1f7 !important;
}

div[data-testid="stAlert"] {
    border-radius: 12px !important; font-size: 13px !important; font-weight: 600 !important;
}

.footer-text {
    text-align: center; font-size: 12px;
    color: #94a3b8; margin-top: 10px;
    font-weight: 500; letter-spacing: 0.04em;
}

::-webkit-scrollbar       { width: 6px; }
::-webkit-scrollbar-track { background: #f1f5f9; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Database Connection
# ---------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH  = os.path.join(BASE_DIR, "tourist.db")
conn = sqlite3.connect(DB_PATH)

def safe_read(query):
    try:
        return pd.read_sql(query, conn)
    except Exception:
        return pd.DataFrame()

users_df   = safe_read("SELECT * FROM users")
ratings_df = safe_read("SELECT * FROM ratings")
likes_df   = safe_read("SELECT * FROM likes")
top_places_df = safe_read("""
    SELECT place, COUNT(*) AS total_ratings
    FROM ratings GROUP BY place ORDER BY total_ratings DESC
""")

n_users   = len(users_df)
n_ratings = len(ratings_df)
n_likes   = len(likes_df)
avg_rating = round(ratings_df["rating"].mean(), 1) if "rating" in ratings_df.columns and not ratings_df.empty else 0
top_place_name  = top_places_df.iloc[0]["place"] if not top_places_df.empty else "—"
top_place_count = int(top_places_df.iloc[0]["total_ratings"]) if not top_places_df.empty else 0
n_destinations  = top_places_df["place"].nunique() if not top_places_df.empty else 0

# ---------------------------------------------------
# Sidebar (dark icon rail)
# ---------------------------------------------------
with st.sidebar:
    st.markdown(
        '<div class="sb-logo">🌍</div>'
        '<div class="sb-icon active" title="Dashboard">📊</div>'
        '<div class="sb-icon" title="Users">👤</div>'
        '<div class="sb-icon" title="Ratings">⭐</div>'
        '<div class="sb-icon" title="Likes">❤️</div>'
        '<div class="sb-icon" title="Export">⬇️</div>',
        unsafe_allow_html=True
    )

# ---------------------------------------------------
# Top bar
# ---------------------------------------------------
top_l, top_r = st.columns([10, 1.4])
with top_l:
    st.markdown(
        '<div class="topbar">'
        '<div>'
        '<div class="topbar-title">📊 Admin Dashboard</div>'
        '<div class="topbar-sub">Overview of users, ratings, likes and top destinations</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )
with top_r:
    if st.button("🏠 Home", key="nav_home"):
        st.switch_page("welcome.py")

st.markdown('<div class="dash-wrap">', unsafe_allow_html=True)

# ---------------------------------------------------
# KPI Cards row
# ---------------------------------------------------
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(
        '<div class="kpi-card">'
        '<div class="kpi-icon blue">👤</div>'
        '<div class="kpi-label">Registered users</div>'
        f'<div class="kpi-value">{n_users:,}</div>'
        '<div class="kpi-delta">All-time signups</div>'
        '<div class="kpi-bar-track"><div class="kpi-bar-fill blue" style="width:78%;"></div></div>'
        '</div>',
        unsafe_allow_html=True
    )
with k2:
    st.markdown(
        '<div class="kpi-card">'
        '<div class="kpi-icon yellow">⭐</div>'
        '<div class="kpi-label">User ratings</div>'
        f'<div class="kpi-value">{n_ratings:,}</div>'
        f'<div class="kpi-delta">Avg {avg_rating} stars</div>'
        '<div class="kpi-bar-track"><div class="kpi-bar-fill yellow" style="width:64%;"></div></div>'
        '</div>',
        unsafe_allow_html=True
    )
with k3:
    st.markdown(
        '<div class="kpi-card">'
        '<div class="kpi-icon pink">❤️</div>'
        '<div class="kpi-label">Liked places</div>'
        f'<div class="kpi-value">{n_likes:,}</div>'
        f'<div class="kpi-delta">{n_destinations} destinations</div>'
        '<div class="kpi-bar-track"><div class="kpi-bar-fill pink" style="width:55%;"></div></div>'
        '</div>',
        unsafe_allow_html=True
    )
with k4:
    st.markdown(
        '<div class="kpi-card">'
        '<div class="kpi-icon green">🏆</div>'
        '<div class="kpi-label">Top place</div>'
        f'<div class="kpi-value">{top_place_name}</div>'
        f'<div class="kpi-delta">{top_place_count} ratings</div>'
        '<div class="kpi-bar-track"><div class="kpi-bar-fill green" style="width:88%;"></div></div>'
        '</div>',
        unsafe_allow_html=True
    )

st.write("")

# ---------------------------------------------------
# Top Destinations bar chart card
# ---------------------------------------------------
dest_colors = ["#4f6df5", "#22c08e", "#f4b740", "#a78bfa", "#f15b7e", "#38bdf8"]
row_chunks = []
if not top_places_df.empty:
    max_count = int(top_places_df["total_ratings"].max())
    for i, row in top_places_df.head(6).iterrows():
        pct = max(8, int((row["total_ratings"] / max_count) * 100))
        color = dest_colors[i % len(dest_colors)]
        row_chunks.append(
            '<div class="dest-row">'
            f'<div class="dest-name">{row["place"]}</div>'
            f'<div class="dest-track"><div class="dest-fill" style="width:{pct}%;background:{color};"></div></div>'
            f'<div class="dest-count">{int(row["total_ratings"])}</div>'
            '</div>'
        )
    rows_html = "".join(row_chunks)
else:
    rows_html = '<div style="color:#94a3b8;font-size:13px;">No rating data available.</div>'

dest_card_html = (
    '<div class="dest-card">'
    '<div class="dest-title">🏆 Top Destinations</div>'
    f'{rows_html}'
    '</div>'
)
st.markdown(dest_card_html, unsafe_allow_html=True)

# -----------------------------
# Registered Users
# -----------------------------
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<h3>👤 Registered Users</h3>', unsafe_allow_html=True)
if not users_df.empty:
    search_users = st.text_input("🔍 Search users", key="search_users", placeholder="Search by any field…")
    if search_users:
        mask = users_df.apply(lambda row: row.astype(str).str.contains(search_users, case=False, na=False).any(), axis=1)
        filtered_users = users_df[mask]
    else:
        filtered_users = users_df

    st.dataframe(filtered_users, use_container_width=True)

    st.download_button(
        "⬇️ Download Users CSV",
        data=filtered_users.to_csv(index=False).encode("utf-8"),
        file_name="users.csv",
        mime="text/csv",
        key="download_users"
    )
else:
    st.warning("No users found.")
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Ratings
# -----------------------------
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<h3>⭐ User Ratings</h3>', unsafe_allow_html=True)
if not ratings_df.empty:
    search_ratings = st.text_input("🔍 Search ratings", key="search_ratings", placeholder="Search by any field…")
    if search_ratings:
        mask = ratings_df.apply(lambda row: row.astype(str).str.contains(search_ratings, case=False, na=False).any(), axis=1)
        filtered_ratings = ratings_df[mask]
    else:
        filtered_ratings = ratings_df

    st.dataframe(filtered_ratings, use_container_width=True)

    st.download_button(
        "⬇️ Download Ratings CSV",
        data=filtered_ratings.to_csv(index=False).encode("utf-8"),
        file_name="ratings.csv",
        mime="text/csv",
        key="download_ratings"
    )
else:
    st.warning("No ratings found.")
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Likes
# -----------------------------
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<h3>❤️ Liked Places</h3>', unsafe_allow_html=True)
if not likes_df.empty:
    search_likes = st.text_input("🔍 Search likes", key="search_likes", placeholder="Search by any field…")
    if search_likes:
        mask = likes_df.apply(lambda row: row.astype(str).str.contains(search_likes, case=False, na=False).any(), axis=1)
        filtered_likes = likes_df[mask]
    else:
        filtered_likes = likes_df

    st.dataframe(filtered_likes, use_container_width=True)

    st.download_button(
        "⬇️ Download Likes CSV",
        data=filtered_likes.to_csv(index=False).encode("utf-8"),
        file_name="likes.csv",
        mime="text/csv",
        key="download_likes"
    )
else:
    st.warning("No likes found.")
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Most Rated Places (table)
# -----------------------------
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<h3>🏆 Most Rated Tourist Places</h3>', unsafe_allow_html=True)
if not top_places_df.empty:
    search_top = st.text_input("🔍 Search places", key="search_top", placeholder="Search by place name…")
    if search_top:
        mask = top_places_df.apply(lambda row: row.astype(str).str.contains(search_top, case=False, na=False).any(), axis=1)
        filtered_top = top_places_df[mask]
    else:
        filtered_top = top_places_df

    st.dataframe(filtered_top, use_container_width=True)

    st.download_button(
        "⬇️ Download Top Places CSV",
        data=filtered_top.to_csv(index=False).encode("utf-8"),
        file_name="top_places.csv",
        mime="text/csv",
        key="download_top_places"
    )
else:
    st.warning("No rating data available.")
st.markdown('</div>', unsafe_allow_html=True)

conn.close()

st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────
st.markdown("""
<p class="footer-text">© 2025 Smart Travel Planner · Admin Console</p>
""", unsafe_allow_html=True)