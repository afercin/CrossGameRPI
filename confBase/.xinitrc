#!/bin/sh
xset s off
xset -dpms
xset s noblank

echo $DISPLAY > /tmp/display

cgAPI.py > /var/log/product/api.log 2>&1 &
keyboardTranslator.py &

crossgameapp > /var/log/product/app.log 2>&1