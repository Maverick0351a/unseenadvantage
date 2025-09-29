# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8088

WORKDIR /app

# System deps kept minimal (no compilers) to stay slim
# If you later need OS libs (e.g., libcblas), apt-get install here.

# Copy dependency descriptors and source for installation
COPY pyproject.toml ./
COPY README.md ./
COPY src ./src

# Install with 'ui' extra to get FastAPI/uvicorn/Jinja2
RUN pip install --upgrade pip && \
    pip install --no-cache-dir ".[ui]" || \
    (pip install --no-cache-dir build && python -m build && pip install --no-cache-dir dist/*.whl)

# Copy remaining project assets
COPY scripts ./scripts
COPY examples ./examples

# Create reports dir inside the container (mounted by compose)
RUN mkdir -p /app/reports

EXPOSE ${PORT}

ENV PYTHONPATH="/app/src"

# Default: run the API (override in compose if needed)
CMD ["python", "-m", "uvicorn", "unseen_advantage.api.server:app", "--host", "0.0.0.0", "--port", "8088"]
