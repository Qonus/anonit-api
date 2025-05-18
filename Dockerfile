FROM python:3.11-slim

WORKDIR /app

ENV PYHTONUNBUFFERED=1
RUN apt-get update \
    && apt-get -y install tesseract-ocr \   
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 10000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]