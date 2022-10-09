#!/bin/bash

STEAM_MODE="/tmp/steam.mode"
STARTX="startx --"

if [[ ! -f "/etc/productConf/start.conf" ]]; then
    echo "There is no configuration file, exiting..."
    exit 1
fi

source "/etc/productConf/start.conf"


if [[ "${disable_xserver}" != "yes" ]]; then
    [[ "${hide_mouse}" == "yes" ]] && STARTX="$STARTX -nocursor"
    $STARTX > /tmp/xserver.log 2>&1
fi

if [[ -f "${STEAM_MODE}" ]]; then
    rm -f "${STEAM_MODE}"
    steamlink
fi
