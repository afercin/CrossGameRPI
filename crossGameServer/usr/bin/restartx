#!/bin/bash
uflag="false"
tty="tty1"

while getopts ut: flag
do
    case "${flag}" in
        u) uflag="true";;
        t) tty="tty${OPTARG}";;
        *) ;;
    esac
done

if [[ $uflag == "true" ]] || ! kill $(ps aux | grep xorg | grep $tty | awk '{ print $2 }'); then
    pkill -9 -t $tty
    exit 0
fi
