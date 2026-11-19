FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for OpenCV and image processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY webapp/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY webapp /app/webapp

ENV PORT=8000
ENV MODEL_PATH=/app/webapp/model/best.pt
EXPOSE 8000

CMD ["sh", "-c", "uvicorn main:app --app-dir webapp --host 0.0.0.0 --port ${PORT}"]
