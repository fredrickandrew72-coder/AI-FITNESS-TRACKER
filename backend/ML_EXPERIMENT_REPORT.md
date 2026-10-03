# AI Fitness & Nutrition Assistant
## Machine Learning Experiment Report

---

## 1. Objective

The objective of this experiment was to establish initial machine learning baselines for the AI Fitness & Nutrition Assistant using the Indian Food Composition Tables (IFCT 2017) dataset.

Two machine learning tasks were evaluated:

1. Food-group classification
2. Energy/calorie regression

These experiments provide baseline models before integrating the multimodal food-image understanding component.

---

# 2. Dataset

The processed IFCT dataset contains:

- 542 food records
- 20 food groups
- 20 nutritional/data columns

The dataset was prepared from the IFCT 2017 nutritional data.

For the classification experiment:

- Training samples: 433
- Testing samples: 109
- Test size: 20%
- Random state: 42
- Stratified split

---

# 3. Experiment 1 — Food Group Classification

## 3.1 Problem

The task was to predict the food group of a food item from its food name.

Example:

```text
Input:
Mango

Output:
Fruits


3.2 Feature Extraction

TF-IDF was used to convert food names into numerical features.

Configuration:

lowercase = True
ngram_range = (1, 2)


| Model                        |   Accuracy |  Precision |     Recall | Weighted F1 | Training Time |
| ---------------------------- | ---------: | ---------: | ---------: | ----------: | ------------: |
| TF-IDF + Logistic Regression |     63.30% |     71.29% |     63.30% |      60.51% |       0.098 s |
| TF-IDF + Linear SVM          | **72.48%** |     77.47% | **72.48%** |  **71.17%** |   **0.013 s** |
| TF-IDF + Random Forest       |     66.06% | **80.00%** |     66.06% |      64.94% |       0.267 s |
