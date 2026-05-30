import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load Dataset
data = pd.read_csv("dataset/advanced_tourist_places.csv")

# Combine Features
data["features"] = (
    data["Type"] + " " +
    data["Climate"] + " " +
    data["Budget"]
)

# Convert Text into Matrix
cv = CountVectorizer()

matrix = cv.fit_transform(data["features"])

# Calculate Similarity
similarity = cosine_similarity(matrix)

# Save Model
with open("model/recommendation_model.pkl", "wb") as file:
    pickle.dump((data, similarity), file)

print("Model Saved Successfully!")