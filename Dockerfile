FROM python:latest

WORKDIR /app/

COPY ./main.py /app/

RUN pip install pykrx matplotlib uvicorn fastapi

CMD uvicorn --host=0.0.0.0 --port 8000 main:app
