import json
import sys
import time

from collections import defaultdict
from sensorrelay import WebsocketPublisher
from serial import Serial
from serial.tools import list_ports

buffers = defaultdict(float)


def exp_average(i, n, alpha=0.2):
    buffers[i] = (alpha * n) + (1.0 - alpha) * buffers[i]
    return buffers[i]


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


if __name__ == "__main__":
    port, ws_host, offset = "", "", 0

    if len(sys.argv) <= 2:
        port = get_portname()
        ws_host = get_ws_host()
    else:
        port = sys.argv[1]
        ws_host = sys.argv[2]

    receiver = Serial(port, baudrate=57600)
    pub = WebsocketPublisher(ws_host)

    while True:
        result = receiver.readline()

        try:
            data = json.loads(result)

            for key in data.keys():
                data[key] = round(exp_average(key, data[key]), 2)

            sys.stdout.write("%.2f => %s\n" % (time.time(), str(data)))
            sys.stdout.flush()

            pub.publish('pressure', data)
        except ValueError:
            pass
