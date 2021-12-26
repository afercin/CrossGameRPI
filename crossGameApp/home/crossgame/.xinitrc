#!/bin/sh

python3 /usr/bin/controllerHook.py &

roms="/mnt/hdd/rpi/roms"

python3 /usr/bin/changeResolution -r 640x480 -c
/usr/share/apptk/emulators/duckstation/bin/duckstation-qt "$roms/ps1/Final Fantasy VII/Disco 1/Final Fantasy VII (Disc 1)(NTSC)(Spanish v3.2).cue" >> /var/log/product/duckstation.log
#fceux --nogui "$roms/nes/Tetris/Tetris (USA).nes" > /tmp/nes.log 2>&1

#python3 /usr/bin/tkMainWindow.py > /var/log/product/apptk.log 2>&1
