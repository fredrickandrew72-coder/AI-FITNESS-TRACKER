# IndianFood10 — YOLO11s Results

## Model

YOLO11s trained on the corrected IndianFood10 dataset.

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

## Training

- Model: YOLO11s
- Epochs: 50
- Image size: 640
- Batch size: 16
- GPU: NVIDIA Tesla T4
- Training time: 01:42:49.06
- Ultralytics: 8.4.171
- PyTorch: 2.11.0+cu128
- Python: 3.13.15

## Clean TEST Results

| Metric | Result |
|---|---:|
| Project Detection Accuracy | 94.20% |
| Precision | 93.24% |
| Recall | 91.55% |
| F1 | 92.39% |
| mAP50 | 95.44% |
| mAP50-95 | 76.51% |
| Inference | 9.80 ms/image |

## Detection Accuracy Definition

Detection Accuracy is a project-defined metric:

Correctly matched ground-truth objects / total ground-truth objects

Matching requirements:

- IoU >= 0.50
- Confidence >= 0.25
- Correct predicted class
- One-to-one ground-truth/prediction matching

This metric is NOT standard image-classification accuracy.

## Test Matching

- Total ground-truth objects: 1,069
- Correctly matched objects: 1,007
- Detection Accuracy: 94.20%

## Model

The final trained model is:

`model/yolo11s_indianfood10_best.pt`
