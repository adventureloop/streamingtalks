#!/usr/bin/env python

import time
import struct
import socket
import sys

def main():
    group = '239.255.42.42'
    mport = 5004

    baddr = '192.168.1.2'
    bport = 5000
    bridgetarget = (baddr, bport)

    # Create a socket
    msock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bsock.connect(bridgetarget)

    msock.bind(('0.0.0.0', mport))
    msock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, 
        socket.inet_aton(group) + socket.inet_aton('192.168.1.2'))

    # Loop, printing any data we receive
    while True:
        try:
            data, sender = msock.recvfrom(1500)
            if forward:
                bsock.send(data)
        except:
            # we are going to get send errors we don't care
            pass

if __name__ == '__main__':
    main()
