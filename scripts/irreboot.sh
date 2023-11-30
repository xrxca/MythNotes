#!/bin/sh
for r in 128 129 ; do
	/usr/bin/curl -s -o /dev/null --connect-timeout 5 \
		http://192.168.1.${r}/reboot
done
