FROM python:3.10-slim

WORKDIR /app

ENV PYHTONUNBUFFERED=1
RUN apt-get update \
    && apt-get -y install tesseract-ocr \   
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000

ENV PYTHONUNBUFFERED 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
