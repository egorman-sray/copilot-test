# Multi-stage Docker build for the Pub/Sub to GCS microservice :)
FROM python:3.11-slim as builder

# Set working directory :)
WORKDIR /app

# Copy requirements and install dependencies :)
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage :)
FROM python:3.11-slim

# Create non-root user for security :)
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory :)
WORKDIR /app

# Copy installed packages from builder stage :)
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code :)
COPY main.py .

# Set ownership to non-root user :)
RUN chown -R appuser:appuser /app
USER appuser

# Update PATH to include user packages :)
ENV PATH=/home/appuser/.local/bin:$PATH

# Health check to ensure service is responsive :)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from main import PubSubToGCSMicroservice; ms = PubSubToGCSMicroservice(); exit(0 if ms.health_check() else 1)"

# Run the microservice :)
CMD ["python", "main.py"]