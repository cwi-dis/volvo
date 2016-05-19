#!/bin/sh
dirname=`dirname $0`
set -x

killall python
killall node
killall npm
killall chromium-browser

sh $dirname/tunneltoflauwte.sh &
sh $dirname/runserver.sh > /home/pi/log.runserver.log 2>&1 &
sleep 10
sh $dirname/runvisualisation.sh > /home/pi/log.runvisualisation.log 2>&1 &
xset s noblank
xset s off
xset -dpms
sleep 60
sh $dirname/runreceiver.sh >/home/pi/log.runreceiver.log 2>&1 &
