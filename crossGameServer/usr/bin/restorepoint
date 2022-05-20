#!/bin/bash
## Static vars
SCRIPTNAME="resorepoint"
BACKUPFOLDER="/rpi/backups"
cflag="false"
fflag="false"
vflag="false"
xflag="false"

## Call to libgoran

## Colors
NC='\033[0m'
BLACK='\033[0;30m'
RED='\033[0;31m'
GREEN='\033[0;32m'
BROWN='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
LGRAY='\033[0;37m'
DGRAY='\033[1;30m'
LRED='\033[1;31m'
LGREEN='\033[1;32m'
YELLOW='\033[1;33m'
LBLUE='\033[1;34m'
LPURPLE='\033[1;35m'
LCYAN='\033[1;36m'
LGRAY='\033[1;37m'

##Functions
currentDate()
{
    date +'%Y/%m/%d %H:%M:%S'
}

msg()
{
    d=$(currentDate)
    echo -e "[$d][$1] $2" >> $LOGFILE
    if [[ $vflag == "true" ]]; then
        echo -e "[$d][$1] $2"
    fi
}

msgInfo()
{
    msg "${LCYAN}INFO${NC}" "$1"
}

msgOk()
{
    msg "${LGREEN}OK${NC}" "$1"
}

msgWarn()
{
    msg "${YELLOW}WARN${NC}" "$1"
}

msgError()
{
    msg "${LRED}ERROR${NC}" "$1" 
}

## Checkers

if [[ -z ${SCRIPTNAME+x} ]]; then
    vflag="false"
    echo "There is no \${SCRIPTNAME} var, libgoran can not continue." 1>&2
    exit 1
fi

## Static vars
LOGFOLDER="/var/log/product"
LOGFILE="${LOGFOLDER}/${SCRIPTNAME}.log"

## Code

while getopts vcxf: flag
do
    case "${flag}" in
        x) xflag="true";;
        f) fflag="true"
           filename=${OPTARG};;
        c) cflag="true";;
        v) vflag="true";;
        *) echo "restorepoint -c|x [-f filename] [-v]"
           exit 1
        ;;
    esac
done

if [[ $cflag == "true" ]]; then
    if [[ $fflag == "false" ]]; then
        d=$(currentDate | tr "/" "-" | tr " " "_" | tr ":" "-")
        filename="${BACKUPFOLDER}/$d.tar.gz"
        msgWarn "Using default filename \"$filename\"!"
    fi
    msgInfo "Creating backup file in \"$filename\"..."
    if tar --exclude=/mnt \
        --exclude=/dev \
        --exclude=/.disk \
        --exclude=/lost+found \
        --exclude=/media \
        --exclude=/proc \
        --exclude=/run \
        --exclude=/snap \
        --exclude=/swapfile \
        --exclude=/sys \
        --exclude=/var/backups \
        --exclude=/var/lock \
        --exclude=/var/log \
        --exclude=/var/tmp \
        --exclude=/var/run \
        --exclude=/tmp \
        -zcf "$filename" / 2> /dev/null; then
        msgOk "Backup created sucessfully!"
    else
        msgError "Can not create backup!"
        exit 1
    fi
    exit 0
fi

if [[ $xflag == "true" ]]; then
    if [[ $fflag == "false" ]]; then
        msgError "Backup file not selected!"
        exit 1
    fi
    msgInfo "Restoring system with backup \"$filename\"..."
    if tar -zxf "$filename" /; then
        msgOK "Files from \"$filename\" restored!"
    else
        msgError "\"$filename\" is corrupted!"
        msgError "Aborting process!"
        exit 1
    fi
    msgInfo "Rebooting System"
    for logfile in $(ls /var/log/product); do
        {
            echo "◤━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━◥"
            echo "                                          SYSTEM RESTORED                                           "
            echo "◣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━◢"
        } >> $logfile
    done
    reboot
fi