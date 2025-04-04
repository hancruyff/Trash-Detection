# self-developed
import data_preprocessing

# python-library
import os


if __name__ == '__main__':
    # 데이터셋 경로 설정
    dataset_path = '생활 폐기물 이미지'

    # 데이터 저장 경로 설정
    data_path = 'data/'
    backup_path = 'backup'

    # 클래스 정보 딕셔너리
    classes = {'0': '고철류/캔류', '1': '비닐류', '2': '스티로폼류', '3': '유리병류', '4': '종이류', '5': '플라스틱류'}
    classes_translation = {'고철류/캔류': 'metal', '비닐류': 'vinyl', '스티로폼류': 'styrofoam', '유리병류': 'glass', '종이류': 'paper', '플라스틱류': 'plastic'}
    classes_to_code = {'metal': '0', 'vinyl': '1', 'styrofoam': '2', 'glass': '3', 'paper': '4', 'plastic': '5'}
    # vinyl, glass, paper, can, PET, plastic

    # 이미지 속성 번역 딕셔너리
    imgattr_translation = {
        '주간': 'day',
        '야간': 'night',
        '실내': 'indoor',
        '실외': 'outdoor',
        '스튜디오': 'studio',
        '고철류/캔류':'metal',
        '비닐류': 'vinyl',
        '스티로폼류':'styrofoam',
        '유리병류': 'glass',
        '종이류': 'paper',
        '플라스틱류': 'plastic'
    }

    # 필요 이미지 속성 리스트
    imgattr_headers = ['resolution', 'iso', 'daynight', 'place', 'obj_class', 'obj_color', 'x_min', 'y_min', 'x_max', 'y_max']

    # 확장자
    exts = {
        'image_ext': ['jpg', 'png'],
        'json_ext': ['json', 'Json']
    }

    # 이미지 사이즈
    img_size = (640, 640)

    # 오류 이미지
    error_imgs = ['22_X006_C013_1015_0']

    # 백업 디렉터리가 없을 경우, 생성
    if not os.path.isdir(backup_path):
        os.mkdir(backup_path)
    # 백업 파일
    #data_preprocessing.copy_files(data_path, backup_path, exts)
    #print("백업 파일 저장 완료")
    # # 라벨링 데이터 내에 필요없는 클래스의 자료들 삭제
    # data_preprocessing.folders_by_classes(f'{dataset_path}/Training/Training_라벨링데이터')
    # data_preprocessing.folders_by_classes(f'{dataset_path}/Validation/[V라벨링]라벨링데이터')

    # # 전체 파일 이동 // dataset_path -> data_path
    # data_preprocessing.gather_data(dataset_path, data_path, exts)

    # 필요없는 데이터 제거
    data_preprocessing.remove_unmatched(data_path, exts, error_imgs)
    print("필요없는 데이터 제거 완료")

    # 이미지 속성 값 추출
    data_preprocessing.extract_imgattr(data_path, imgattr_translation, imgattr_headers)
    print("csv파일 생성 완료")

    # 백업 파일
    #data_preprocessing.copy_files(data_path, backup_path, exts)
    #print("백업 파일 저장 완료")

    # 서브 디렉터리가 없을 경우, 생성
    if not os.path.isdir(os.path.join(data_path, 'train')):
        data_preprocessing.create_folders(data_path)

    # 데이터 전처리
    data_preprocessing.data_preprocess(data_path, classes_to_code, img_size, exts)
    print('데이터 전처리 완료')
    
    # 파일 분배
    data_preprocessing.distribute_files(data_path, exts)
    print("파일 분배 완료")
