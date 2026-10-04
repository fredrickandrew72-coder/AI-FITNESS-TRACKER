import pandas as pd
import json
from pathlib import Path

PROJECT = Path(r"C:\Users\Hp\OneDrive\Desktop\AI FITNESS TRACKER")
RESULTS = PROJECT / "results"

# ---------------------------------------------------------
# Training summary
# ---------------------------------------------------------
training_file = RESULTS / "training" / "training_summary.csv"

training = pd.read_csv(training_file)

# ---------------------------------------------------------
# Validation/model-selection results
# ---------------------------------------------------------
validation = [
    {
        "model": "YOLOv8n",
        "precision": 0.6404,
        "recall": 0.6830,
        "f1": 0.6610,
        "mAP50": 0.7187,
        "mAP50-95": 0.4391,
        "inference_ms": 4.071,
        "parameters": 3326166,
        "best_model_size_mb": 6.57,
        "peak_gpu_gb": 2.20,
        "training_time_min": 54.31
    },
    {
        "model": "YOLOv8s",
        "precision": 0.6445,
        "recall": 0.7068,
        "f1": 0.6742,
        "mAP50": 0.7524,
        "mAP50-95": 0.4626,
        "inference_ms": 9.125,
        "parameters": 11173526,
        "best_model_size_mb": 21.55,
        "peak_gpu_gb": 3.51,
        "training_time_min": 62.30
    },
    {
        "model": "YOLO11n",
        "precision": 0.6589,
        "recall": 0.7017,
        "f1": 0.6796,
        "mAP50": 0.7513,
        "mAP50-95": 0.4573,
        "inference_ms": 4.053,
        "parameters": 2652232,
        "best_model_size_mb": 5.35,
        "peak_gpu_gb": 2.48,
        "training_time_min": 56.54
    },
    {
        "model": "YOLO11s",
        "precision": 0.6943,
        "recall": 0.6880,
        "f1": 0.6911,
        "mAP50": 0.7517,
        "mAP50-95": 0.4656,
        "inference_ms": 9.414,
        "parameters": 9465718,
        "best_model_size_mb": 18.37,
        "peak_gpu_gb": 4.05,
        "training_time_min": 75.27
    }
]

# ---------------------------------------------------------
# Final untouched test evaluation
# ---------------------------------------------------------
test = {
    "model": "YOLO11s",
    "test_images": 353,
    "test_instances": 364,
    "precision": 0.6344,
    "recall": 0.6533,
    "f1": 0.6437,
    "mAP50": 0.7198,
    "mAP50-95": 0.4378,
    "inference_ms_per_image": 9.873,
    "evaluation_time_seconds": 6.1,
    "parameters": 9465718,
    "best_model_size_mb": 18.37,
    "peak_gpu_gb": 0.83
}

# ---------------------------------------------------------
# Experimental protocol
# ---------------------------------------------------------
protocol = {
    "training_images": 3672,
    "clean_validation_images": 495,
    "clean_test_images": 353,
    "test_annotation_instances": 364,
    "classes": 98,
    "max_epochs": 100,
    "patience": 30,
    "image_size": 640,
    "batch_size": 16,
    "seed": 0,
    "gpu": "NVIDIA Tesla T4",
    "ultralytics_version": "8.4.171",
    "pretrained": True,
    "selected_model": "YOLO11s",
    "selection_basis": "Clean validation evaluation"
}

# ---------------------------------------------------------
# Validation vs final test
# ---------------------------------------------------------
yolo11s_val = next(
    x for x in validation
    if x["model"] == "YOLO11s"
)

validation_test = {}

for metric in [
    "precision",
    "recall",
    "f1",
    "mAP50",
    "mAP50-95"
]:
    validation_test[metric] = {
        "validation": yolo11s_val[metric],
        "test": test[metric],
        "difference": round(
            test[metric] - yolo11s_val[metric],
            4
        )
    }

# ---------------------------------------------------------
# Final evidence document
# ---------------------------------------------------------
evidence = {
    "project": "AI Fitness & Nutrition Assistant",
    "component": "Food Detection",
    "training_summary": training.to_dict(
        orient="records"
    ),
    "validation_model_comparison": validation,
    "final_test_evaluation": test,
    "experimental_protocol": protocol,
    "yolo11s_validation_vs_test": validation_test
}

output = RESULTS / "food_detection_experimental_evidence.json"

with open(
    output,
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        evidence,
        f,
        indent=2
    )

print("=" * 80)
print("FINAL FOOD DETECTION EXPERIMENTAL EVIDENCE")
print("=" * 80)

print("\nTraining:")
print(training.to_string(index=False))

print("\nFinal YOLO11s Test:")
for key, value in test.items():
    print(f"{key}: {value}")

print("\nSaved:")
print(output)
