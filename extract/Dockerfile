FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY .env .
COPY maker.py .
COPY script_to_api.py .
COPY script_to_extract.py .

EXPOSE 3000

CMD ["sh", "-c", "python3 maker.py && tail -f /dev/null"]
