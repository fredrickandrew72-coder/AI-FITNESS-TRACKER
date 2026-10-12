from pathlib import Path
from ultralytics import YOLO


MODEL_PATH = (
    Path(__file__).resolve().parents[3]
    / "models"
    / "food_detection"
    / "yolo11s_indianfood10_best.pt"
)

model = YOLO(str(MODEL_PATH))


def detect_food(image_path: str, confidence: float = 0.70):
    results = model.predict(
        source=image_path,
        conf=confidence,
        verbose=False
    )

    detections = []

    for result in results:
        if result.boxes is None:
            continue

        for box in result.boxes:
            class_id = int(box.cls[0])
            confidence_score = float(box.conf[0])

            detections.append({
                "class_id": class_id,
                "class_name": result.names[class_id],
                "confidence": confidence_score,
                "x1": float(box.xyxy[0][0]),
                "y1": float(box.xyxy[0][1]),
                "x2": float(box.xyxy[0][2]),
                "y2": float(box.xyxy[0][3]),
            })

    detections.sort(key=lambda x: x["confidence"], reverse=True)

    return detections
