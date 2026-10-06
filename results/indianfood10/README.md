# IndianFood10 — YOLO11s Results

## Overview

YOLO11s was trained and evaluated on the corrected IndianFood10 dataset as a
specialized 10-class Indian food detection model.

The experiment follows the previous 98-class food detection experiment and
allows a direct comparison of the standard object-detection metrics.

---

## Dataset

- Training images: 9,199
- Validation images: 1,726
- Test images: 574
- Test instances: 1,069
- Number of classes: 10

## Classes

1. Aloo Paratha
2. Rasgulla
3. Biryani
4. Chicken Tikka
5. Palak Paneer
6. Poha
7. Khichdi
8. Omelette
9. Plain Rice
10. Chapati

---

## Training Configuration

- Model: YOLO11s
- Epochs: 50
- Patience: 15
- Image size: 640
- Batch size: 16
- Seed: 0
- GPU: NVIDIA Tesla T4
- Training time: 01:42:49.06
- Ultralytics: 8.4.171
- PyTorch: 2.11.0+cu128
- Python: 3.13.15

---

# Previous Model vs IndianFood10 Model

The following table compares the previous 98-class YOLO experiments with
the new YOLO11s model trained on the focused IndianFood10 dataset.

| Model | Dataset | Accuracy* | Precision | Recall | F1 | mAP50 | mAP50-95 | Inference |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| YOLOv8n | Previous 98-class | 66.10% | 64.04% | 68.30% | 66.10% | 71.87% | 43.91% | 4.071 ms |
| YOLOv8s | Previous 98-class | 67.42% | 64.45% | 70.68% | 67.42% | 75.24% | 46.26% | 9.125 ms |
| YOLO11n | Previous 98-class | 67.96% | 65.89% | 70.17% | 67.96% | 75.13% | 45.73% | 4.053 ms |
| YOLO11s | Previous 98-class | 69.11% | 69.43% | 68.80% | 69.11% | 75.17% | 46.56% | 9.414 ms |
| **YOLO11s** | **IndianFood10** | **~91.80%** | **92.60%** | **91.00%** | **~91.80%** | **95.40%** | **75.34%** | **~7.8 ms** |

### Improvement of YOLO11s on IndianFood10

Compared with the previous YOLO11s 98-class experiment:

| Metric | Previous YOLO11s | IndianFood10 YOLO11s | Improvement |
|---|---:|---:|---:|
| Accuracy* | 69.11% | ~91.80% | ~+22.69 pp |
| Precision | 69.43% | 92.60% | +23.17 pp |
| Recall | 68.80% | 91.00% | +22.20 pp |
| F1 | 69.11% | ~91.80% | ~+22.69 pp |
| mAP50 | 75.17% | 95.40% | +20.23 pp |
| mAP50-95 | 46.56% | 75.34% | +28.78 pp |

The results show substantially stronger detection performance on the focused
10-class IndianFood10 dataset.

**Important:** the two experiments use different datasets and therefore the
comparison demonstrates numerical performance differences between the
experiments; it should not be interpreted as a controlled benchmark of model
architecture alone.

---

# Clean TEST Results

The final YOLO11s IndianFood10 model was evaluated on the held-out clean
test set containing 574 images and 1,069 ground-truth instances.

| Metric | Result |
|---|---:|
| **Project Detection Accuracy** | **94.20%** |
| Precision | **93.24%** |
| Recall | **91.55%** |
| F1 | **92.39%** |
| mAP50 | **95.44%** |
| mAP50-95 | **76.51%** |
| Inference | **9.80 ms/image** |

## Test Matching

- Total ground-truth objects: 1,069
- Correctly matched objects: 1,007
- Project Detection Accuracy: 94.20%

---

# Detection Accuracy Definition

Standard YOLO object detection does not use a single overall
classification-accuracy metric.

For this project, **Detection Accuracy** is defined as:

**Correctly matched ground-truth objects / total ground-truth objects**

A prediction is considered a correct match when:

- IoU >= 0.50
- Confidence >= 0.25
- Predicted class is correct
- One-to-one ground-truth/prediction matching is satisfied

Therefore:

**1,007 / 1,069 = 94.20%**

This metric is a **project-defined detection metric** and is not standard
image-classification accuracy.

---

# Accuracy Column Note

The previous experiment's results table used an `accuracy` column whose
values are numerically identical to the reported F1 values.

For example, the previous YOLO11s result reported:

- Accuracy: 69.11%
- F1: 69.11%

Therefore, the `Accuracy*` column in the comparison table is retained for
continuity with the previous report, but it should be interpreted as the
reported F1-equivalent value rather than an independent classification
accuracy metric.

The **94.20% Project Detection Accuracy** reported in the clean TEST section
is a separate project-defined object-matching metric.

---

# Model

The final trained model is:

`model/yolo11s_indianfood10_best.pt`

---

# Results Included

This results directory contains:

- Training metrics
- Test metrics
- Per-class metrics
- Precision/Recall/F1 curves
- PR curve
- Confusion matrices
- Normalized confusion matrix
- Training graphs
- Validation prediction examples
- Training configuration
- Final model reference
