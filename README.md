# MuckPic - AI Model
# 중요
> - 모델 변경으로 모델 설치 코드 변경
> - !git clone https://github.com/ultralytics/yolov5
> - !cd yolov5;pip install -qr requirements.txt

## Docker
> - docker build -t test_yolov5(이미지 이름) .
> - docker images (이미지 확인)
> - docker run -p 8000:8000 test_yolov5(이미지 이름)

## local 사용
> - swagger UI: http://localhost:8000/docs#/
> - 엔드포인트 URL: http://localhost:8000/predict/
> - 요청 헤더: Content-Type: application/json
> - 요청 본문: {"url": "https://example.com/path-to-image.jpg"}
> - 응답:
```
{
    "result": "쌀밥"
}
```

