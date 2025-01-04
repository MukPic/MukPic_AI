# MuckPic - AI Model

## Docker
> - docker build -t test_yolov3(이미지 이름) .
> - docker images (이미지 확인)
> - docker run -p 8000:8000 test_yolov3

## local 사용
> - swagger UI: http://localhost:8000/docs#/
> - http://localhost:8000/predict/ -> 엔드포인트 URL
> - Content-Type: application/json -> 요청 헤더
> - {"url": "https://example.com/path-to-image.jpg"} -> 요청 본문
> - 응답
```
{
  "args": {},
  "data": {
    "result": "보리밥"
  },
  "files": {},
  "form": {},
  "headers": {
    "host": "postman-echo.com",
    "x-request-start": "t1735952941.014",
    "connection": "close",
    "content-length": "32",
    "x-forwarded-proto": "https",
    "x-forwarded-port": "443",
    "x-amzn-trace-id": "Root=1-67788a2d-26393adb63e9a576138aee4f",
    "user-agent": "python-requests/2.32.3",
    "accept-encoding": "gzip, deflate",
    "accept": "*/*",
    "content-type": "application/json"
  },
  "json": {
    "result": "보리밥"
  },
  "url": "https://postman-echo.com/post"
}
```

