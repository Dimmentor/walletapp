FROM python:3.11
LABEL maintainer="dl.ruled@gmail.com"
ENV ADMIN="dimmentor"
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000 8089

CMD ["locust", "-f", "locustfile.py", "--host=http://127.0.0.1:8000"]