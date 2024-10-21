from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from ultralytics import YOLO
import os

app = FastAPI()

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = 'runs/detect/train17/weights/best.pt'
model = YOLO(MODEL_PATH)

templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = 'board_user_auth'
RESULT_DIR = 'result'

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("testindex.html", {"request": request})

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    # 파일 저장 경로 설정
    user_file_path = os.path.join(UPLOAD_DIR, file.filename)

    # 파일을 지정된 경로에 저장
    with open(user_file_path, "wb") as f:
        f.write(await file.read())

    # 이미지 읽기
    img = cv2.imread(user_file_path)

    # 이미지 전처리
    img = cv2.resize(img, (640, 640))
    img = img / 255.0

    results = model.predict(source=img)
    detections = results[0].boxes
    count = len(detections)

    label_counts = {}
    
    for box in detections:
        x1, y1, x2, y2 = box.xyxy[0]
        label = int(box.cls[0]) 
        score = box.conf[0]

        if score > 0.5:
            label_text = label_map.get(label, str(label))
            label_counts[label_text] = label_counts.get(label_text, 0) + 1

            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            text = f"{label_text}: {score:.2f}"
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
            text_x = int(x1)
            text_y = int(y1 - 10 if y1 - 10 > 10 else y1 + text_size[1] + 10)
            cv2.putText(img, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 결과 이미지 저장
    result_file_path = os.path.join(RESULT_DIR, file.filename)
    cv2.imwrite(result_file_path, img * 255)  # 정규화된 이미지 복원 후 저장

    return JSONResponse(content={
        "count": count,
        "label_counts": label_counts,
        "result_image_path": result_file_path
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
