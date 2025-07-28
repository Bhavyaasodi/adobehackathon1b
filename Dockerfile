# Use slim Python base image
FROM --platform=linux/amd64 python:3.10-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app folder
COPY app/ ./app/

# Set default command
CMD ["python", "app/main.py"]
