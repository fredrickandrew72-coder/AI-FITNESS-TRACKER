import joblib

# Load trained model
model = joblib.load("ml/models/food_group_svm.joblib")

test_foods = [
    "Amaranth seed, black",
    "Bajra",
    "Chicken leg",
    "Rice",
    "Mango",
    "Spinach",
    "Groundnut",
    "Egg",
    "Potato",
    "Fish"
]

predictions = model.predict(test_foods)

print("\nFood Group Predictions")
print("=" * 50)

for food, prediction in zip(test_foods, predictions):
    print(f"{food:30} -> {prediction}")