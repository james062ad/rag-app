# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y curl

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy dependency files first
COPY pyproject.toml poetry.lock ./

# Install project dependencies
RUN poetry install --no-interaction

# Copy the rest of your app
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run the app with Uvicorn
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
