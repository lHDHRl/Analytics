FROM python:3.12-slim

WORKDIR /app
COPY reqs.txt .
RUN pip install --no-cache-dir -r reqs.txt
COPY generator.py .

CMD ["python3", "generator.py"]