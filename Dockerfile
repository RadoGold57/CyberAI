FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY backend/ backend/
COPY core/ core/
COPY results/ results/

# Expose API port
EXPOSE 8000

# Default to running API
CMD ["python", "-m", "backend.server"]
