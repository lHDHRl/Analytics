FROM python:3.13-slim AS builder

WORKDIR /app

COPY reqs.txt .

RUN pip install --no-cache-dir uv && uv pip install --no-cache-dir --target /install -r reqs.txt

FROM gcr.io/distroless/python3-debian12

WORKDIR /app

COPY --from=builder /install /app
COPY generator.py .
ENV PYTHONPATH=/app

CMD ["python3","generator.py"]