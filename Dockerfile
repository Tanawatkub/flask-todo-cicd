# ---------- Build stage ----------
    FROM python:3.11-slim AS builder

    # Set working directory
    WORKDIR /app
    
    # Install build dependencies
    RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        postgresql-client \
        && rm -rf /var/lib/apt/lists/*
    
    # Copy requirements first (for Docker layer caching)
    COPY requirements.txt .
    
    # Install dependencies into local user path
    RUN pip install --upgrade pip && \
        pip install --no-cache-dir --user -r requirements.txt
    
    
    # ---------- Runtime stage ----------
    FROM python:3.11-slim
    
    # Create non-root user
    RUN useradd -m -u 1000 appuser
    
    # Set working directory
    WORKDIR /app
    
    # Install minimal runtime dependencies
    RUN apt-get update && apt-get install -y --no-install-recommends \
        postgresql-client \
        && rm -rf /var/lib/apt/lists/*
    
    # Copy installed packages from builder stage
    COPY --from=builder /root/.local /home/appuser/.local
    
    # Copy application code
    COPY --chown=appuser:appuser . .
    
    # Environment variables
    ENV PATH=/home/appuser/.local/bin:$PATH \
        PYTHONUNBUFFERED=1 \
        FLASK_APP=run.py \
        PORT=5000
    
    # Switch to non-root user
    USER appuser
    
    # Expose port
    EXPOSE 5000
    
    # Healthcheck
    HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
      CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/api/health')" || exit 1
    
    # Start app using Gunicorn
    CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "run:app"]

    