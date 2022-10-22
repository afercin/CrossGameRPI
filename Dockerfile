#sudo apt-get install qemu binfmt-support qemu-user-static
ARG IMAGE_ARCH=linux/arm/v7
#ARG IMAGE_ARCH=linux/arm64/v8
ARG IMAGE_TAG=buster
FROM --platform=$IMAGE_ARCH debian:$IMAGE_TAG

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get -y --force-yes install gcc g++ \
    cmake \
    wget \
    dpkg-dev \
    debhelper \
    rsync \
    git \
    python3-pip \
    zlib1g-dev \
    libudev1 \
    libudev-dev

RUN rm -rf /var/lib/apt/lists/* \
    && cd /tmp \
    && wget https://github.com/neurobin/shc/archive/refs/tags/4.0.1.tar.gz \
    && tar -xvzf 4.0.1.tar.gz \
    && cd shc-4.0.1 \
    && ./configure \
    && make \
    && make install

RUN apt-get update \
    && apt -y --force-yes install python3-tk \
    python3-flask \
    libjpeg-dev \
    zlib1g-dev

COPY requeriments.txt requeriments.txt

RUN pip3 install -U -r requeriments.txt