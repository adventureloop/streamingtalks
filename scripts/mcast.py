#!/usr/bin/env python

import time
import struct
import socket
import sys

def main():
    group = '239.255.42.42'
    port = 5004

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.bind(('0.0.0.0', port))

    s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, 
        socket.inet_aton(group) + socket.INADDR_ANY)

    # Loop, printing any data we receive
    while True:
        data, sender = s.recvfrom(1500)
        print (sender, len(data))

if __name__ == '__main__':
    main()
