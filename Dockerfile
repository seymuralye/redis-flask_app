# Use an official Python image as the base image
FROM python:3.11-slim

# Set environment variables for PostgreSQL connection
ENV DB_NAME=my_database
ENV DB_USER=admin
ENV DB_PASSWORD=admin123
ENV DB_HOST=192.168.198.129
ENV DB_PORT=5432
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a working directory in the container
WORKDIR /app

# Copy the Python script and data file into the container
COPY insert_countries.py /app/
COPY countries_capitals.txt /app/

# Install Python dependencies
RUN pip install psycopg2 redis flask

# Command to run the script
CMD ["python", "insert_countries.py"]

