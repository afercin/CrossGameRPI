#!/bin/sh
xset s off
xset -dpms
xset s noblank

echo $DISPLAY > /tmp/display

. /etc/productConf/start.conf

changeResolution -r $default_resolution
cgAPI.py > /var/log/product/api.log 2>&1 &
keyboardTranslator.py &

crossgameapp > /var/log/product/app.log 2>&1