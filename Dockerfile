# Use Python as base image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first (for faster builds)
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy all project files
COPY . .

# Create data directory
RUN mkdir -p data

# Expose port 5000
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]