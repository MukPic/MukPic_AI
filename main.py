from fastapi import FastAPI, HTTPException
import os
import requests
import subprocess
from pydantic import BaseModel

app = FastAPI()

# 클래스, 제외할 클래스
class_names = ['접시', '잡곡밥', '보리밥', '흑미밥', '김치볶음밥', '볶음밥', '비빔밥', '새우볶음밥', '알밥',
 '육회비빔밥', '불고기덮밥', '소고기국밥', '잡채밥', '제육덮밥', '순대국밥', '전주콩나물국밥', '해물덮밥', '돼지국밥', '유부초밥',
  '김밥', '김치말이국수', '닭칼국수', '들깨칼국수', '라면', '막국수', '메밀국수', '물냉면', '비빔국수', '비빔냉면', '수제비', '자장면',
   '잔치국수', '짬뽕', '쫄면', '콩국수', '해물칼국수', '떡국', '짜장라면', '만둣국', '닭죽', '소고기버섯죽', '잣죽', '전복죽', '팥죽',
    '호박죽', '미역국', '토란국']
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