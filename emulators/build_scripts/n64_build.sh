#!/bin/bash

set -e

[[ ! -f /opt/build_scripts/common.sh ]] && echo "[ERROR] No se encuentra el script common" && exit 1
. /opt//build_scripts/common.sh

## Variables
CODE_FOLDER="${GIT_FOLDER}/n64"
BUILD_FOLDER="${CODE_FOLDER}/build"

USR_FOLDER="/emulators/usr/"
LIB_FOLDER="${USR_FOLDER}/local"

COMPONENTS="core rom ui-console audio-sdl input-sdl rsp-hle video-rice video-glide64mk2"
GIT_ARGS=""

## Code

echo "##########################################################################"
echo "################# Building N64 emulator (Mupen64Plus) ####################"
echo "##########################################################################"
echo

[[ -d "${BUILD_FOLDER}" ]] && rm -r "${BUILD_FOLDER}"

for component in ${COMPONENTS}; do
    component="mupen64plus-${component}"
    COMPONENT_FOLDER="${CODE_FOLDER}/${component}"
    
    if [[ ! -d "${COMPONENT_FOLDER}" ]]; then
        echo " ### Downloading ${component} code..."
        git clone "https://github.com/mupen64plus/${component}.git" ${GIT_ARGS} "${COMPONENT_FOLDER}"
    else
        cd "${COMPONENT_FOLDER}"
        echo "### Pulling  ${component} code..."
        git pull
    fi
    echo

    echo "### Compiling ${component} binaries"
    echo

    make -C "${COMPONENT_FOLDER}/projects/unix" all
    make -C "${COMPONENT_FOLDER}/projects/unix" install

    echo
done
