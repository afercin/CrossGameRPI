#sudo apt-get install qemu binfmt-support qemu-user-static
ARG IMAGE_ARCH=linux/arm/v7
#ARG IMAGE_ARCH=linux/arm64/v8
ARG IMAGE_TAG=buster
FROM --platform=$IMAGE_ARCH debian:$IMAGE_TAG

ARG DEBIAN_FRONTEND=noninteractive

# Global dependencies
RUN apt-get update && \
    apt-get install -y debhelper