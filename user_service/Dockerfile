# Base image
FROM python:3.9-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Expose the port
EXPOSE 8000

# Run the Django server
RUN pip install gunicorn

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "user_service.wsgi:application"]

