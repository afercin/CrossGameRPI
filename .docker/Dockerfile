#sudo apt-get install qemu binfmt-support qemu-user-static
FROM --platform=linux/arm64/v8 ubuntu:22.04 

ARG DEBIAN_FRONTEND=noninteractive

# Global dependencies
RUN apt-get update && \
    apt-get install -y \
    git \
    debhelper \
    cmake

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

# Duckstation dependencies
RUN apt-get install -y \
    libsdl2-dev \
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
    ninja-build

#PPSSPP dependencies
RUN apt-get install -y \
    build-essential \
    libgl1-mesa-dev \
    libvulkan-dev \
    libspeexdsp-dev \
    libsamplerate0-dev