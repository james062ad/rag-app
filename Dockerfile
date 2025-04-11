# Use official Python base image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl build-essential

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Copy pyproject files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi

# Copy app files
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
