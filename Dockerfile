FROM python:3.11

LABEL maintainer="dl.ruled@gmail.com"

RUN apt-get update && \
    apt-get install -y libpq-dev python3-dev && \
    rm -rf /var/lib/apt/lists/*

ENV ADMIN="dimmentor"

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000 8089

CMD ["locust", "-f", "locustfile.py", "--host=http://dimmentor_psql:5432"]