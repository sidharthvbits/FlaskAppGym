
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /FlaskAppGym

# Copy requirements file first (for better layer caching)
COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    build-essential cmake pkg-config libdbus-1-dev libdbus-glib-1-dev

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port your app runs on
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the application
CMD ["flask", "run"]
