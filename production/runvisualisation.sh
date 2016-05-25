#!/bin/sh
case `uname` in
Darwin)
	BROWSER="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
	;;
Linux)
	BROWSER=chromium-browser
	;;
esac
URL="http://localhost:8080"
exec "$BROWSER" --incognito --temp-profile --start-fullscreen "$URL"
