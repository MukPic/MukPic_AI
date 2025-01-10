# Base image
FROM python:3.10-slim

# Working directory 설정
WORKDIR /app

# 필요한 파일 복사
COPY requirements.txt /app/

# 패키지 설치
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 git \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# YOLOv5 requirements 설치
# COPY yolov5/requirements.txt /app/yolov5/
# RUN pip install --no-cache-dir -r /app/yolov5/requirements.txt

# 나머지 파일 복사
COPY main.py /app/
COPY yolov5 /app/yolov5/
COPY weights /app/yolov5/weights/

# 권한 설정
RUN chmod -R 755 /app

# 컨테이너 실행 명령어
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
