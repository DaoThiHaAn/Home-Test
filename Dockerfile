# Use "slim" variant of Python image to reduce image size
FROM python:3.12-slim

# Avoid writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure Python logs are printed directly to the console (stdout/stderr) immediately without being buffered
ENV PYTHONUNBUFFERED=1

# Set the default working directory inside the Container to /app
WORKDIR /app

# Utilize Docker Layer Caching
# Only copy the requirements file first, if this file hasn't changed, subsequent builds will skip the pip install step
COPY requirements.txt .

# Install dependencies and remove cache immediately to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code from your machine into the /app directory of the Container
COPY . .

# Main entry point for the Container.
# When docker run is called, the container will execute this command, run main.py, and then exit with code 0.
CMD ["python", "main.py"]