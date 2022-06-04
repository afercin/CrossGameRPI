#sudo apt-get install qemu binfmt-support qemu-user-static
FROM --platform=linux/arm64/v8 ubuntu:22.04 

ARG DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt install -q -y --yes -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" \
    git \
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
    ninja-build \
    build-essential \
    cmake \
    libgl1-mesa-dev \
    libvulkan-dev \
    libspeexdsp-dev \
    libsamplerate0-dev \
    libboost-filesystem-dev
