# Use Python base image
FROM python:3.9

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django app
COPY . .

EXPOSE 3334

# Run Gunicorn for production
CMD ["gunicorn", "--workers=2", "--timeout=120", "--preload", "backend.wsgi:application", "--bind", "0.0.0.0:3334"]
