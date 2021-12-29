#!/bin/sh
xset s off
xset -dpms
xset s noblank

python3 /usr/bin/controllerHook.py &

game="/mnt/hdd/rpi/roms/$(cat /mnt/hdd/rpi/roms/current.game)"

python3 /usr/bin/changeResolution -r 640x480 -c
/usr/share/apptk/emulators/duckstation/bin/duckstation-qt -fullscreen "$game" > /var/log/product/duckstation.log 2>&1

#fceux --nogui "$roms/nes/Tetris/Tetris (USA).nes" > /tmp/nes.log 2>&1

#python3 /usr/bin/tkMainWindow.py > /var/log/product/apptk.log 2>&1

#python3 /usr/bin/changeResolution -r 1920x1080
#firefox --window-size 1920 https://www.netflix.com/
#firefox --window-size 1920,1080 -kiosk https://www.netflix.com/
