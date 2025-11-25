# MENA Bias Evaluation Pipeline - Docker Image
# Python 3.12 - Lightweight version without PyTorch

FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy files
COPY requirements.txt .
COPY pipeline.py .

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install only essential dependencies (no PyTorch for demo)
RUN pip install --no-cache-dir \
    numpy pandas scipy \
    matplotlib seaborn plotly \
    reportlab Pillow pypdf \
    openpyxl python-dateutil pytz \
    packaging requests urllib3 certifi typing-extensions \
    cloudpickle tqdm slicer

# Create directories
RUN mkdir -p input output

# Environment variables
ENV PYTHONUNBUFFERED=1

# Run pipeline
CMD ["python", "pipeline.py"]