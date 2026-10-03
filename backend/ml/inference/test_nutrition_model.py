import pandas as pd
import joblib

# Load trained Gradient Boosting model
model = joblib.load(
    "ml/models/nutrition_gradient_boosting.joblib"
)

# Load dataset
df = pd.read_csv(
    "ml/data/food_training_data.csv"
)

features = [
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
    "zinc_mg"
]

# Select some real food records
samples = df.sample(10, random_state=42)

predictions = model.predict(samples[features])

print("\nNutrition Model Predictions")
print("=" * 80)

for (_, row), prediction in zip(samples.iterrows(), predictions):

    actual = row["energy_kcal"]

    print(
        f"{row['food_name'][:35]:35} | "
        f"Actual: {actual:8.2f} kcal | "
        f"Predicted: {prediction:8.2f} kcal | "
        f"Error: {abs(actual - prediction):8.2f}"
    )