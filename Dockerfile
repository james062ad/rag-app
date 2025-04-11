# Use an official Python base image
FROM python:3.11-slim

# Set environment variables
ENV POETRY_VERSION=1.7.1
ENV PATH="/root/.local/bin:$PATH"

# Install system dependencies
RUN apt-get update \
 && apt-get install -y curl build-essential git \
 && apt-get clean

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set the working directory
WORKDIR /app

# Copy only Poetry files to cache deps first
COPY pyproject.toml poetry.lock ./

# Install dependencies + Supabase
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi \
 && poetry add supabase

# Copy the rest of the application code
COPY . .

# Expose port for FastAPI
EXPOSE 8000

# Start the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
