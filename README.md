# Trash-Detection

## 개요
YOLO를 활용한 쓰레기 분류 모델

## 전처리

prem.py 파일들 라벨링에 따라 클래스 넘버->문자 or 문자->클래스 넘버

이미지 속성 번역

이미지 속성을 영어로 번역하는 딕셔너리를 설정하여, 데이터의 일관성을 유지합니다.

필요 이미지 속성 리스트

모델 학습에 필요한 이미지 속성 리스트를 정의합니다:

해상도, ISO, 낮/밤, 장소, 물체 클래스, 물체 색상, 경계 박스 좌표 등.

파일 및 폴더 관리

확장자 설정: 처리할 이미지와 JSON 파일의 확장자를 설정합니다.

백업 디렉터리: 존재하지 않을 경우 백업 디렉터리를 생성합니다.

데이터 정리

필요 없는 데이터 및 오류 이미지를 제거하여 데이터를 정리합니다.

라벨링 데이터에서 필요 없는 클래스의 자료를 삭제합니다.

이미지 속성 값 추출

정리된 데이터에서 이미지 속성 값을 추출하여 CSV 파일로 저장합니다. 이 파일은 모델 학습에 필수적인 정보를 포함합니다.

데이터 전처리

이미지 크기를 640x640으로 조정하고 클래스 정보를 기반으로 데이터를 전처리합니다.

최종적으로 필요한 데이터 파일을 지정된 경로로 분배
## 데이터 구성

```
data = {
    'train': os.path.join(data_path, 'train/images'),
    'val': os.path.join(data_path, 'val/images'),
    'test': os.path.join(data_path, 'test/images'),
    'names': ['metal', 'vinyl', 'styrofoam', 'glass', 'paper', 'plastic'],
    'nc': 6  # 클래스 수
}
yaml_path = os.path.join(data_path, 'data.yaml')
with open(yaml_path, 'w') as f:
    yaml.dump(data, f)
```

데이터 경로와 클래스 이름을 설정하고, 이를 YAML 파일로 저장.

## 학습 설정

```
results = model.train(
    model='yolo11n.pt',
    data='data/data.yaml',
    epochs=10,
    patience=5,
    batch=16,
    seed=42,
    optimizer='AdamW',
    pretrained=True,
    device='cuda',
    save=True,
    save_period=1,
    lr0=0.001
)
```

지정된 하이퍼파라미터를 사용하여 모델 훈련.

## 결과

![11111](https://github.com/user-attachments/assets/7328a4ca-77c9-47bd-a21d-61c399e84289)

테스트 이미지 기준 95%의 정확도

<img src="https://github.com/user-attachments/assets/f43f289f-dda3-4e01-a6ca-44faf0c12db5" width="184" height="400"/>
<img src="https://github.com/user-attachments/assets/b18f743e-a706-49ca-b3bf-1ae45d2262a6" width="184" height="400"/>
