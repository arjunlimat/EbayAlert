# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory to the container
COPY . .

# Expose port 8080 for the Django application
EXPOSE 8080

# Run the Django development server
CMD ["bash", "-c", "python manage.py runserver 0.0.0.0:8080"]

