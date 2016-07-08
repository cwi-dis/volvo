#!/bin/sh
dirname=`dirname $0`
cd $dirname
if [ -f $HOME/NO-IGOR ]; then
	echo "Skip running IGOR because $HOME/NO-IGOR exists"
	exit 1
fi
exec python ../../../igor/igor/igor -d ../../../igor/databases/igorDatabase.volvo
