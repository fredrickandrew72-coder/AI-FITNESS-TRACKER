import pandas as pd
import numpy as np
from pathlib import Path
import shutil
import json

PROJECT = Path(r"C:\Users\Hp\OneDrive\Desktop\AI FITNESS TRACKER")
SOURCE = Path(r"C:\Users\Hp\Downloads\ai_training_evidence")

TRAINING = PROJECT / "results" / "training"
GRAPHS = PROJECT / "results" / "graphs"

TRAINING.mkdir(parents=True, exist_ok=True)
GRAPHS.mkdir(parents=True, exist_ok=True)

MODELS = ["yolov8n", "yolov8s", "yolo11n", "yolo11s"]

all_data = []
summary = []

for model in MODELS:

    source_csv = SOURCE / model / "results.csv"

    print(f"\nProcessing {model}...")

    if not source_csv.exists():
        print(f"ERROR: {source_csv} not found")
        continue

    df = pd.read_csv(source_csv)

    # -------------------------------------------------------
    # Epoch numbering
    # -------------------------------------------------------
    df["epoch"] = df["epoch"].astype(int)

    # -------------------------------------------------------
    # Calculate per-epoch wall time
    # 'time' is cumulative elapsed seconds
    # -------------------------------------------------------
    df["epoch_wall_time_sec"] = df["time"].diff()

    # First epoch starts from time zero
    df.loc[df.index[0], "epoch_wall_time_sec"] = df.loc[df.index[0], "time"]

    df["epoch_wall_time_min"] = (
        df["epoch_wall_time_sec"] / 60
    )

    # -------------------------------------------------------
    # Calculate validation F1
    # -------------------------------------------------------
    p = df["metrics/precision(B)"]
    r = df["metrics/recall(B)"]

    df["metrics/F1(B)"] = np.where(
        (p + r) > 0,
        2 * p * r / (p + r),
        0
    )

    # -------------------------------------------------------
    # Add model column
    # -------------------------------------------------------
    df.insert(0, "model", model)

    # -------------------------------------------------------
    # Save full epoch metrics
    # -------------------------------------------------------
    output_csv = TRAINING / f"{model}_epoch_metrics.csv"

    df.to_csv(
        output_csv,
        index=False
    )

    all_data.append(df)

    # -------------------------------------------------------
    # Best epoch based on mAP50-95
    # -------------------------------------------------------
    best_index = df["metrics/mAP50-95(B)"].idxmax()
    best = df.loc[best_index]

    total_seconds = float(df["time"].iloc[-1])

    summary.append({
        "Model": model,
        "Epochs Completed": int(len(df)),
        "Best Epoch": int(best["epoch"]),
        "Precision": float(best["metrics/precision(B)"]),
        "Recall": float(best["metrics/recall(B)"]),
        "F1": float(best["metrics/F1(B)"]),
        "mAP50": float(best["metrics/mAP50(B)"]),
        "mAP50-95": float(best["metrics/mAP50-95(B)"]),
        "Total Training Time (sec)": total_seconds,
        "Total Training Time (min)": total_seconds / 60,
        "Average Epoch Time (sec)": float(df["epoch_wall_time_sec"].mean())
    })

    # -------------------------------------------------------
    # Copy graphs
    # -------------------------------------------------------
    graph_files = [
        "results.png",
        "confusion_matrix.png",
        "confusion_matrix_normalized.png"
    ]

    for graph in graph_files:

        source_graph = SOURCE / model / graph

        if source_graph.exists():

            destination_name = (
                f"{model}_{graph}"
            )

            shutil.copy2(
                source_graph,
                GRAPHS / destination_name
            )

    print(f"  Epochs: {len(df)}")
    print(f"  Best epoch: {int(best['epoch'])}")
    print(f"  Best mAP50-95: {best['metrics/mAP50-95(B)']:.4f}")
    print(f"  Total time: {total_seconds / 60:.2f} minutes")
    print(f"  Saved: {output_csv}")

# -----------------------------------------------------------
# Combined epoch dataset
# -----------------------------------------------------------

if all_data:

    combined = pd.concat(
        all_data,
        ignore_index=True
    )

    combined.to_csv(
        TRAINING / "all_models_epoch_metrics.csv",
        index=False
    )

# -----------------------------------------------------------
# Training summary
# -----------------------------------------------------------

summary_df = pd.DataFrame(summary)

summary_df.to_csv(
    TRAINING / "training_summary.csv",
    index=False
)

# -----------------------------------------------------------
# Print final summary
# -----------------------------------------------------------

print("\n")
print("=" * 90)
print("TRAINING SUMMARY")
print("=" * 90)

print(
    summary_df.to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}"
    )
)

print("\n")
print("=" * 90)
print("FILES CREATED")
print("=" * 90)

for path in sorted(TRAINING.glob("*")):
    print(path)

print("\nGraphs:")

for path in sorted(GRAPHS.glob("*")):
    print(path)

print("\nDONE.")
