FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Environment variables (can be overridden)
ENV ALLOWED_ORIGINS="*"
ENV USE_JINA_FALLBACK="1"
ENV PORT=5000

EXPOSE 5000

# Use Gunicorn for production
CMD gunicorn -w 2 -k gthread -t 60 -b 0.0.0.0:$PORT wsgi:application
