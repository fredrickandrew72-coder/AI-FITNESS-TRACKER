# AI Fitness & Nutrition Assistant

> A multimodal, context-aware AI system for food recognition, nutrition analysis, fitness tracking, and personalized dietary recommendations for college and hostel students.

**Project Status:** 🚧 In Development  
**Current Completed Stage:** Food Detection Model Development and Evaluation

---

## 📌 Project Overview

The **AI Fitness & Nutrition Assistant** is an AI-based system designed to help college and hostel students monitor their food intake, understand nutrition, track fitness-related information, and receive personalized dietary recommendations.

The system is designed around a practical problem faced by students: food is often consumed from hostel messes, college canteens, restaurants, and outside-food sources, making accurate and consistent food logging difficult.

Instead of requiring users to manually search for every food item and enter its nutritional information, the proposed system aims to understand food through **images and natural-language input**, retrieve relevant nutritional information, consider the user's fitness goals and activity, and provide personalized recommendations.

The project combines:

- Computer Vision
- Food Object Detection
- Vision-Language Models (VLM)
- Natural Language Processing
- Nutrition Knowledge Retrieval
- Retrieval-Augmented Generation (RAG)
- Machine Learning
- Personalized Recommendation

The current development stage focuses on the **food detection component**, where multiple YOLO models have been trained and experimentally evaluated.

---

# 🎯 Problem Statement

Maintaining a proper diet and fitness routine can be difficult for college and hostel students.

Students frequently depend on:

- Hostel/mess food
- College canteens
- Restaurants
- Fast food
- Outside food
- Frequently changing menus

Existing calorie-counting and nutrition applications often depend heavily on manual food entry. Users may need to search for the food item, determine the quantity, and enter nutritional information themselves.

This creates several challenges:

- Manual food logging is time-consuming.
- Indian and regional foods may not always be represented accurately.
- Students may not know the nutritional composition of their meals.
- Hostel and mess menus change frequently.
- Food consumed outside the hostel may be difficult to log.
- Nutrition information is often separated from fitness activity and user goals.
- Generic recommendations may not account for individual requirements.

### Proposed Problem

The project aims to develop an intelligent system that can automatically understand food inputs, retrieve nutritional information, consider user context and fitness goals, and provide personalized nutrition assistance.

The system therefore investigates the following research direction:

> **Can a multimodal AI system combine food image understanding, nutrition knowledge retrieval, user context, and fitness information to provide practical and personalized nutrition assistance for college and hostel students?**

---

# 💡 Proposed Solution

The proposed system follows a multimodal pipeline where users can provide information through different inputs.

### Possible Inputs

- Food images
- Natural-language food descriptions
- Hostel/mess menu images
- Restaurant or outside-food information
- Fitness/activity information
- User goals and preferences

The system processes these inputs and produces:

- Food identification
- Nutritional information
- Calorie estimation
- Macronutrient information
- Micronutrient information where available
- Personalized nutrition suggestions
- Fitness-oriented food recommendations

### High-Level Architecture

```text
                         USER
                           |
          +----------------+----------------+
          |                |                |
      Food Image       Text Input      Menu Image
          |                |                |
          +----------------+----------------+
                           |
                           v
                  Food Understanding
                           |
              +------------+------------+
              |                         |
         YOLO11s                    VLM/NLP
      Food Detection           Future Integration
              |                         |
              +------------+------------+
                           |
                           v
                  Detected Food Items
                           |
                           v
             Nutrition Knowledge Layer
                  Database + RAG
                           |
                           v
              Nutritional Analysis
                           |
          +----------------+----------------+
          |                |                |
       Calories       Macronutrients   Micronutrients
          |                |                |
          +----------------+----------------+
                           |
                           v
                   User Context
                           |
          +----------------+----------------+
          |                |                |
      Fitness Goal      Activity       Preferences
          |                |                |
          +----------------+----------------+
                           |
                           v
             Personalized Recommendation
                           |
                           v
              AI Fitness Assistant

```

# 🧠 AI/ML Approach
The project is designed as a combination of multiple AI components.
## 1. Food Detection
The first major component is automatic food detection from images.
The current implementation uses YOLO-based object detection.
The following models were trained and compared:
- YOLOv8n
- YOLOv8s
- YOLO11n
- YOLO11s
The models were evaluated using the same experimental protocol to provide a fair comparison.


## 2. Vision-Language Model
A Vision-Language Model is planned as part of the broader multimodal system for understanding complex food images and menu images.
The VLM component is intended to help with cases where simple object detection may not be sufficient, such as:
- Understanding menu images
- Interpreting food descriptions
- Handling complex meal images
- Extracting contextual information from images
The complete VLM pipeline is part of the future integration stage.

## 3. Nutrition Knowledge Retrieval
After food items are identified, the system retrieves nutritional information from the project's nutrition data sources.
The nutrition layer is intended to provide information such as:
- Calories
- Protein
- Carbohydrates
- Fat
- Fiber
- Micronutrients
Processed nutrition datasets are already included in the project.

# 📊 Food Detection Dataset
Dataset: Tamil and Indian Food Detection Dataset 2
| Property | Value |
|---|---:|
| Food classes | **98** |
| Training images | **3,672** |
| Clean validation images | **495** |
| Clean test images | **353** |
| Test annotation instances | **364** |

The dataset is used for an object-detection use case with food class labels and bounding-box annotations.
The clean validation set was used for model comparison and model selection. The clean test set was kept untouched until final evaluation.

# 🔬 Current Experimental Results
The four YOLO models were compared on the same 495-image clean validation set.

| Model | Precision | Recall | F1 | mAP50 | mAP50-95 | Inference |
|---|---:|---:|---:|---:|---:|---:|
| YOLOv8n | 0.6404 | 0.6830 | 0.6610 | 0.7187 | 0.4391 | 4.071 ms |
| YOLOv8s | 0.6445 | 0.7068 | 0.6742 | 0.7524 | 0.4626 | 9.125 ms |
| YOLO11n | 0.6589 | 0.7017 | 0.6796 | 0.7513 | 0.4573 | 4.053 ms |
| **YOLO11s** | **0.6943** | **0.6880** | **0.6911** | **0.7517** | **0.4656** | **9.414 ms** |

## Selected Model: YOLO11s
YOLO11s was selected based on the clean validation evaluation.
- Precision: 0.6943
- Recall: 0.6880
- F1: 0.6911
- mAP50: 0.7517
- mAP50-95: 0.4656
- Inference: 9.414 ms/image
- Parameters: 9,465,718
- Model size: 18.37 MB

# 🧪 Final Test Evaluation
After model selection, YOLO11s was evaluated on the untouched clean test set.
| Metric | Result |
|---|---:|
| Precision | **0.6344** |
| Recall | **0.6533** |
| F1 | **0.6437** |
| mAP50 | **0.7198** |
| mAP50-95 | **0.4378** |
| Inference | **9.873 ms/image** |
| Test images | **353** |
| Test instances | **364** |

# ⚙️ Experimental Protocol
All four models were trained/evaluated using a common protocol:
- Maximum epochs: 100
- Patience: 30
- Image size: 640
- Batch size: 16
- Seed: 0
- GPU: NVIDIA Tesla T4
- Ultralytics: 8.4.171
- Pretrained models: Yes
- Training images: 3,672
- Validation images: 495
- Test images: 353
The test set was checked for image/label existence, duplicates, validation/test overlap, dataset configuration, image count, and annotation count.

## Experimental Evidence

The repository contains the experimental evidence generated during food-detection model development.

### Training Evidence

The four candidate models were trained under the same experimental protocol:

- YOLOv8n
- YOLOv8s
- YOLO11n
- YOLO11s

For each model, the repository contains epoch-level training and validation metrics, including:

- Training box loss
- Training classification loss
- Training distribution focal loss
- Validation box loss
- Validation classification loss
- Validation distribution focal loss
- Precision
- Recall
- F1-score
- mAP@50
- mAP@50–95
- Learning rates
- Cumulative training time
- Per-epoch wall time

Training evidence:

```text
results/training/
├── all_models_epoch_metrics.csv
├── training_summary.csv
├── yolov8n_epoch_metrics.csv
├── yolov8s_epoch_metrics.csv
├── yolo11n_epoch_metrics.csv
└── yolo11s_epoch_metrics.csv
```
## Training and Evaluation Graphs
Training curves and evaluation visualizations are available in:
results/graphs/

The directory contains:
- Training/validation result plots
- Confusion matrices
- Normalized confusion matrices
for all four candidate models.

## Consolidated Experimental Evidence
A machine-readable summary of the complete food-detection experiment is available at:
results/food_detection_experimental_evidence.json

### This file consolidates:
- Training metrics
- Best epoch
- Training duration
- Model comparison
- Independent validation results
- Final test results
- Experimental protocol
- Validation-to-test comparison
- Selected final model
## Evaluation Structure
The evaluation was separated into three stages:
1. Training evidence — epoch-by-epoch metrics recorded during model training.
2. Clean validation evaluation — used for model comparison and selection.
3. Final test evaluation — performed on the untouched test split after model selection.
The final selected model is YOLO11s.

## Final Test Evidence
The final YOLO11s model was evaluated on:
- 353 clean test images
- 364 annotated test instances
### Final test results:
| Metric | YOLO11s |
|---|---:|
| Precision | 0.6344 |
| Recall | 0.6533 |
| F1-score | 0.6437 |
| mAP@50 | 0.7198 |
| mAP@50–95 | 0.4378 |
| Inference time | 9.873 ms/image |

The complete test evaluation is stored in:
results/yolo11s_test_clean_eval_summary.json

The test split was not used during training or model selection.


# 📈 Current Project Progress
Completed
- [x] Project architecture defined
- [x] Nutrition datasets collected and processed
- [x] Food detection dataset prepared
- [x] Food detection annotations used
- [x] YOLOv8n trained
- [x] YOLOv8s trained
- [x] YOLO11n trained
- [x] YOLO11s trained
- [x] Four-model comparison completed
- [x] YOLO11s selected using clean validation data
- [x] Independent clean test evaluation completed
- [x] Experimental results documented
- [x] Backend development started
- [x] Frontend development started
- [x] Project pushed to GitHub
- [x] Add model evaluation visualizations
      
## In Progress
- [ ] Integrate YOLO11s with the backend
- [ ] Develop food detection API
- [ ] Connect detected food with nutrition data
- [ ] Implement nutrition retrieval / RAG
- [ ] Implement calorie and nutrient analysis
- [ ] Implement personalized recommendations
- [ ] Integrate fitness/activity information
- [ ] Integrate menu and food image understanding
- [ ] Perform complete end-to-end evaluation


# 🔬 Research Direction
The project investigates an integrated approach combining:
Food Recognition + Nutrition Knowledge + User Context + Fitness Activity + Personalized Recommendation
The main research question is:
Can a multimodal AI system combine food image understanding, nutrition retrieval, fitness information, and user context to provide practical and personalized nutrition assistance for college and hostel students?

The research contribution will be established through experimental evaluation, model comparisons, baseline comparisons, failure-case analysis, and evaluation of the complete integrated system rather than claiming novelty solely from application development.

# 🚀 Planned Pipeline
The completed YOLO11s model will be integrated into the broader system:
Food Image
    ↓
YOLO11s Food Detection
    ↓
Detected Food + Confidence
    ↓
Nutrition Database / RAG
    ↓
Calories + Macronutrients + Micronutrients
    ↓
User Profile + Activity + Fitness Goal
    ↓
Personalized Nutrition Recommendation

# 🗂️ Repository Structure
```text
AI-FITNESS-TRACKER/
├── backend/
├── frontend/
├── data/
│   └── processed/
│       ├── indian_food_nutrition.csv
│       └── indian_recipe_nutrition.csv
├── models/
│   └── README.md
├── results/  
  ├── model_comparison.csv
  ├── model_comparison.json
  ├── yolo11s_test_clean_eval_summary.json
  ├── food_detection_experimental_evidence.json
  ├── training/
  │   ├── all_models_epoch_metrics.csv
  │   ├── training_summary.csv
  │   ├── yolov8n_epoch_metrics.csv
  │   ├── yolov8s_epoch_metrics.csv
  │   ├── yolo11n_epoch_metrics.csv
  │   └── yolo11s_epoch_metrics.csv
  └── graphs/
      ├── yolov8n_results.png
      ├── yolov8n_confusion_matrix.png
      ├── yolov8n_confusion_matrix_normalized.png
      ├── yolov8s_results.png
      ├── yolov8s_confusion_matrix.png
      ├── yolov8s_confusion_matrix_normalized.png
      ├── yolo11n_results.png
      ├── yolo11n_confusion_matrix.png
      ├── yolo11n_confusion_matrix_normalized.png
      ├── yolo11s_results.png
      ├── yolo11s_confusion_matrix.png
      └── yolo11s_confusion_matrix_normalized.png
├── .gitignore
└── README.md
```

Detailed food detection experiments are documented in:
models/README.md

# 🛠️ Technology Stack
## AI / ML
- Python
- Ultralytics YOLO
- YOLOv8
- YOLO11
- Machine Learning
- Vision-Language Models
- RAG
- NLP
- Recommendation Systems
## Backend
- Node.js
- Express.js
- REST API
## Frontend
- React
- TypeScript
- Vite
## Database
- MongoDB
## Development
- Git
- GitHub
- Kaggle
- VS Code


# ⚠️ Current Limitations
The complete system is still under development.
Current limitations include:
- Food detection is limited to the classes represented in the dataset.
- Food appearance can vary with lighting, camera angle, presentation, and image quality.
- Visually similar food items may be difficult to distinguish.
- Nutrition estimates depend on the available nutrition data.
- Portion-size estimation requires further development.
- The complete recommendation pipeline has not yet been evaluated.
- Further testing across real-world users and environments is required.


# 📌 Current Status
Food Detection Model
Completed ✅
Selected model: YOLO11s
Final clean-test performance:
- mAP50: 0.7198
- mAP50-95: 0.4378
- F1: 0.6437
- Inference: 9.873 ms/image

## Overall AI Fitness & Nutrition Assistant
In Development 🚧
The next major milestone is integrating the validated YOLO11s food detection model with the nutrition, RAG, user-context, fitness, and recommendation components.
