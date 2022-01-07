#!/bin/sh
xset s off
xset -dpms
xset s noblank

python3 /usr/bin/prueba
python3 /usr/bin/controllerHook.py &
python3 /usr/bin/simulateKeys.py -s &

roms="/rpi/roms"
game="$roms/$(cat $roms/current.game)"
emulators="/usr/share/server/emulators"

#firefox --window-size 1920,1080 -kiosk https://www.netflix.com/
#"$emulators/ps2/DobieStation" "$roms/ps2/Final Fantasy XII.iso" > /tmp/ps2.log 2>&1
#"$emulators/psp/PPSSPPSDL" --fullscreen "$roms/psp/Crash of the Titans/Crash Of The Titans.iso"

python3 /usr/bin/changeResolution.py -r 640x480 -c
"$emulators/ps1/duckstation-qt" -fullscreen "$game" > /var/log/product/duckstation.log 2>&1

#fceux --nogui "$roms/nes/Tetris/Tetris (USA).nes" > /tmp/nes.log 2>&1

#python3 /usr/bin/tkMainWindow.py > /var/log/product/apptk.log 2>&1

#python3 /usr/bin/changeResolution -r 1920x1080
#chromium-browser -start-fullscreen --window-position=0,0 --window-size=1920,1080  https://www.netflix.com/
#firefox --window-size 1920,1080 -kiosk https://www.netflix.com/