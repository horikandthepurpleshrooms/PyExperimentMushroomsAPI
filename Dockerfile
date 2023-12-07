# Use a Python base image
FROM python:3.8-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy only the necessary files
COPY app .

# Create a virtual environment and install dependencies
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the application
CMD ["venv/bin/python", "app.py"]
