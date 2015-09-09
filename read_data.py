import json
import sys
import time

from sensorrelay import WebsocketPublisher
from serial import Serial
from serial.tools import list_ports


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

            sys.stdout.write(str(time.time()) + " => " + result)
            sys.stdout.flush()

            pub.publish('pressure', data)
        except ValueError:
            pass
