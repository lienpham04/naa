#!/bin/bash

cd /opt/airflow

# Train model using Ultralytics CLI (ví dụ YOLOv8)
yolo detect train model=yolov8n.pt data=config.yaml epochs=50 imgsz=640 project=trained_models name=yolov8_retrained

# Log to MLflow (ví dụ: save metrics to a file and log them)
python airflow/scripts/log_to_mlflow.py
