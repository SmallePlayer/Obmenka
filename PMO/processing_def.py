from ultralytics import YOLO
import serial
import asyncio

def yolo_detect(version: str, weight: str, frame, show: bool):
    model = YOLO(f'yolo{version}{weight}.pt')
    while True:
        results =  model.predict(source=frame,show=show,imgsz=640)
        result = results[0]
        for box in result.boxes:
            class_id = box.cls[0].item()
            return class_id