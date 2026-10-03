import pandas as pd
import joblib
import time

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# --------------------------------------------------
# 1. Load dataset
# --------------------------------------------------

DATA_PATH = "ml/data/food_training_data.csv"

df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)


# --------------------------------------------------
# 2. Select features and target
# --------------------------------------------------

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

df = df.dropna(subset=features + [target])

X = df[features]
y = df[target]

print("Samples after cleaning:", len(df))
print("Features:", len(features))
print("Target:", target)


# --------------------------------------------------
# 3. Train-test split
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# --------------------------------------------------
# 4. Models
# --------------------------------------------------

models = {
    "Linear Regression": LinearRegression(),

    "Random Forest": RandomForestRegressor(
        n_estimators=200,
        random_state=42
    ),

    "Gradient Boosting": GradientBoostingRegressor(
        n_estimators=200,
        random_state=42
    )
}


results = []


# --------------------------------------------------
# 5. Train and evaluate
# --------------------------------------------------

for name, model in models.items():

    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    start_time = time.perf_counter()

    model.fit(X_train, y_train)

    training_time = time.perf_counter() - start_time

    start_time = time.perf_counter()

    predictions = model.predict(X_test)

    prediction_time = time.perf_counter() - start_time

    mae = mean_absolute_error(y_test, predictions)

    rmse = mean_squared_error(
        y_test,
        predictions
    ) ** 0.5

    r2 = r2_score(y_test, predictions)

    print(f"MAE:              {mae:.4f}")
    print(f"RMSE:             {rmse:.4f}")
    print(f"R² Score:         {r2:.4f}")
    print(f"Training Time:    {training_time:.6f} sec")
    print(f"Prediction Time:  {prediction_time:.6f} sec")

    results.append({
        "Model": name,
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2,
        "Training_Time_sec": training_time,
        "Prediction_Time_sec": prediction_time
    })

    # Save model
    filename = name.lower().replace(" ", "_")

    joblib.dump(
        model,
        f"ml/models/nutrition_{filename}.joblib"
    )


# --------------------------------------------------
# 6. Save comparison
# --------------------------------------------------

results_df = pd.DataFrame(results)

results_df.to_csv(
    "ml/models/nutrition_regression_results.csv",
    index=False
)

print("\n" + "=" * 60)
print("MODEL COMPARISON")
print("=" * 60)

print(results_df.to_string(index=False))

print("\nResults saved to:")
print("ml/models/nutrition_regression_results.csv")