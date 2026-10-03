import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


# ============================================================
# 1. Load dataset
# ============================================================

df = pd.read_csv(
    "ml/data/food_training_data.csv"
)

X = df["food_name"]
y = df["food_group"]


# ============================================================
# 2. Same test split used during training
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ============================================================
# 3. Load saved SVM pipeline
# ============================================================

model = joblib.load(
    "ml/models/food_group_svm.joblib"
)


# ============================================================
# 4. Predict directly using raw text
# ============================================================

predictions = model.predict(X_test)


# ============================================================
# 5. Generate confusion matrix
# ============================================================

cm = confusion_matrix(
    y_test,
    predictions,
    labels=model.classes_
)

display = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=model.classes_
)

fig, ax = plt.subplots(figsize=(14, 12))

display.plot(
    ax=ax,
    xticks_rotation=90,
    cmap="Blues",
    values_format="d"
)

plt.title(
    "Food Group Classification - TF-IDF + Linear SVM"
)

plt.tight_layout()

plt.savefig(
    "ml/models/svm_confusion_matrix.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nConfusion matrix generated successfully.")
print(
    "Saved to: ml/models/svm_confusion_matrix.png"
)