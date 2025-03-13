FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir locust


CMD ["locust", "-f", "locustfile.py", "--host=http://127.0.0.1:8000"]