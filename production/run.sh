#!/bin/sh
dirname=`dirname $0`
set -x

killall python
killall node
killall npm
killall 'Google Chrome'

sh $dirname/runserver.sh &
sleep 10
sh $dirname/runvisualisation.sh &
exec $dirname/runreceiver.sh
