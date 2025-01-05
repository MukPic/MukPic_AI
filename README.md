# MuckPic - AI Model

## Docker
> - docker build -t test_yolov3(이미지 이름) .
> - docker images (이미지 확인)
> - docker run -p 8000:8000 test_yolov3(이미지 이름)

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

