# Start from official Python slim image (smaller than full image)
FROM python:3.12.1-slim

# Prevents Python from buffering stdout/stderr (logs appear immediately)
# Prevents Python from writing .pyc files (not needed in containers)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set working directory for all subsequent commands
WORKDIR /app

# Install system dependencies needed for Python packages
# build-essential: for packages that need compilation
# curl: for downloading Poetry installer
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry package manager
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Copy only dependency files first (Docker layer caching)
# This layer is cached unless dependencies change
COPY pyproject.toml poetry.lock* ./

# Install Python dependencies from Poetry
# --no-root: don't install the project itself yet
# --only main: skip dev dependencies for production
# virtualenvs.create false: install globally in container
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root --only main

# Copy application source code
# Done last so code changes don't invalidate dependency cache
COPY src/ ./src/

# Port your app will listen on (change if needed)
EXPOSE 8000

# Command to run when container starts
CMD ["python", "src/app/main.py"]

# For FastAPI apps, use this instead:
# CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
