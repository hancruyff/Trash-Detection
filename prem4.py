import os

# 클래스 매핑
class_mapping = {
    '12': '0',
    '15': '1',
    '16': '2',
    '17': '3',
    '21': '4',
    '22': '0',
    '23': '5',
    '24': '5'
}

# 라벨 파일 경로
labels_dir = 'data/test/labels'  # 라벨 파일이 있는 디렉토리 경로

# 라벨 파일 수정 함수
def update_class_in_labels(label_file):
    with open(label_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    updated_lines = []
    for line in lines:
        parts = line.strip().split()  # 라인 분리
        if len(parts) > 0:
            class_id = parts[0]  # 첫 번째 요소가 클래스 ID
            if class_id in class_mapping:
                # 클래스 ID 수정
                parts[0] = class_mapping[class_id]
            updated_lines.append(' '.join(parts))  # 수정된 라인 추가

    # 수정된 내용을 파일에 저장
    with open(label_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(updated_lines))

# 모든 라벨 파일에 대해 함수 적용
for label_file in os.listdir(labels_dir):
    if label_file.endswith('.txt'):  # .txt 파일만 처리
        update_class_in_labels(os.path.join(labels_dir, label_file))

print("라벨 파일 클래스 ID 수정 완료.")
