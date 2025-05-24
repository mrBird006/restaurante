FROM python:3.11-slim

# Install dependencies
RUN pip install --no-cache-dir -r "requirements.txt"

# Set working directory
WORKDIR /app

# Copy application code
COPY . .

# Expose FastAPI default port
EXPOSE 8000

# Start FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
