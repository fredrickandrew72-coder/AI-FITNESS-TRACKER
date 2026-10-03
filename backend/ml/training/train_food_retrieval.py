import pandas as pd
import joblib

from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer


DATA_PATH = Path("ml/data/food_training_data.csv")
MODEL_PATH = Path("ml/models/food_tfidf.joblib")


def main():
    print("Loading food dataset...")

    df = pd.read_csv(DATA_PATH)

    # Combine food name and food group
    # This gives the model more context for matching.
    df["search_text"] = (
        df["food_name"].fillna("")
        + " "
        + df["food_group"].fillna("")
    )

    print(f"Foods loaded: {len(df)}")

    # Convert food text into TF-IDF vectors
    vectorizer = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2)
    )

    matrix = vectorizer.fit_transform(df["search_text"])

    model = {
        "vectorizer": vectorizer,
        "matrix": matrix,
        "food_data": df
    }

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, MODEL_PATH)

    print(f"TF-IDF matrix shape: {matrix.shape}")
    print(f"Model saved to: {MODEL_PATH}")
    print("\nFood retrieval model training complete!")


if __name__ == "__main__":
    main()