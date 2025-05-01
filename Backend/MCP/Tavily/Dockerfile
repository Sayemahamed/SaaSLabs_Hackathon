FROM python:3.12-slim

# Install necessary system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy your application code into the container
COPY . .

# Install Python dependencies using pip
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the Celery worker with logging
CMD ["python", "main.py"]
