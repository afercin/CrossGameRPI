#!/bin/sh
xset s off
xset -dpms
xset s noblank

python3 /usr/bin/keyboardTranslator.py &

python3 /usr/bin/cgAPI.py > /tmp/api.log 2>&1 &

chromium-browser -start-fullscreen --window-position=0,0 --window-size=1920,1080  http://localhost:4200/

roms="/rpi/roms"
game="$roms/$(cat $roms/current.game)"
emulators="/usr/share/server/emulators"

#firefox --window-size 1920,1080 -kiosk https://www.netflix.com/
#"$emulators/ps2/DobieStation" "$roms/ps2/Final Fantasy XII.iso" > /tmp/ps2.log 2>&1
#"$emulators/psp/PPSSPPSDL" --fullscreen "$roms/psp/Crash of the Titans/Crash Of The Titans.iso"

python3 /usr/bin/changeResolution.py -r 640x480 -c > /tmp/prueba 2>&1
touch /tmp/key.lock
"$emulators/ps1/duckstation-qt" -fullscreen "$game" > /var/log/product/duckstation.log 2>&1

#fceux --nogui "$roms/nes/Tetris/Tetris (USA).nes" > /tmp/nes.log 2>&1

#python3 /usr/bin/tkMainWindow.py > /var/log/product/apptk.log 2>&1

#python3 /usr/bin/changeResolution -r 1920x1080
#chromium-browser -start-fullscreen --window-position=0,0 --window-size=1920,1080  https://www.netflix.com/
#firefox --window-size 1920,1080 -kiosk https://www.netflix.com/