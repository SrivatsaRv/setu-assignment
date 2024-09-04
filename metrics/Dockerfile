# Dockerfile for metrics container

FROM python:3.8-slim

# Install necessary Python dependencies
RUN pip install docker mysql-connector-python

# Copy the metrics collector script into the container
COPY metrics_collector.py /app/metrics_collector.py

# Command to run the script
CMD ["python", "/app/metrics_collector.py"]
