#!/bin/bash
# Needs to be cleaned up and should probably be replaced with a python script.

# Do the actual send to the ESP IR transmitter, uses a lockfile to prevent multiple sends
dosend() { # ip channel
        umask 0000
        LOCKFILE=/var/lock/irsend_${1}.lock
        (
                flock -w 30 9 || return 1
                logger -t mythtv "Channel HDPVR${1} - ${2}"
                wget -O - http://${1}/channel/${2} &>/dev/null
        ) 9>${LOCKFILE}
}

case "${1:-x}" in
        1) ip=192.168.1.129 ;;
        2) ip=192.168.1.128 ;;
        *) exit ;;
esac
c="${2//[^0-9]}"
[ ${#c} -ne 3 ] && exit
[ ${c} -lt 101 ] && exit
[ ${c} -gt 999 ] && exit
dosend ${ip} ${c} && exit
# If the send failed sleep and try again in 20 seconds
sleep 20
dosend ${ip} ${c} && exit
logger -t mythtv "IRChannel Failed ($?) ${t} ${c}"
