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

# Copy seed script
COPY seed_data.py .

CMD ["python3", "seed_data.py"]
