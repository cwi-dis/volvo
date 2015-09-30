# Script for reading sensor data from a serial port and sending it to a PubSub
# channel.
#
# If this script is launched without any parameters, it will ask you to choose
# a serial device to read from and a WebSocket host to send the data to in the
# format hostname:port.
# These parameters however can also be passed in through the command line like
# so:
#
#    $ python read_data.py /dev/cu.usbserial-A704FZK7 localhost:23148
#
# This will read the data from the serial device at /dev/cu.usbserial-A704FZK7,
# process it and send it to the PubSub server located on localhost at port
# 23148 (make sure to start the server first).
#
# Please note that in order for this script to work, you need to install
# pyserial from PyPI and the sensorrelay package which can be found in the
# DIS wearing-sense repository.

import json
import sys
import time

from collections import defaultdict
from sensorrelay import WebsocketPublisher
from serial import Serial
from serial.tools import list_ports

VERBOSE=False
DOTS=True
AVERAGE=True

DEFAULT_MAXIMUM_PRESSURE = 3      # Defaul value (and minimal value) for pressure that is seen as 100%

SWIPE_TIMEOUT = 1.0                # A swipe remains active for at least one second

def get_portname():
    """Interactive helper function - ask for tty portname"""
    print "Please select a port to listen on:"
    print

    available_ports = list_ports.comports()
    for i, port in enumerate(available_ports):
        print "%2d => %s" % (i + 1, port[0])

    print
    portnum = int(raw_input("> "))
    print

    return available_ports[portnum - 1][0]


def get_ws_host():
    """Interactive helper function - ask for websocket address"""
    print "Please specify WebSocket host:port"
    print

    ws_host = raw_input("> ")
    print

    return ws_host

class SensorValueCollector:
    def __init__(self):
        self.perSensorMin = {}
        self.perSensorMax = {}
        self.curValues = {}
        self._ignore = ()
        self.defaultMaximumPressure = DEFAULT_MAXIMUM_PRESSURE
        
    def ignore(self, *keys):
    	self._ignore = keys
        

    def process_value(self, tile, key, value):
    	if key in self._ignore: return 0.0
        # Keep per-sensor minimal and maximal value and global maximum
        if not key in self.perSensorMin or value < self.perSensorMin[key]:
            self.perSensorMin[key] = value
            # Also optionally adjust default maximum, to cater for tiles that
            # are too tight
            if value*2 > self.defaultMaximumPressure:
            	self.defaultMaximumPressure = value*2
        if not key in self.perSensorMax or value > self.perSensorMax[key]:
            self.perSensorMax[key] = value
        else:
            self.perSensorMax[key] -= 1
        rangeMin = self.perSensorMin[key]
        rangeMax = max(self.perSensorMin[key]+self.defaultMaximumPressure, self.perSensorMax[key])
        rv = float(value-rangeMin) / (rangeMax-rangeMin)
        if rv > 0.5:
            rv = 1.0
        else:
            rv = 0.0
        self.curValues[key] = rv
        return rv
        
    def get_values(self):
        return self.curValues
        
class HandSensorValueCollector(SensorValueCollector):
    def __init__(self):
        SensorValueCollector.__init__(self)
        self.depressTime = None
        self.releaseTime = None

    def get_values(self):
        rv = {}
        if self.curValues:
            value = max(self.curValues.values())
            for k in self.curValues.keys():
                rv[k] = self.curValues[k]
            if value:
                rv['hidehand'] = 0
            else:
                rv['hidehand'] = 1
            rv['hidescanning'] = 1
            rv['hideloaded'] = 1
            if value and self.depressTime == None:
                # Hand has just been pressed.
                self.depressTime = time.time()
                self.releaseTime = None
            elif not value and self.releaseTime == None and self.depressTime:
                # Hand has just been released
                if time.time() >= self.depressTime + 2:
                    # It was depressed for over 2 seconds
                    self.releaseTime = time.time()
                self.depressTime = None
            if self.depressTime:
                if time.time() < self.depressTime + 2:
                    rv['hidescanning'] = 0
                else:
                    rv['hideloaded'] = 0
            elif self.releaseTime and time.time() < self.releaseTime+5:
                rv['hideloaded'] = 0
        return rv
        
class SwipeSensorValueCollector(SensorValueCollector):
    def __init__(self):
        SensorValueCollector.__init__(self)
        self.active = False
        self.firstSensor = None
        self.lastSensor = None
        self.swipeStartTime = None
        
    def process_value(self, tile, key, value):
        value = SensorValueCollector.process_value(self, tile, key, value)
        if value > 0:
            # This sensor is pressed. Update start and end of swipe, and swipe active time.
            self.swipeStartTime = time.time()
            if key < self.firstSensor or not self.firstSensor:
                self.firstSensor = key
            if key > self.lastSensor or not self.lastSensor:
                self.lastSensor = key
        elif self.swipeStartTime and time.time() > self.swipeStartTime + SWIPE_TIMEOUT:
            # This sensor is not pressed, and nothing has been pressed during the timeout.
            # Reset the slider.
            self.firstSensor = None
            self.lastSensor = None
            self.swipeStartTime = None
        else:
            # This sensor is not pressed, but a swipe is underway. Light up this sensor if
            # it is between first and last.
            if self.firstSensor <= key and self.lastSensor >= key:
                value = 1.0
        return value
    
    def get_values(self):
        rv = {}
        for k in self.curValues.keys():
            if self.swipeStartTime and self.firstSensor <= k and self.lastSensor >= k:
                value = 1.0
            else:
                value = 0.0
            rv[k] = value
        return rv
        
class SensorReceiver:
    def __init__(self, comport, server):
        self.comport = comport
        self.server = server
        self.runningAverage = defaultdict(float)
        self.collectors = {
            1: SensorValueCollector(),
            2: SensorValueCollector(),
            3: SensorValueCollector(),
            4: SensorValueCollector(),
            5: SensorValueCollector(),
            6: SensorValueCollector(),
            7: SensorValueCollector(),
            8: HandSensorValueCollector(),
            9: SwipeSensorValueCollector(),
            }
        self.collectors[7].ignore('7s3')	# Tile 7 is the small tile with 2 sensors
        self.collectors[8].ignore('8s2', '8s3')	# Tile 8 is the hand tile with one sensor

    def exp_average(self, key, val, alpha=0.9):
        """ Computes exponential running average for the given value.
        This function computes an exponential running average for the parameter
        'val'. The parameter 'key' designates the sensor ID for which the moving
        average shall be computed.

        The intensity of the smoothing can be tuned by adjusting the value 'alpha'.
        A low value for alpha (e.g. 0.01) yields a stronger smoothing effect and
        correspondingly a high value (e.g. 0.5) a significantly weaker smoothing
        effect but increases responsiveness.
        Empirically alpha=0.2 seems to provide a good balance between smoothing and
        adequate response times given the data for which this is intended to be
        used.
        """
        self.runningAverage[key] = round((alpha * val) + (1.0 - alpha) * self.runningAverage[key], 2)
        return self.runningAverage[key]

    def run(self):
        transmitStorage = {}
        transmitStorageTiles = set()
        while True:
            # read line from serial port
            result = self.comport.readline()

            try:
                # parse line read from serial port as JSON
                data = json.loads(result)
            except ValueError:
                # skip to next iteration if JSON parsing causes an exception
                sys.stdout.write("JSON parser raised ValueError on %s" % repr(result))
                continue

            # apply exponential smoothing to each value in the data,
            # but only for the keys that are sensor values
            tile = data['n']
            collector = self.collectors[tile]
            if VERBOSE:
                # print result with timestamp to stdout
                now = time.time()
                sys.stdout.write("%.2f .. %s\n" % (now, str(data)))
                sys.stdout.flush()
            for key in data.keys():
                if key == 'n': continue
                value = data[key]
                if key.isdigit():
                    key = '%ss%s' % (tile, key)
                    value = collector.process_value(tile, key, value)
                else:
                    # Non-sensor data items are stored into the transmitStorage directly
                    key = '%s%s' % (tile, key)
                    transmitStorage[key] = value

            # 
            # Save the data, possibly transmitting if we have a full set
            #
            if tile in transmitStorageTiles:
                # Get current data for all tiles
                for collector in self.collectors.values():
                    to_add = collector.get_values()
                    if AVERAGE:
                        for k in to_add.keys():
                            to_add[k] = self.exp_average(k, to_add[k])
                    transmitStorage.update(to_add)
                    
                if VERBOSE:
                    # print result with timestamp to stdout
                    now = time.time()
                    sys.stdout.write("%.2f => %s\n" % (now, str(transmitStorage)))
                    sys.stdout.flush()
                    
                if self.server:
                    self.server.publish('pressure', transmitStorage)
                    if DOTS:
                        sys.stderr.write(".")
                        sys.stderr.flush()
                    
                transmitStorage = {}
                transmitStorageTiles = set()
                    
            transmitStorageTiles.add(tile)

def main():
    port, ws_host = "", ""

    if len(sys.argv) > 1 and sys.argv[1] == "-v":
        global VERBOSE
        VERBOSE=True
        del sys.argv[1]
        
    if len(sys.argv) <= 2:
        port = get_portname()
        ws_host = get_ws_host()
    else:
        port = sys.argv[1]
        ws_host = sys.argv[2]

    # initialise serial connection with 57600 baud
    comport = Serial(port, baudrate=57600)
    # initialise PubSub system
    pub = None
    if ws_host:
        pub = WebsocketPublisher(ws_host)
    else:
        sys.stderr.write("WARNING: no websocket host specified, not publishing data\n")
    rec = SensorReceiver(comport, pub)
    rec.run()
        

if __name__ == "__main__":
    main()
