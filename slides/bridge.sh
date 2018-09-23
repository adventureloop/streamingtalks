#!/bin/sh

socat UDP4-RECV:5004,ip-add-membership=239.255.42.42:192.168.1.2 STDOUT | nc -u 192.168.1.2 5000

