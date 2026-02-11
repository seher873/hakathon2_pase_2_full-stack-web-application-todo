FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY phase3/backend/requirements.txt .
RUN pip install --no-cache-dir --timeout=300 -r requirements.txt

# Copy the application code
COPY . .

WORKDIR /app/phase3/backend

# Expose the port the app runs on
EXPOSE 9000

# The command will be overridden by docker-compose.dev-modified.yml
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]