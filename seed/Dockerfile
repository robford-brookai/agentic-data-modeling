FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for postgres and compilation
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all seed scripts
COPY scripts/config.py .
COPY scripts/s3.py .
COPY scripts/metabase.py .
COPY scripts/metabase.sql .

# Default command (can be overridden)
CMD ["python3", "s3.py"]
