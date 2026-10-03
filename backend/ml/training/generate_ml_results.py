import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


# ============================================================
# 1. Load results
# ============================================================

classification = pd.read_csv(
    "ml/models/food_classifier_results.csv"
)

regression = pd.read_csv(
    "ml/models/nutrition_regression_results.csv"
)

print("\nClassification Results")
print(classification)

print("\nRegression Results")
print(regression)


# ============================================================
# 2. Classification model comparison
# ============================================================

plt.figure(figsize=(8, 5))

plt.bar(
    classification["model"],
    classification["f1"]
)

plt.ylabel("Weighted F1 Score")
plt.title("Food Classification Model Comparison")
plt.xticks(rotation=20)
plt.tight_layout()

plt.savefig(
    "ml/models/classification_model_comparison.png",
    dpi=300
)

plt.close()


# ============================================================
# 3. Regression model comparison
# ============================================================

plt.figure(figsize=(8, 5))

plt.bar(
    regression["Model"],
    regression["R2"]
)

plt.ylabel("R² Score")
plt.title("Nutrition Regression Model Comparison")
plt.xticks(rotation=20)
plt.tight_layout()

plt.savefig(
    "ml/models/regression_model_comparison.png",
    dpi=300
)

plt.close()


# ============================================================
# 4. Load dataset
# ============================================================

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

target = "energy_kcal"


# ============================================================
# 5. Actual vs predicted calories
# ============================================================

from sklearn.model_selection import train_test_split

X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

model = joblib.load(
    "ml/models/nutrition_gradient_boosting.joblib"
)

predictions = model.predict(X_test)


plt.figure(figsize=(7, 7))

plt.scatter(
    y_test,
    predictions,
    alpha=0.7
)

# Perfect prediction reference line
minimum = min(y_test.min(), predictions.min())
maximum = max(y_test.max(), predictions.max())

plt.plot(
    [minimum, maximum],
    [minimum, maximum],
    linestyle="--"
)

plt.xlabel("Actual Energy (kcal)")
plt.ylabel("Predicted Energy (kcal)")
plt.title("Actual vs Predicted Energy - Gradient Boosting")

plt.tight_layout()

plt.savefig(
    "ml/models/actual_vs_predicted_calories.png",
    dpi=300
)

plt.close()


print("\nGenerated:")
print("1. classification_model_comparison.png")
print("2. regression_model_comparison.png")
print("3. actual_vs_predicted_calories.png")