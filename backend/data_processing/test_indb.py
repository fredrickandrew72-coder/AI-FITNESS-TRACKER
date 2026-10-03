import pandas as pd

df = pd.read_csv("../data/processed/indian_recipe_nutrition.csv")

names = [
    "idli",
    "dosa",
    "sambar",
    "chicken biryani",
    "veg biryani",
    "chapati",
    "parotta",
    "pongal",
    "upma",
    "curd rice",
]

for name in names:
    print(f"\n--- {name} ---")

    results = df[
        df["food_name"].str.contains(
            name,
            case=False,
            na=False
        )
    ]

    print(
        results[
            [
                "food_code",
                "food_name",
                "energy_kcal",
                "protein_g",
                "carb_g",
                "fat_g",
                "servings_unit",
            ]
        ].to_string(index=False)
    )