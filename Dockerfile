FROM ubuntu:18.04

# Dependencias
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    qt5-default \
    sudo \
    libprotobuf-dev \
    protobuf-compiler \
    python \ 
    python3-pip \
    && apt-get clean 

#WORKDIR red5v5
COPY requirements.txt .
RUN pip3 install -r requirements.txt

