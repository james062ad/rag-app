# Use official Python base image
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Install dependencies
COPY pyproject.toml poetry.lock ./
RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    export PATH="/root/.local/bin:$PATH" && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Copy rest of the app
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run the FastAPI app
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
