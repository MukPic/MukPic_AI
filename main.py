from fastapi import FastAPI, HTTPException
import os
import requests
import subprocess
from pydantic import BaseModel

app = FastAPI()

# 클래스, 제외할 클래스
class_names = ['접시', '김치말이국수', '닭칼국수', '들깨칼국수', '떡라면', '라면', '막국수', '메밀국수', 
               '물냉면', '닭죽', '소고기버섯죽', '어죽', '잣죽', '전복죽', '참치죽', '채소죽', '팥죽', '바지락조개국', 
               '소고기무국', '소고기미역국', '순대국', '어묵국', '오징어국', '토란국', '탕국', '홍합미역국', '황태해장국', 
               '근대된장국', '미소된장국', '배추된장국', '뼈다귀해장국', '선지해장국', '콩나물국', '시금치된장국', '시래기된장국', 
               '쑥된장국', '아욱된장국', '우거지된장국', '우거지해장국', '우렁된장국', '갈비탕']
exclude_classes = ['접시']

yolo_dir = "/app/yolov5"
weights_path = os.path.join(yolo_dir, "weights", "best.pt")
output_dir = "/app/run_image"
labels_dir = os.path.join(output_dir, "labels")

# 이미지 URL 입력 데이터 구조 정의
class ImageURL(BaseModel):
    url: str

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