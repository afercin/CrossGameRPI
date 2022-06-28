#!/bin/bash

set -e

[[ ! -f ./build_scripts/common.sh ]] && echo "[ERROR] No se encuentra el script common" && exit 1
. ./build_scripts/common.sh

## Variables
EMULATOR="ps1"
DEST_FOLDER="${EMULATORS_FOLDER}/${EMULATOR}"
CODE_FOLDER="${GIT_FOLDER}/${EMULATOR}"
BUILD_FOLDER="${CODE_FOLDER}/build"

GIT_REPOSITORY="https://github.com/stenzek/duckstation.git"
GIT_ARGS="-b dev"

## Code

echo "##########################################################################"
echo "################## Building PS1 emulator (DuckStation) ###################"
echo "##########################################################################"
echo

if [[ ! -d "${CODE_FOLDER}" ]]; then
    echo "### Downloading DuckStation code..."
    git clone "${GIT_REPOSITORY}" ${GIT_ARGS} "${CODE_FOLDER}"
else
    cd "${CODE_FOLDER}"
    echo "### Pulling DuckStation code..."
    git pull
fi
echo

echo "### Creating ${BUILD_FOLDER} folder..."
echo

mkdir -p "${BUILD_FOLDER}"
cd "${BUILD_FOLDER}"

echo "### Compiling DuckStation binaries"
echo

cmake -DCMAKE_BUILD_TYPE=Release -GNinja "${CODE_FOLDER}"
ninja 

echo
echo "### Copying DuckStation binaries to ${DEST_FOLDER}"
echo

[[ -d "${DEST_FOLDER}" ]] && rm -r "${DEST_FOLDER}"
mv "${BUILD_FOLDER}/bin" "${DEST_FOLDER}"
