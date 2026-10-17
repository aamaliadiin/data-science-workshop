# Build dari root repo:  docker build -f api/Dockerfile -t workshop-api .
FROM python:3.11-slim
WORKDIR /app/api
COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY data /app/data
COPY api /app/api
EXPOSE 8000
CMD ["uvicorn", "mock_api:app", "--host", "0.0.0.0", "--port", "8000"]
