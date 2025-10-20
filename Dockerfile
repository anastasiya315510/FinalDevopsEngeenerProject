# Use Python base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose the port
EXPOSE 8000

# Run Gunicorn with 4 workers
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
