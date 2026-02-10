FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential \
    python3 \
    python3-pip \
    tcpdump \
    netcat-openbsd \
    libcap2-bin \
    iproute2 \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install scapy

WORKDIR /app

COPY . /app
