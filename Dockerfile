FROM ubuntu:22.04

# Dependencias
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    qtbase5-dev \
    qt5-qmake \
    sudo \
    libprotobuf-dev \
    protobuf-compiler \
    python3.10 \
    python3-pip \
    && apt-get clean 

#WORKDIR red5v5
COPY requirements.txt .
RUN pip3 install -r requirements.txt

