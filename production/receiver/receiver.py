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

class SensorReceiver:
    def __init__(self, comport, server):
        self.comport = comport
        self.server = server
        self.buffers = defaultdict(float)

    def exp_average(self, key, val, alpha=0.2):
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
        self.buffers[key] = (alpha * val) + (1.0 - alpha) * self.buffers[key]
        return self.buffers[key]

    def run(self):
        while True:
            # read line from serial port
            result = self.comport.readline()

            try:
                # parse line read from serial port as JSON
                data = json.loads(result)

                # apply exponential smoothing to each value in the data,
                # but only for the keys that are sensor values
                for key in data.keys():
                    if key.isdigit():
                        data[key] = round(self.exp_average(key, data[key]), 2)

                if VERBOSE:
                    # print result with timestamp to stdout
                    now = time.time()
                    sys.stdout.write("%.2f => %s\n" % (now, str(data)))
                    sys.stdout.flush()

                # publish data on channel 'pressure'
                if self.server:
                    self.server.publish('pressure', data)
            except ValueError:
                # skip to next iteration if JSON parsing causes an exception
                pass

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
