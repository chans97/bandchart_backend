## What is it

- bandchart 를 서비스를 구현하기 위한 백엔드 서버입니다.

## How to Start

```
uvicorn main:app --reload
```

## packages

- pipenv
- requests
- pykrx
- fastapi
- matplotlib
- uvicorn


## docker 
```
docker build -t chans97/bandchart_backend:0.1 .
docker run --rm -p 8080:8000 chans97/bandchart_backend:0.1
```

amd64 
```
docker build --platform linux/amd64 -t chans97/bandchart_backend_amd64 .
```

arm64
