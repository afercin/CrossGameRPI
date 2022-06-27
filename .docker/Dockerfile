#sudo apt-get install qemu binfmt-support qemu-user-static
FROM --platform=linux/arm64/v8 ubuntu:20.04 

ARG DEBIAN_FRONTEND=noninteractive

# Global dependencies
RUN apt-get update && \
    apt-get install -y \
    git \
    debhelper

RUN apt-get install -q -y --yes -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" \
    libxrandr-dev \
    pkg-config \
    qtbase5-dev \
    qtbase5-private-dev \
    qtbase5-dev-tools \
    qttools5-dev \
    libevdev-dev \
    libwayland-dev \
    libwayland-egl-backend-dev \
    extra-cmake-modules \
    libcurl4-gnutls-dev \
    libgbm-dev \
    libdrm-dev \
    ninja-build \
    build-essential \
    cmake \
    libgl1-mesa-dev \
    libvulkan-dev \
    libspeexdsp-dev \
    libsamplerate0-dev

# Mupen64plus dependencies
RUN apt-get install -y \
    libpng-dev \
    libfreetype-dev \
    nasm \
    build-essential \
    libz-dev \
    libsdl2-dev \
    libboost-dev \
    libboost-filesystem-dev