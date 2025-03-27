# 🗑 Trash Detection using YOLO

## 📌 프로젝트 개요
본 프로젝트는 **YOLO(You Only Look Once) 모델을 활용하여 업로드된 이미지에서 쓰레기를 탐지하고 종류별 개수를 분석하는 서비스**입니다. 사용자가 이미지를 업로드하면 모델이 자동으로 분석하여 결과를 반환합니다.

## 🚀 주요 기능
### 1. 이미지 기반 객체 탐지
- 사용자가 업로드한 이미지에서 YOLO 모델을 이용해 **쓰레기 종류를 탐지**합니다.
- 탐지된 객체를 바운딩 박스로 표시하고, **클래스 라벨 및 신뢰도 점수**를 반환합니다.

### 2. REST API 제공
- `api_trash_detection.py`를 통해 **FastAPI 기반 REST API 서비스**를 제공합니다.
- 클라이언트는 이미지를 업로드하면 **탐지 결과(JSON)를 응답받을 수 있습니다.**

### 3. 모델 학습 및 개선
- `train11.py`를 활용하여 **YOLO 모델을 학습**하고, 학습된 가중치를 이용하여 새로운 이미지에서 탐지 성능을 개선할 수 있습니다.

## 🛠 기술 스택
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/> <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white"/> <img src="https://img.shields.io/badge/YOLO-00FFFF?style=for-the-badge"/> <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>

- **YOLOv11**: 객체 탐지 모델 사용
- **OpenCV**: 이미지 전처리 및 시각화
- **FastAPI**: RESTful API 개발
- **NumPy**: 데이터 처리 및 연산

## 💻 주요 코드 설명
### 1. FastAPI 기반 REST API (`api_trash_detection.py`)
```python
from fastapi import FastAPI, File, UploadFile
import cv2
import numpy as np
from ultralytics import YOLO
import os

app = FastAPI()

MODEL_PATH = 'runs/detect/train17/weights/best.pt'
model = YOLO(MODEL_PATH)

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    file_path = f"temp/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    img = cv2.imread(file_path)
    results = model.predict(source=img)
    detections = results[0].boxes
    label_counts = {}
    
    for box in detections:
        label = int(box.cls[0]) 
        score = box.conf[0]
        if score > 0.5:
            label_counts[label] = label_counts.get(label, 0) + 1
    
    return {"detections": label_counts}
```
- **YOLOv11을 사용하여 객체 탐지**를 수행합니다.
- 사용자가 업로드한 이미지에서 **쓰레기 종류 및 개수를 분석**합니다.
- 결과는 **JSON 형태**로 반환됩니다.

### 2. YOLO 모델 학습 (`train11.py`)
```python
from ultralytics import YOLO

model = YOLO("yolov11n.pt")
model.train(data="trash_dataset.yaml", epochs=50, imgsz=640)
model.export(format="onnx")
```
- YOLOv8 모델을 **사용자 정의 데이터셋**으로 학습합니다.
- 학습된 모델을 ONNX 형식으로 변환하여 **다양한 환경에서 활용 가능**하도록 합니다.

## 📊 결과 예시

<img src="https://github.com/user-attachments/assets/f43f289f-dda3-4e01-a6ca-44faf0c12db5" width="184" height="400"/>
<img src="https://github.com/user-attachments/assets/b18f743e-a706-49ca-b3bf-1ae45d2262a6" width="184" height="400"/>

- **YOLO 모델을 활용하여 폐기물 종류를 정확하게 탐지**합니다.
- API를 통해 **다른 서비스에서도 객체 탐지 기능을 사용할 수 있습니다**.

## 🔄 향후 개선 사항
✅ 탐지 정확도를 높이기 위해 **YOLOv11 기반 하이퍼파라미터 튜닝**  
✅ 대시보드 추가하여 **탐지 결과 시각화 및 로그 관리 기능 제공**  
✅ 더 다양한 쓰레기 종류를 학습할 수 있도록 **데이터셋 확장**  
