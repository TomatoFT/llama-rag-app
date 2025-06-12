FROM python:3.10-slim

WORKDIR /app

# Install system dependencies including git and build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create necessary directories
RUN mkdir -p models/llama-2-7b uploads

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "api_main.py"] 