# Python Playwright Framework - Dockerfile
# Multi-stage build for efficient image size

FROM mcr.microsoft.com/playwright/python:v1.40.0-focal

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers (already installed in base image, but ensure dependencies)
RUN playwright install-deps

# Copy application code
COPY . .

# Create reports directory
RUN mkdir -p reports/screenshots reports/videos reports/logs reports/html-report

# Set default test environment
ENV TEST_ENV=qa \
    BROWSER=chrome \
    HEADLESS=true \
    WORKERS=auto

# Run tests by default
CMD ["pytest", "-v", "--html=reports/html-report/index.html", "--self-contained-html"]
