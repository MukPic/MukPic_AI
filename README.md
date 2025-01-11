# MuckPic - AI Model
# 중요
> - 모델 변경으로 모델 설치 코드 변경
> - !git clone https://github.com/ultralytics/yolov5
> - !cd yolov5;pip install -qr requirements.txt
> - 예측 음식: ['잡곡밥', '보리밥', '흑미밥', '김치볶음밥', '볶음밥', '비빔밥', '새우볶음밥', '알밥', '육회비빔밥', '불고기덮밥', '소고기국밥', '잡채밥', '제육덮밥', '순대국밥', '전주콩나물국밥', '해물덮밥', '돼지국밥', '유부초밥', '김밥', '김치말이국수', '닭칼국수', '들깨칼국수', '라면', '막국수',
> - '메밀국수', '물냉면', '비빔국수', '비빔냉면', '수제비', '자장면', '잔치국수', '짬뽕', '쫄면', '콩국수', '해물칼국수', '떡국', '짜장라면', '만둣국', '닭죽', '소고기버섯죽', '잣죽', '전복죽', '팥죽', '호박죽', '미역국', '토란국']

# aws 배포
> - POST: https://mukpicai.duckdns.org/predict/
```
{
  "url": "https://example.com/image.jpg"
}
```

## local 사용
> - swagger UI: http://localhost:8000/docs#/
> - 엔드포인트 URL: http://localhost:8000/predict/
> - 요청 헤더: Content-Type: application/json
> - 요청 본문: {"url": "https://example.com/path-to-image.jpg"}

## Docker
> - docker build -t test_yolov5(이미지 이름) .
> - docker images (이미지 확인)
> - docker run -p 8000:8000 test_yolov5(이미지 이름)

> - 응답:
```
{
    "result": "쌀밥"
}
```
