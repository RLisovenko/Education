FROM python:3.12-slim

# Install Git required by dbt
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

# Install dbt and MinIO client
RUN pip install --no-cache-dir "dbt-postgres==1.11.0" "minio==7.2.18"

WORKDIR /usr/app