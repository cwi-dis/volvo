import json
import sys
import time

from collections import defaultdict
from sensorrelay import WebsocketPublisher
from serial import Serial
from serial.tools import list_ports

# buffer for storing accumulator values used in exponential smoothing for each
# sensor ID
buffers = defaultdict(float)


def exp_average(key, val, alpha=0.2):
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
    buffers[key] = (alpha * val) + (1.0 - alpha) * buffers[key]
    return buffers[key]


def get_portname():
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
    print "Please specify WebSocket host:"
    print

    ws_host = raw_input("> ")
    print

    return ws_host


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

if __name__ == "__main__":
    port, ws_host = "", ""

    if len(sys.argv) <= 2:
        port = get_portname()
        ws_host = get_ws_host()
    else:
        port = sys.argv[1]
        ws_host = sys.argv[2]

    # initialise serial connection with 57600 baud
    receiver = Serial(port, baudrate=57600)
    # initialise PubSub system
    pub = None
    if pub:
        pub = WebsocketPublisher(ws_host)
    else:
        sys.stdout.write("WARNING: no websocket host specified, not publishing data\n")
    lastSeen = {}
    try:
        while True:
            # read line from serial port
            result = receiver.readline()

            try:
                # parse line read from serial port as JSON
                data = json.loads(result)

                # apply exponential smoothing to each value in the data
                for key in data.keys():
                    data[key] = round(exp_average(key, data[key]), 2)

                # print result with timestamp to stdout
                now = time.time()
                for sensorNum in data.keys():
                    lastSeen[sensorNum] = now
                sys.stdout.write("%.2f => %s\n" % (now, str(data)))
                sys.stdout.flush()

                # publish data on channel 'pressure'
                if pub:
                    pub.publish('pressure', data)
            except ValueError:
                # skip to next iteration if JSON parsing causes an exception
                pass
    except KeyboardInterrupt:
        for sensorNum, ts in lastSeen.items():
            print sensorNum, '\t', ts
            
