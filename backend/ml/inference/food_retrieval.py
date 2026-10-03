import joblib
import pandas as pd

from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity


MODEL_PATH = Path("ml/models/food_tfidf.joblib")


def search_food(query, top_k=5):
    model = joblib.load(MODEL_PATH)

    vectorizer = model["vectorizer"]
    matrix = model["matrix"]
    food_data = model["food_data"]

    # Convert user query into TF-IDF vector
    query_vector = vectorizer.transform([query])

    # Calculate similarity with every food
    similarities = cosine_similarity(query_vector, matrix).flatten()

    # Get highest similarity scores
    top_indices = similarities.argsort()[::-1][:top_k]

    results = food_data.iloc[top_indices].copy()
    results["similarity"] = similarities[top_indices]

    # Remove results with no textual similarity
    results = results[results["similarity"] > 0]

    return results[
        [
            "food_code",
            "food_name",
            "food_group",
            "energy_kcal",
            "protein_g",
            "fat_g",
            "carbohydrate_g",
            "fiber_g",
            "similarity",
        ]
    ]


if __name__ == "__main__":
    query = input("Enter food name: ")

    results = search_food(query)

    print("\nMatching foods:\n")
    print(results.to_string(index=False))