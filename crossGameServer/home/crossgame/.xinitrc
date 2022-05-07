#!/bin/sh
xset s off
xset -dpms
xset s noblank

python3 /usr/bin/cgAPI.py > /tmp/api.log 2>&1 &
python3 /usr/bin/keyboardTranslator.py > /tmp/keyboard.log 2>&1 &

crossgame