#!/bin/bash
#
# Installs to a Linux system using virtual environment.

set -e
echo "Install to home or system? [H/s]"
read dest
if [ -z $dest ];
then
    dest="H"
fi

if [ $dest == "s" ] || [ $dest == "S" ];
then
    sudo python3 -m venv /opt/timecard-app
else
    sudo python3 -m venv ~/.timecard-app
fi
#python3 -m venv timecard-app
