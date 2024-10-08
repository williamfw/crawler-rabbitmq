FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY script_to_api.py .
COPY script_to_print.py .

EXPOSE 3001

CMD ["python", "script_to_api.py"]
