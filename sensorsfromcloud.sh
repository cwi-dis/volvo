#!/bin/sh
curl https://api.particle.io/v1/devices/240023001547343339383037/pressures?access_token=fcd299e67b640c8d2f2cd1a493e9a3095c61afe0 2>/dev/null |grep result |egrep -o "\"[0-9,]+\"" |tr -d '"'
