FROM python:3.12-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt requirements-api.txt ./

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements-api.txt

# Copy application files
COPY api.py config.yaml logger.py validators.py model_loader.py performance.py ./
COPY pipeline.py custom_metrics.py multilingual_support.py ./

# Create directories
RUN mkdir -p input output logs

# Expose port
EXPOSE 8000

# Start command
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]