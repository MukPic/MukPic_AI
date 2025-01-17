from fastapi import FastAPI, HTTPException
import os
import requests
import subprocess
from pydantic import BaseModel

app = FastAPI()

# 클래스, 제외할 클래스
class_names = ['접시', '잡곡밥', '보리밥', '흑미밥', '김치볶음밥', '볶음밥', '비빔밥', '새우볶음밥', '알밥', \
    '육회비빔밥', '불고기덮밥', '소고기국밥', '잡채밥', '제육덮밥', '순대국밥', '콩나물국밥, 콩나물국', '해물덮밥', '돼지국밥', \
        '유부초밥', '김밥', '김치말이국수', '닭칼국수', '들깨칼국수', '라면', '막국수', '메밀국수', '물냉면', '비빔국수', '비빔냉면', \
        '수제비', '자장면', '잔치국수', '짬뽕', '쫄면', '콩국수', '해물칼국수', '떡국', '만둣국', '전복죽', '팥죽', '호박죽', '미역국', \
            '토란국', '황태국', '배추된장국', '선지해장국', '시금치된장국', '우거지된장국', '우거지해장국', '갈비탕', '감자탕', '매운탕', '닭볶음탕', \
                '삼계탕', '설렁탕', '알탕', '연포탕', '추어탕', '육개장', '뼈해장국', '부대찌개', '된장찌개', '청국장찌개', '곱창전골', '돼지고기김치찌개', \
                    '순두부찌개', '대구찜', '아귀찜', '해물찜', '돼지고기수육', '찜닭', '족발', '달걀찜', '닭갈비', '닭꼬치', '갈비', '떡갈비', \
                        '불고기', '소곱창구이', '훈제오리', '삼치구이', '동태전', '해물파전', '동그랑땡', '육전', '감자전', '김치전', '녹두빈대떡', \
                            '배추전', '부추전', '파전', '호박전', '달걀말이', '낙지볶음', '멸치볶음', '어묵볶음', '오징어볶음', '오징어채볶음', \
                                '주꾸미볶음', '감자볶음', '두부김치', '호박볶음', '돼지고기볶음', '돼지껍데기볶음', '소세지볶음', '순대볶음', \
                                    '오리불고기', '오삼불고기', '떡볶이', '라볶이', '갈치조림', '고등어조림', '꽁치조림', '감자조림', \
                                        '쥐포튀김', '닭강정', '모래집튀김', '양념치킨', '고구마맛탕', '도토리묵', '무생채', '무말랭이', \
                                            '파무침', '상추겉절이', '청포묵무침', '가지나물', '고사리나물', '숙주나물', '시금치나물', \
                                                '북어채무침', '쥐치채', '홍어무침', '골뱅이국수무침', '잡채', '갓김치', '깍두기', \
                                                    '동치미', '배추김치', '백김치', '부추김치', '열무김치', '오이소박이', '총각김치', \
                                                        '파김치', '간장게장', '깻잎장아찌', '양념게장', '오징어젓갈', '육회', '육사시미', \
                                                            '가래떡', '경단', '꿀떡', '시루떡', '메밀전병', '무지개떡', '백설기', '송편', \
                                                                '수수팥떡', '쑥떡', '약식', '인절미', '절편', '증편', '찹쌀떡', '매작과', \
                                                                    '다식', '약과', '유과', '산자', '깨강정']
exclude_classes = ['접시']

yolo_dir = "/app/yolov5"
weights_path = os.path.join(yolo_dir, "weights", "best.pt")
output_dir = "/app/run_image"
labels_dir = os.path.join(output_dir, "labels")

# 이미지 URL 입력 데이터 구조 정의
class ImageURL(BaseModel):
    url: str


# 루트 경로 추가
@app.get("/")
def root():
    return {
        "message": "Welcome to MukPicAI API!",
        "endpoints": {
            "/health": "Check the health of the API",
            "/predict/": "Send a POST request with an image URL to get a prediction"
        }
    }


# 헬스 체크 엔드포인트 추가
@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/predict/")
async def predict(data: ImageURL):
    image_name = data.url.split('/')[-1].split('.')[0]
    input_image_path = f"{output_dir}/{image_name}.jpg"
    label_file = os.path.join(labels_dir, f"{image_name}.txt")

    # 디렉토리 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # URL 이미지 다운로드
    try:
        response = requests.get(data.url, stream=True)
        response.raise_for_status()
        with open(input_image_path, "wb") as buffer:
            buffer.write(response.content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"이미지 다운로드 실패: {e}")

    # YOLOv3 모델 예측 실행
    detect_command = [
        "python", os.path.join(yolo_dir, "detect.py"),
        "--source", input_image_path,
        "--weights", weights_path,
        "--conf", "0.2",
        "--project", output_dir,
        "--name", "",
        "--exist-ok",
        "--line-thickness", "2",
        "--save-txt",
        "--save-conf"
    ]
    result = subprocess.run(detect_command, cwd=yolo_dir, capture_output=True, text=True)
    if result.returncode != 0:
        raise HTTPException(status_code=500, detail=f"실행 실패: {result.stderr}")

    best_class_name = None
    max_confidence = 0

    if os.path.exists(label_file):
        with open(label_file, 'r') as file:
            results = file.readlines()

        for line in results:
            class_id, confidence = int(line.split()[0]), float(line.split()[1])
            class_name = class_names[class_id]

            if class_name not in exclude_classes and confidence > max_confidence:
                max_confidence = confidence
                best_class_name = class_name

    # 임시 파일 삭제
    try:
        if os.path.exists(input_image_path):
            os.remove(input_image_path)
        if os.path.exists(label_file):
            os.remove(label_file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"임시 파일 삭제 중 오류 발생: {e}")

    # 결과 전송
    if best_class_name:
        return {"result": best_class_name}
    else:
        return {"message": "제외되지 않은 클래스가 없습니다."}