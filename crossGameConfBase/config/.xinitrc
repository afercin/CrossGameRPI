#!/bin/sh
xset s off
xset -dpms
xset s noblank

python3 /usr/bin/cgAPI.py > /var/log/product/api.log 2>&1 &
python3 /usr/bin/keyboardTranslator.py &

crossgameapp > /var/log/product/app.log 2>&1