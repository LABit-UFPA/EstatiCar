# Use Python 3.12 as base image (matching pyproject.toml requirement)
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml .
COPY app/ ./app/

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Create necessary directories
RUN mkdir -p /app/app/uploads /app/app/build_assets/db /app/app/build_assets/json

# Expose Flet web server port and Flask download server port
EXPOSE 8080 8081

# Set the working directory to app folder
WORKDIR /app/app

# Set default environment variables
ENV QDRANT_URL=http://qdrant:6333
ENV OLLAMA_HOST=http://ollama:11434
ENV PYTHONUNBUFFERED=1

# Run the application directly
CMD ["python", "main.py"]
