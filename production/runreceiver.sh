#!/bin/sh
dirname=`dirname $0`
SERIAL=/dev/tty.usbserial-AL006SWC
SERVER=localhost:23148
exec python $dirname/receiver/receiver.py $SERIAL $SERVER
