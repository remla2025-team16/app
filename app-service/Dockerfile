FROM python:3.10-slim

WORKDIR /app

COPY ./src /app
COPY requirements.txt /app

RUN apt-get update && apt-get install -y git && apt-get clean

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

ENV MODEL_SERVICE_URL=http://model-service:5010

CMD ["python", "app.py"]