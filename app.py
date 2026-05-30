import streamlit as st
import pandas as pd
import pickle

# Load Model
with open("model/recommendation_model.pkl", "rb") as file:
    data, similarity = pickle.load(file)

# Recommendation Function
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

        # Apply Filters
        if (
            recommended_place["Budget"] == budget
            and
            recommended_place["Climate"] == climate
        ):

            recommended_places.append(recommended_place)

        if len(recommended_places) == 3:
            break

    return recommended_places

# Page Title
st.title("Tourist Place Recommendation System")

st.write(
    "Find the best tourist destinations using Machine Learning"
)

# User Inputs
selected_place = st.selectbox(
    "Select Tourist Place",
    data["Place"].values
)

budget = st.selectbox(
    "Select Budget",
    ["Low", "Medium", "High"]
)

climate = st.selectbox(
    "Select Climate",
    ["Hot", "Cold", "Moderate"]
)

# Recommendation Button
if st.button("Recommend"):

    recommendations = recommend(
        selected_place,
        budget,
        climate
    )

    st.subheader("Recommended Places")

    if len(recommendations) == 0:

        st.write("No matching places found.")

    else:

        for place in recommendations:

            st.write("📍", place["Place"])

            # Rating
            st.write(
                "⭐ Rating:",
                place["Rating"]
            )

            # Climate
            st.write(
                "🌤 Climate:",
                place["Climate"]
            )

            # Budget
            st.write(
                "💰 Budget:",
                place["Budget"]
            )

            # Display Image
            image_path = (
                "images/" + place["Image"]
            )

            try:
                st.image(
                    image_path,
                    width=300
                )

            except:
                st.write("Image not found.")

            # Google Maps
            st.markdown(
                f"[Open in Google Maps]({place['Map']})"
            )

            st.write("--------------------------------")

# Sidebar
st.sidebar.title("Top Destinations")

top_places = [
    "Goa",
    "Kerala",
    "Manali",
    "Leh"
]

for place in top_places:

    st.sidebar.write("🌍", place)