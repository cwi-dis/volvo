#!/bin/sh
dirname=`dirname $0`
cd $dirname/server
exec npm start
