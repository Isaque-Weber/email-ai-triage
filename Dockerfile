FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (build-essential needed for some python packages like pandas/numpy sometimes)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port (Dockploy/Railway usually map internal port to 80 or similar)
EXPOSE 80

# Run the application
# --host 0.0.0.0 makes it accessible outside the container
# --port 80 to match standard web port
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]