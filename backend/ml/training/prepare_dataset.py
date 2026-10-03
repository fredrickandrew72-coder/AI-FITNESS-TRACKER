import pandas as pd
from pathlib import Path


INPUT_PATH = Path("ml/data/indian_food_nutrition.csv")
OUTPUT_PATH = Path("ml/data/food_training_data.csv")


def main():
    print("Loading IFCT 2017 dataset...")

    df = pd.read_csv(INPUT_PATH)

    print(f"Original rows: {len(df)}")
    print(f"Original columns: {len(df.columns)}")

    # Features useful for nutrition/recommendation models
    feature_columns = [
        "food_code",
        "food_name",
        "food_group",
        "energy_kcal",
        "protein_g",
        "fat_g",
        "carbohydrate_g",
        "fiber_g",
        "calcium_mg",
        "iron_mg",
        "magnesium_mg",
        "phosphorus_mg",
        "potassium_mg",
        "sodium_mg",
        "zinc_mg",
        "vitamin_a",
        "vitamin_b6",
        "vitamin_c_mg",
        "vitamin_d",
        "folate",
    ]

    df = df[feature_columns]

    # Remove rows without a food name
    df = df.dropna(subset=["food_name"])

    # Remove duplicate foods
    df = df.drop_duplicates(subset=["food_code"])

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(OUTPUT_PATH, index=False)

    print(f"Final rows: {len(df)}")
    print(f"Final columns: {len(df.columns)}")
    print(f"Saved to: {OUTPUT_PATH}")
    print("\nDataset preparation successful!")


if __name__ == "__main__":
    main()