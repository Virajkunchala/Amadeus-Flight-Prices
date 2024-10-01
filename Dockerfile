# Use the official Python image
FROM python:3.11-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire project
COPY . /app/

COPY .env ./


# Expose the port the app runs on
EXPOSE 8000

# Run migrations and start the server (adjust the command as needed)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]



