# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Copy requirements.txt to the container
COPY requirements.txt .


# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project to the container
COPY . .

# Run database migrations
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py collectstatic --no-input

# Expose the port the app runs on
EXPOSE 8000

# Start the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]