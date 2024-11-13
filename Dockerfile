# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /eterio-api

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the app code to the container
COPY . .

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Set environment variable for the port (Cloud Run uses 8080)
ENV PORT 8080

# Command to run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]