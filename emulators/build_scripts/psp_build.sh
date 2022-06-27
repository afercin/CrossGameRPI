#!/bin/bash

[[ ! -f ./build_scripts/common.sh ]] && echo "[ERROR] No se encuentra el script common" && exit 1
. ./build_scripts/common.sh

## Variables
EMULATOR="psp"
DEST_FOLDER="${EMULATORS_FOLDER}/${EMULATOR}"
CODE_FOLDER="${GIT_FOLDER}/${EMULATOR}"
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
    git pull
fi
echo

echo "### Creating ${BUILD_FOLDER} folder..."
echo

mkdir -p "${BUILD_FOLDER}"
cd "${BUILD_FOLDER}"

echo "### Compiling PPSSPP binaries"
echo

cmake "${CODE_FOLDER}"
cmake -j 4 "${CODE_FOLDER}"
make install

echo
echo "### Copying PPSSPP binaries to ${DEST_FOLDER}"
echo

mkdir -p "${DEST_FOLDER}"
cp -r "${CODE_FOLDER}/assets" "${BUILD_FOLDER}/PPSSPPSDL" "${DEST_FOLDER}"
