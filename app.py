import streamlit as st
import pandas as pd
import pickle

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="Tourist Place Recommendation System",
    page_icon="🌍",
    layout="wide"
)

# ---------------------------------------------------
# Custom CSS
# ---------------------------------------------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #e3f2fd, #ffffff);
}

/* Main Text */
html, body, [class*="css"] {
    color: black;
}

/* Header */
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

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(to bottom, #0E76A8, #053B50);
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Input Box */
div[data-baseweb="select"] {
    border-radius: 10px;
}

/* Button */
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

/* Recommendation Card */
.recommend-card {
    background: white;
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 25px;
    box-shadow: 0px 5px 20px rgba(0,0,0,0.15);
}

.recommend-card h2 {
    color: #0E76A8;
}

.recommend-card p {
    color: black;
    font-size: 18px;
}

.footer {
    text-align: center;
    color: #0E76A8;
    font-size: 22px;
    font-weight: bold;
}

.recommend-card {
    background: white !important;
    color: black !important;
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.2);
}

.recommend-card * {
    color: black !important;
}

.recommend-card h1,
.recommend-card h2,
.recommend-card h3,
.recommend-card p,
.recommend-card span,
.recommend-card div {
    color: black !important;
}
.recommend-card {
    background-color: white !important;
    color: black !important;
}

.recommend-card * {
    color: black !important;
    opacity: 1 !important;
}
/* Force all headings dark */
h1, h2, h3, h4, h5, h6 {
    color: #0E76A8 !important;
    opacity: 1 !important;
}

/* Force normal text dark */
p, span, div, label {
    color: #111111 !important;
}
/* Select Box */
div[data-baseweb="select"] > div {
    background: white !important;
    color: black !important;
    border: 1px solid #d3d3d3 !important;
}

/* Selected Value */
div[data-baseweb="select"] span {
    color: black !important;
}

/* Dropdown Menu */
div[role="listbox"] {
    background: white !important;
    border: 1px solid #d3d3d3 !important;
}

/* Dropdown Options */
div[role="option"] {
    background: white !important;
    color: black !important;
}

/* Hovered Option */
div[role="option"]:hover {
    background: #f0f2f6 !important;
    color: black !important;
}

/* Force all select elements */
[data-baseweb="select"],
[data-baseweb="select"] * {
    color: black !important;
}

/* Dropdown arrow */
[data-baseweb="select"] svg {
    fill: black !important;
}
/* Dropdown popup */
div[data-baseweb="popover"] {
    background-color: white !important;
}

/* Dropdown menu */
ul {
    background-color: white !important;
}

/* Options */
li {
    background-color: white !important;
    color: black !important;
}

/* Hover effect */
li:hover {
    background-color: #f0f2f6 !important;
    color: black !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Load Model
# ---------------------------------------------------
with open("model/recommendation_model.pkl", "rb") as file:
    data, similarity = pickle.load(file)

# ---------------------------------------------------
# Recommendation Function
# ---------------------------------------------------
def recommend(place, budget, climate):

    index = data[data["Place"] == place].index[0]

    scores = list(enumerate(similarity[index]))

    sorted_scores = sorted(
        scores,
        key=lambda x: x[1],
        reverse=True
    )

    recommended_places = []

    for i in sorted_scores[1:]:

        recommended_place = data.iloc[i[0]]

        if (
            recommended_place["Budget"] == budget
            and
            recommended_place["Climate"] == climate
        ):
            recommended_places.append(recommended_place)

        if len(recommended_places) == 3:
            break

    return recommended_places

# ---------------------------------------------------
# Header
# ---------------------------------------------------
st.markdown(
    '<div class="main-title">🌍 Tourist Place Recommendation System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Discover Amazing Destinations Using Machine Learning ✈️</div>',
    unsafe_allow_html=True
)

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------
st.sidebar.title("🌴 Popular Destinations")

popular_places = [
    "Goa",
    "Kerala",
    "Manali",
    "Leh"
]

for place in popular_places:
    st.sidebar.success(place)

st.sidebar.markdown("---")

st.sidebar.info(
    "Select your preferred destination, budget and climate to get recommendations."
)

# ---------------------------------------------------
# Input Section
# ---------------------------------------------------
st.markdown("## 🔍 Search Your Perfect Destination")

col1, col2 = st.columns(2)

with col1:
    selected_place = st.selectbox(
        "📍 Select Tourist Place",
        data["Place"].values
    )

with col2:
    budget = st.selectbox(
        "💰 Select Budget",
        ["Low", "Medium", "High"]
    )

climate = st.selectbox(
    "🌤 Select Climate",
    ["Hot", "Cold", "Moderate"]
)


# ---------------------------------------------------
# Recommendation Button
# ---------------------------------------------------
if st.button("🚀 Get Recommendations"):

    recommendations = recommend(
        selected_place,
        budget,
        climate
    )

    st.header("✨ Recommended Places")

    if len(recommendations) == 0:

        st.warning("No matching places found.")

    else:

        for place in recommendations:

            image_path = "images/" + place["Image"]

            st.markdown(
                '<div class="recommend-card">',
                unsafe_allow_html=True
            )

            col1, col2 = st.columns([1, 2])

            with col1:

                try:
                    st.image(
                        image_path,
                        use_container_width=True
                    )
                except:
                    st.warning("Image not found.")

            with col2:

                st.markdown(
    f"""
    <h2 style="color:#000000;">📍 {place['Place']}</h2>

    <p style="color:#000000; font-size:18px; font-weight:500;">
        ⭐ <b>Rating:</b> {place['Rating']}<br><br>
        🌤 <b>Climate:</b> {place['Climate']}<br><br>
        💰 <b>Budget:</b> {place['Budget']}
    </p>
    """,
    unsafe_allow_html=True
)

                st.markdown(
                    f"""
                    <a href="{place['Map']}" target="_blank">
                        <button style="
                        background:#0E76A8;
                        color:white;
                        border:none;
                        padding:12px 20px;
                        border-radius:10px;
                        font-size:16px;
                        cursor:pointer;">
                        📍 Open in Google Maps
                        </button>
                    </a>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

# ---------------------------------------------------
# Footer
# ---------------------------------------------------
st.markdown("---")

st.markdown(
    """
    <div class="footer">
    ✈️ Explore • Discover • Travel
    </div>
    """,
    unsafe_allow_html=True
)