FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    curl \
    git \
    python3 \
    python3-pip \
    python3-venv \
    awscli \
    && apt-get clean

RUN curl -fsSL https://get.docker.com | sh

RUN curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose \
    && chmod +x /usr/local/bin/docker-compose

RUN curl -fsSL https://cli.github.com/packages/githubcli-archive.key | tee /etc/apt/trusted.gpg.d/github.asc
RUN apt-add-repository https://cli.github.com/packages
RUN apt-get update && apt-get install gh

RUN pip3 install --no-cache-dir --upgrade pip setuptools wheel

WORKDIR /app

COPY . /app/

RUN pip3 install -r requirements.txt

USER root

ENTRYPOINT ["python3", "fetch_upload_s3_mongo.py"]
