if __name__ == "__main__":
    # 라이브러리 임포트
    from ultralytics import YOLO
    import os
    import yaml

    # 기본 경로 설정
    model_path = 'models/'  # 모델이 저장될 경로
    data_path = 'data/'          # 데이터 세트 경로

    # 데이터 설정 파일(YAML) 생성
    data = {
        'train': os.path.join(data_path, 'train/images'),  # 학습 이미지 경로
        'val': os.path.join(data_path, 'val/images'),     # 검증 이미지 경로
        'test': os.path.join(data_path, 'test/images'),     # 테스트 이미지 경로
        'names': ['metal', 'vinyl', 'styrofoam', 'glass', 'paper', 'plastic'],
        'nc': 6  # 클래스 수
    }

    yaml_path = os.path.join(data_path, 'data.yaml')
    with open(yaml_path, 'w') as f:
        yaml.dump(data, f)

    # YOLO 모델 초기화 (사전 학습된 모델 사용)
    model = YOLO('yolo11n.pt')  # 'yolov8n.yaml' 대신 'yolov8n.pt' 사용

    # CUDA 사용
    model.to('cuda')

    # 학습 데이터 설정
    results = model.train(
        model='yolo11n.pt',  # 사전 학습된 모델 파일 이름
        data='data/data.yaml',      # 데이터 설정 파일 경로
        epochs=10,           # 학습 에폭 수
        patience=5,          # 조기 종료 인내 값
        batch=16,            # 배치 크기
        seed=42,             # 랜덤 시드
        optimizer='AdamW',   # 옵티마이저
        pretrained=True,     # 사전 학습된 가중치 사용
        device='cuda',       # GPU 사용
        save=True,           # 모델 저장 여부
        save_period=1,       # 모델 저장 주기
        amp=False,           # 자동 혼합 정밀도 사용 여부
        lr0=0.001            # 초기 학습률
    )
