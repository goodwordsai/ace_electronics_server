FROM python:3.13-slim

WORKDIR /app

RUN pip install fastapi uvicorn
RUN pip install --no-cache-dir uv
RUN uv pip install --system "sentry-sdk[fastapi]"

COPY main.py .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
