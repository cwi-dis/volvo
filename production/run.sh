#!/bin/sh
dirname=`dirname $0`
sh $dirname/runserver.sh &
sleep 5
sh $dirname/runvisualisation.sh &
sh $dirname/runreceiver.sh &
