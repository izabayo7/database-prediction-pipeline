FROM python:3.10-slim

WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt /code/task_2_api/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /code/task_2_api/requirements.txt

# Copy application code into task_2_api package
COPY . /code/task_2_api/

# Expose port
EXPOSE 8000

# Run the FastAPI application from parent directory so relative imports work
CMD ["uvicorn", "task_2_api.main:app", "--host", "0.0.0.0", "--port", "8000"]