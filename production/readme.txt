To build the hardware see jeenode/readme.txt and the hardware folder.

To change the visualisation see server/public (which has the HTML files,
SVG files and JavaScripts).

The rest of these instructions are for using karnemelk (the white MacBook)
and the byBorre user (as it has been prepared for the Volvo presentation).

To assemble the system and configure the display for the first time:

 - Assembling the table, connect the jeenodes, power it up.
 
 - attach the VGA dongle and big screen to karnemelk
 
 - power on karnemelk, takes about 60 seconds.
 
 - it may try to start the presentation (some Terminal screens, maybe a
   fullscreen Chrome browser window). Kill everything by using
   CMD-Q (quit application), CMD-TAB (goto next application) and possibly
   NEWLINE (if there is a dialog "are you sure you want to quit")
   until only the Finder is running.
 
 - configure the big display to be portrait mode
   with the right orientation (1080x1920, 75Hz is known to work. If not
   try other refresh frequencies).
   
 - set the big display to be the primary screen.
 
 - Make sure the screen saver/power saver are off (Apple Menu -> System Preferences
   -> Power Saver, all slider to the far right).
   
 - Attach the JeeNode dongle.
 
 - Power down the system (press power button, select "Shut down" in the dialog).

To start the system:
 
 - Make sure the VGA dongle is connected, VGA is connected and the big screen is on.
 
 - Make sure the JeeNode dongle is connected.
 
 - Turn on karnemelk.
 
 - After about a minute it comes up and tries to start the whole presentation (this
   will take another half minute). If everything works you should see the following things:
   
   - The macbook screen shows a grey pattern
   
   - the JeeNode dongle flashes red LEDs
   
   - the big screen shows the demo
   
 - If anything went wrong (or takes too long) type sequences of CMD-Q, RETURN and CMD-TAB
   until the macbook screen shows the black-and-white desktop again. Then doule-click
   the "start volvo on powerup" icon and hope for the best.
   
 - Always turn of the MacBook BEFORE powering down the display or removing cables. Otherwise
   you may have to go through the "assembly" procedure again.
 
To debug the system:

 - if things don't start up:
   make sure you have connected all dongles and cables. The jeenode dongle should flash when
   it is receiving data from the sensor-jeenodes (and when the receiver progrm is running).
   Looking at the Terminal window (the frontmost is probably the most recent one) may give
   an indication of what is wrong.
   
 - if some of the sensors don't work:
   you scroll down the normal presentation screen (in Google Chrome) there is a "show debug
   console" link. Click this. You will see the output of each individual sensor. You will
   also see an error message in red if any of the jeenodes is not responding.
   
 - if the display is incorrect (wrong screen, wrong orientation):
   - repeat the "assembly" procedure.


