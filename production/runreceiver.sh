#!/bin/sh
dirname=`dirname $0`
case `uname` in
Darwin)
	SERIAL=/dev/tty.usbserial-AL006SWC
	;;
Linux)
	SERIAL=/dev/ttyUSB0
	;;
esac
SERVER=localhost:23148
exec python $dirname/receiver/receiver.py $SERIAL $SERVER
