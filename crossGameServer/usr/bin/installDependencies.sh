#!/bin/bash

echo "Comprobando si hay dependencias por instalar..."

if [[ ! -f "/etc/productConf/product.version" ]]; then
    touch "/etc/productConf/product.version"
fi

version=$(dpkg -l | grep crossgameapp | awk '{ print $3 }')

if [[ $(cat '/etc/productConf/product.version') != $version ]]; then

    echo "Detectado cambio de versión, comprobando las dependencias..."

    dependencies=("imutils" "opencv-python" "python-vlc" "ds4drv" "screeninfo" "pygame")

    pip install --upgrade pip
        
    for d in "${dependencies[@]}"; do
        pip install --user "$d"
    done

    echo $version > "/etc/productConf/product.version"
    echo "Dependencias instaladas correctamente"
else
    echo "No hay dependencias por instalar"
fi

touch /tmp/crossgame.ready