#!/bin/sh
dirname=`dirname $0`
cd $dirname
exec python ../../home/homeServer/homeServer -p 9090
