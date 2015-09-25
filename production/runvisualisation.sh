#!/bin/sh
BROWSER="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
URL="http://localhost:8080"
exec "$BROWSER" --incognito --start-fullscreen "$URL"
