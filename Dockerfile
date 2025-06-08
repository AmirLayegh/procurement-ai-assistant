# Use Python 3.11 slim image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY pyproject.toml ./
COPY uv.lock* ./

# Install uv and dependencies
RUN pip install uv
RUN uv sync --frozen

# Copy application code
COPY . .

# Create data directory and copy CSV
RUN mkdir -p data/csv
COPY data/csv/products_enriched.csv data/csv/

# Expose port (Cloud Run uses PORT environment variable)
EXPOSE 8080

# Set environment variables
ENV PORT=8080
ENV PYTHONPATH=/app

# Run the application with our custom server module
CMD ["uv", "run", "python", "-m", "superlinked.server"]