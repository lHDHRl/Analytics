FROM python:3.13-slim

WORKDIR /app

COPY reqs.txt .

RUN pip install --no-cache-dir -r reqs.txt

COPY generator.py .

RUN useradd -m -u 1000 lox && \
    chown -R lox:lox /app

USER lox

CMD ["python3", "generator.py"]