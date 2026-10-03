import pandas as pd
import joblib
import time

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier 
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)


DATA_PATH = Path("ml/data/food_training_data.csv")
MODEL_DIR = Path("ml/models")


def evaluate_model(name, model, X_train, X_test, y_train, y_test):

    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    # Training time
    start_train = time.perf_counter()

    model.fit(X_train, y_train)

    end_train = time.perf_counter()

    training_time = end_train - start_train

    # Prediction time
    start_predict = time.perf_counter()

    predictions = model.predict(X_test)

    end_predict = time.perf_counter()

    prediction_time = end_predict - start_predict

    # Metrics
    accuracy = accuracy_score(y_test, predictions)

    precision = precision_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0,
    )

    recall = recall_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0,
    )

    f1 = f1_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0,
    )

    print(f"\nAccuracy          : {accuracy:.4f}")
    print(f"Precision         : {precision:.4f}")
    print(f"Recall            : {recall:.4f}")
    print(f"F1 Score          : {f1:.4f}")
    print(f"Training Wall Time: {training_time:.6f} seconds")
    print(f"Prediction Time   : {prediction_time:.6f} seconds")

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0,
        )
    )

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, predictions))

    return {
        "model": name,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "training_time_seconds": training_time,
        "prediction_time_seconds": prediction_time,
    }


def main():

    print("Loading IFCT 2017 dataset...")

    df = pd.read_csv(DATA_PATH)

    print(f"Total foods: {len(df)}")

    # Combine food name with food group information
    #
    # NOTE:
    # For a real predictive model, the target label
    # food_group must NOT be included in the input text.
    #
    # Therefore we only use food_name as the feature.
    X = df["food_name"].fillna("")

    y = df["food_group"]

    print(f"Number of food groups: {y.nunique()}")

    print("\nFood groups:")
    print(y.value_counts())

    # Stratified split keeps class proportions where possible
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    print("\nDataset split:")
    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples : {len(X_test)}")

    # ---------------------------------------------------------
    # MODEL 1: TF-IDF + LOGISTIC REGRESSION
    # ---------------------------------------------------------

    logistic_model = Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=True,
                    ngram_range=(1, 2),
                ),
            ),
            (
                "classifier",
                LogisticRegression(
                    max_iter=2000,
                ),
            ),
        ]
    )

    results_1 = evaluate_model(
        "TF-IDF + Logistic Regression",
        logistic_model,
        X_train,
        X_test,
        y_train,
        y_test,
    )

    # ---------------------------------------------------------
    # MODEL 2: TF-IDF + LINEAR SVM
    # ---------------------------------------------------------

    svm_model = Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=True,
                    ngram_range=(1, 2),
                ),
            ),
            (
                "classifier",
                LinearSVC(),
            ),
        ]
    )

    results_2 = evaluate_model(
        "TF-IDF + Linear SVM",
        svm_model,
        X_train,
        X_test,
        y_train,
        y_test,
    )
    # ---------------------------------------------------------
    # MODEL 3: TF-IDF + RANDOM FOREST
    # ---------------------------------------------------------

    random_forest_model = Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=True,
                    ngram_range=(1, 2),
                ),
            ),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=200,
                    random_state=42,
                    n_jobs=-1,
                ),
            ),
        ]
    )

    results_3 = evaluate_model(
        "TF-IDF + Random Forest",
        random_forest_model,
        X_train,
        X_test,
        y_train,
        y_test,
    )   
    # ---------------------------------------------------------
    # SAVE MODELS
    # ---------------------------------------------------------

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    joblib.dump(
        logistic_model,
        MODEL_DIR / "food_group_logistic.joblib",
    )

    joblib.dump(
        svm_model,
        MODEL_DIR / "food_group_svm.joblib",
    )
    joblib.dump(
        random_forest_model,
        MODEL_DIR / "food_group_random_forest.joblib",
    )

    # ---------------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------------

    results = pd.DataFrame(
    [
        results_1,
        results_2,
        results_3,
    ]
)

    print("\n" + "=" * 60)
    print("MODEL COMPARISON")
    print("=" * 60)

    print(
        results.to_string(
            index=False
        )
    )

    results.to_csv(
        MODEL_DIR / "food_classifier_results.csv",
        index=False,
    )

    print("\nModels saved successfully.")
    print(
        f"Results saved to: "
        f"{MODEL_DIR / 'food_classifier_results.csv'}"
    )


if __name__ == "__main__":
    main()