FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY maker.py .
COPY script_to_api.py .
COPY script_to_transc.py .

EXPOSE 3001

CMD ["python", "script_to_api.py"]
