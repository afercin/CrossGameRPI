#!/bin/bash

[[ ! -f ./common.sh ]] && echo "[ERROR] No se encuentra el script common" && exit 1
. ./common.sh

## Variables
EMULATOR="n64"
DEST_FOLDER="${EMULATORS_FOLDER}/${EMULATOR}"
CODE_FOLDER="${GIT_FOLDER}/${EMULATOR}"
BUILD_FOLDER="${CODE_FOLDER}/build"

USR_FOLDER="/crossGameEmulators/usr/"
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
        git clone "https://github.com/mupen64plus/${component}.git" "${COMPONENT_FOLDER}"
    else
        cd "${COMPONENT_FOLDER}"
        echo "### Pulling  ${component} code..."
        git pull
    fi

    echo
    echo "### Compiling ${component} binaries"
    echo

    make -C "${COMPONENT_FOLDER}/projects/unix" PREFIX="${BUILD_FOLDER}" all
    make -C "${COMPONENT_FOLDER}/projects/unix" install PREFIX="${BUILD_FOLDER}"
    
    echo
done

echo "### Copying Mupen64Plus binaries to ${DEST_FOLDER}"
echo

[[ -d "${DEST_FOLDER}" ]] && rm -r "${DEST_FOLDER}"
mv "${BUILD_FOLDER}/bin" "${DEST_FOLDER}"

echo "### Copying Mupen64Plus libraries to ${LIB_FOLDER}/lib"
echo

mkdir -p "${LIB_FOLDER}"
cp -r "${BUILD_FOLDER}/lib" "${LIB_FOLDER}"

echo "### Copying Mupen64Plus libraries to ${LIB_FOLDER}/share"
echo

cp -r "${BUILD_FOLDER}/share" "${USR_FOLDER}"
