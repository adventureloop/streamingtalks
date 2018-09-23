import plt
import sys

import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5000
bridgehost = (UDP_IP, UDP_PORT)

def bridgemulticast(interface):

    bridgesocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    bridgesocket.connect(bridgehost)

    print("capturing on {}".format(interface))
    trace = plt.trace('bpf:{}'.format(interface))
    
    #capturefilter = 'multicast and host 239.255.42.42 and port 5004'
    capturefilter = 'udp and port 5004'
    capfilter = plt.filter(capturefilter)
    trace.conf_filter(capfilter)
    trace.conf_promisc(True)

    trace.start()

    try:
        for pkt in trace:
            hdr = pkt.udp
            if not hdr:
                continue

             

            data = pkt.udp_payload.data
            print(type(data))
            if not data:
                continue
            if len(data) < 1000:
                continue

            try:
                s = bridgesocket.send(data)
                print('sent ', s)
            except:
                pass

    except KeyboardInterrupt:
        trace.close()
        sys.exit()

if __name__ == "__main__":
    bridgemulticast('ue0')
