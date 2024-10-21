import os
import json

# 클래스 매핑 (숫자 -> 클래스)
class_mapping = {
    '고철류': '0',        # 고철류
    '캔류': '0',          # 캔류는 고철류로 통합
    '비닐류': '1',        # 비닐
    '스티로폼류': '2',    # 스티로폼
    '유리병류': '3',      # 유리병
    '종이류': '4',        # 종이
    '페트병류': '5',      # 페트병은 플라스틱류로 분류
    '플라스틱류': '5'     # 플라스틱류
}

# JSON 파일 경로
json_dir = 'data/'

# JSON 파일 수정 함수
def update_class_in_json(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # CLASS 값을 매핑된 번호로 변경
    for bounding in data.get("Bounding", []):
        class_name = bounding.get("CLASS")
        if class_name in class_mapping:
            bounding["CLASS"] = class_mapping[class_name]
    
    # 수정된 내용을 다시 파일에 저장
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 모든 JSON 파일에 대해 함수 적용
for json_file in os.listdir(json_dir):
    if json_file.endswith('.Json'):
        update_class_in_json(os.path.join(json_dir, json_file))
