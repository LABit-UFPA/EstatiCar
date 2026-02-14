# Use Python 3.10 as base image
FROM python:3.10-slim

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

# Expose Flet web server port
EXPOSE 8000

# Set the working directory to app folder
WORKDIR /app/app

# Run the application in web mode
CMD ["python", "-m", "flet", "run", "--web", "--port", "8000", "main.py"]
