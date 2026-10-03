\# Food Detection Model Evaluation



\## Overview



This directory documents the food detection model experiments used in the AI Fitness \& Nutrition Assistant project.



The food detection component identifies Indian/Tamil food items from images and provides the detected food classes to the downstream nutrition analysis pipeline.



\## Dataset



\*\*Dataset:\*\* Tamil and Indian Food Detection Dataset 2



\* Number of classes: \*\*98\*\*

\* Training images: \*\*3,672\*\*

\* Clean validation images: \*\*495\*\*

\* Clean test images: \*\*353\*\*

\* Test annotation instances: \*\*364\*\*



The clean validation set was used for model comparison and checkpoint selection. The clean test set was kept untouched until the final evaluation.



\## Models Compared



Four YOLO models were trained using the same experimental protocol.



| Model   | Precision | Recall |     F1 |  mAP50 | mAP50-95 | Inference |

| ------- | --------: | -----: | -----: | -----: | -------: | --------: |

| YOLOv8n |    0.6404 | 0.6830 | 0.6610 | 0.7187 |   0.4391 |  4.071 ms |

| YOLOv8s |    0.6445 | 0.7068 | 0.6742 | 0.7524 |   0.4626 |  9.125 ms |

| YOLO11n |    0.6589 | 0.7017 | 0.6796 | 0.7513 |   0.4573 |  4.053 ms |

| YOLO11s |    0.6943 | 0.6880 | 0.6911 | 0.7517 |   0.4656 |  9.414 ms |



Model comparison was performed on the same \*\*495-image clean validation set\*\*.



\## Selected Model



\*\*YOLO11s\*\* was selected based on the clean validation evaluation.



Validation results:



\* Precision: \*\*0.6943\*\*

\* Recall: \*\*0.6880\*\*

\* F1: \*\*0.6911\*\*

\* mAP50: \*\*0.7517\*\*

\* mAP50-95: \*\*0.4656\*\*

\* Inference time: \*\*9.414 ms/image\*\*

\* Parameters: \*\*9,465,718\*\*

\* Best checkpoint size: \*\*18.37 MB\*\*



The selected checkpoint was Ultralytics' internal `best.pt`.



\## Final Test Evaluation



After model selection, YOLO11s was evaluated once on the untouched clean test set.



Test results:



| Metric         |             Result |

| -------------- | -----------------: |

| Precision      |         \*\*0.6344\*\* |

| Recall         |         \*\*0.6533\*\* |

| F1             |         \*\*0.6437\*\* |

| mAP50          |         \*\*0.7198\*\* |

| mAP50-95       |         \*\*0.4378\*\* |

| Inference      | \*\*9.873 ms/image\*\* |

| Test images    |            \*\*353\*\* |

| Test instances |            \*\*364\*\* |



The final evaluation was performed without modifying the test dataset or using it for model selection.



\## Validation vs Test



| Metric    | Validation |   Test | Difference |

| --------- | ---------: | -----: | ---------: |

| Precision |     0.6943 | 0.6344 |    -0.0599 |

| Recall    |     0.6880 | 0.6533 |    -0.0347 |

| F1        |     0.6911 | 0.6437 |    -0.0474 |

| mAP50     |     0.7517 | 0.7198 |    -0.0318 |

| mAP50-95  |     0.4656 | 0.4378 |    -0.0278 |



\## Training Protocol



The models were evaluated under a common experimental protocol:



\* Maximum epochs: \*\*100\*\*

\* Patience: \*\*30\*\*

\* Image size: \*\*640\*\*

\* Batch size: \*\*16\*\*

\* Seed: \*\*0\*\*

\* GPU: \*\*NVIDIA Tesla T4\*\*

\* Ultralytics version: \*\*8.4.171\*\*

\* Pretrained models: \*\*Yes\*\*

\* Training dataset: \*\*3,672 images\*\*

\* Model-selection dataset: \*\*495 clean validation images\*\*

\* Final evaluation dataset: \*\*353 clean test images\*\*



The same protocol was used for the four model comparisons.



\## Evaluation Integrity



The test set was kept separate from model selection.



Before final evaluation, the clean test set was checked for:



\* Image and label existence

\* Correct dataset configuration

\* Duplicate images

\* Validation/test overlap

\* Number of images

\* Number of annotation instances

\* Correct test YAML configuration



The final validator processed exactly \*\*353 test images and 364 annotation instances\*\*.



\## Result Files



The reproducible lightweight evaluation outputs are stored in the `results/` directory:



```text

results/

├── model\_comparison.csv

├── model\_comparison.json

└── yolo11s\_test\_clean\_eval\_summary.json

```



These files contain the model comparison and final test evaluation information.



\## Model Weights



The trained `.pt` model weights are intentionally not included in the normal Git repository.



Model checkpoints are larger binary artifacts and can be stored separately using a model-artifact repository or Git LFS when required.



The final selected checkpoint was:



```text

runs/yolo11s/weights/best.pt

```



Size: approximately \*\*18.37 MB\*\*.



\## Next Stage



The completed YOLO11s food detection model will be integrated into the AI Fitness \& Nutrition Assistant pipeline:



```text

Food Image

&#x20;   ↓

YOLO11s Food Detection

&#x20;   ↓

Detected Food + Confidence

&#x20;   ↓

Nutrition Database / RAG

&#x20;   ↓

Calories + Macronutrients + Micronutrients

&#x20;   ↓

User Profile + Activity + Fitness Goal

&#x20;   ↓

Personalized Nutrition Recommendation

```



