#!/bin/bash
#
# Switching on or off light at home
# bartjan@pc-mania.nl - 08 Mar 2018

snmp_exec="/usr/bin/snmpset"

function check_reqs {
	if [ ! -f $snmp_exec ]; then
		echo "Error: snmpset executable not found.."
		echo ""
		exit 1
	fi
}

function show_help {
	echo "Error: incorrect syntax.."
	echo "Usage: ./lights.sh [on|off]"
	echo ""
}

function switch {
	# 1st arg is outlet nr (integer)
	# 2nd arg options: on / off
	if [ $2 == "on" ]; then
		${snmp_exec} -v2c -cpublic 192.168.1.251 1.3.6.1.4.1.318.1.1.4.4.2.1.3.${1} i 1 1>/dev/null 2>&1
	elif [ $2 == "off" ]; then
		${snmp_exec} -v2c -cpublic 192.168.1.251 1.3.6.1.4.1.318.1.1.4.4.2.1.3.${1} i 2 1>/dev/null 2>&1
fi
}

# Start the program

check_reqs

if [ ! $1 ]; then
	show_help
	exit 1
fi


if [ $1 == "on" ]; then
	echo "Iluminate"
	switch 1 on
	switch 8 on
elif [ $1 == "off" ]; then
	echo "Deluminate"
	switch 1 off
	switch 8 off
else
	show_help
	exit 1
fi

