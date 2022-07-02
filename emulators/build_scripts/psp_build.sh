#!/bin/bash

set -e

[[ ! -f /opt/common.sh ]] && echo "[ERROR] No se encuentra el script common" && exit 1
. /opt/common.sh

## Variables
CODE_FOLDER="${GIT_FOLDER}/psp"
BUILD_FOLDER="${CODE_FOLDER}/build"

GIT_REPOSITORY="https://github.com/hrydgard/ppsspp.git"
GIT_ARGS="--recurse-submodules"

## Code

echo "##########################################################################"
echo "#################### Building PSP emulator (PPSSPP) ######################"
echo "##########################################################################"
echo

if [[ ! -d "${CODE_FOLDER}" ]]; then
    echo "### Downloading PPSSPP code..."
    git clone "${GIT_REPOSITORY}" ${GIT_ARGS} "${CODE_FOLDER}"
else
    cd "${CODE_FOLDER}"
    echo "### Pulling PPSSPP code..."
    git pull --rebase "${GIT_REPOSITORY}"
    git submodule update --init --recursive
fi
echo

echo "### Creating ${BUILD_FOLDER} folder..."
echo

mkdir -p "${BUILD_FOLDER}"
cd "${BUILD_FOLDER}"

echo "### Compiling PPSSPP binaries"
echo

cmake "${CODE_FOLDER}"
cmake j"$(nproc)" "${CODE_FOLDER}"
make install

echo
echo "### Copying PPSSPP binaries to ${EMULATORS_FOLDER}"
echo

mkdir -p "${EMULATORS_FOLDER}"
cp -r "${CODE_FOLDER}/assets" "${BUILD_FOLDER}/PPSSPPSDL" "${EMULATORS_FOLDER}"
