# Use the official Python image as the base
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files to the container
COPY . .

# Expose the port (if your application needs it, e.g., Flask or FastAPI)
# Not needed for your script with GUI.

# Default command to run the project
CMD ["python", "main.py"]
