FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV SERVER_HOST=0.0.0.0
ENV SERVER_PORT=5555

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY FlaskWebProject1 ./FlaskWebProject1
COPY runserver.py .

EXPOSE 5555

CMD ["python", "runserver.py"]
