import pandas as pd
from pathlib import Path


INPUT_PATH = Path("../data/raw/indian_nutrition/indb/INDB.xlsx")
OUTPUT_PATH = Path("../data/processed/indian_recipe_nutrition.csv")


def main():
    print("Loading INDB dataset...")

    df = pd.read_excel(
        INPUT_PATH,
        sheet_name="Nutrient Data"
    )

    print(f"Original rows: {len(df)}")
    print(f"Original columns: {len(df.columns)}")

    selected_columns = [
        "food_code",
        "food_name",
        "energy_kcal",
        "carb_g",
        "protein_g",
        "fat_g",
        "fibre_g",
        "calcium_mg",
        "iron_mg",
        "magnesium_mg",
        "phosphorus_mg",
        "sodium_mg",
        "potassium_mg",
        "zinc_mg",
        "vita_ug",
        "vitb6_mg",
        "vitc_mg",
        "folate_ug",
        "servings_unit",
        "unit_serving_energy_kcal",
        "unit_serving_protein_g",
        "unit_serving_carb_g",
        "unit_serving_fat_g",
        "unit_serving_fibre_g",
    ]

    df = df[selected_columns]

    # Remove rows without food names
    df = df.dropna(subset=["food_name"])

    # Remove duplicate food codes
    df = df.drop_duplicates(subset=["food_code"])

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(f"Final rows: {len(df)}")
    print(f"Final columns: {len(df.columns)}")
    print(f"Saved to: {OUTPUT_PATH}")

    print("\nFirst 5 foods:")
    print(
        df[
            [
                "food_code",
                "food_name",
                "energy_kcal",
                "protein_g",
                "carb_g",
                "fat_g",
                "servings_unit"
            ]
        ].head().to_string(index=False)
    )

    print("\nINDB processing successful!")


if __name__ == "__main__":
    main()