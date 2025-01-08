# Base image
FROM python:3.10-slim

# Working directory 설정
WORKDIR /app

# 필요한 파일 복사
COPY requirements.txt /app/
COPY main.py /app/
COPY yolov5 /app/yolov5/
COPY weights /app/yolov5/weights/

# 필요한 패키지 설치
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 git
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# YOLOv5 requirements 설치
# RUN cd /app/yolov5 && pip install -qr requirements.txt

# 컨테이너 실행 명령어
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
