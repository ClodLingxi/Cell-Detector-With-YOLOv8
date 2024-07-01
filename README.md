# Cell Detector

**image handle** tool and **machine learning** algorithm.

## Abstract

- Based on **complete training** Cell Detector Model, we train it with **a small amount** other type cell Date.
- And finish detector task with **relatively High Accuracy** (Compare to other commercial cell detector Like Countess).
- We have **more than 80% confidence level**


## Model base
[keremberke/yolov8m-blood-cell-detection](https://huggingface.co/keremberke/yolov8m-blood-cell-detection)

## Method

Image Tool
- Split the cell image into **540 X 540**
- Apply thresholding using **Otsu's method** (with Gaussian blur pretreatment) 
- Find contours in the thresholded image
- Invert contours to [Label Studio](https://github.com/HumanSignal/label-studio) format
- Update labeling **semi-automatically**

Machine Learning 

- Training **blood-cell-detection** Model with Labeling date
- Finish Detector Task