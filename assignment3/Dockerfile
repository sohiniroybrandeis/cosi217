FROM python:3.10.8-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install --default-timeout=100 -r requirements.txt

COPY . .

ENV FLASK_APP=run.py
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]