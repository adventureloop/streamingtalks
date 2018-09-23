#!/usr/bin/env python3

import requests
import time
import json
import sys

url = 'https://api.scaleengine.net/stable/'
apikey = '346EA2FF7E289CEDECA23FA4074C79CC'
cdn = '11255'
app =  'bsd-streams/live'
stream = '268bf'

def usage():
        print('record [start|stop]')
        sys.exit(1)

def startrecording():
    cmd = {
        'command':'recording.start',
        'apikey': apikey,
        'date': int(time.time()),
        'cdn': cdn,
        'app': app,
        'stream': stream
    }
    print(cmd)

    response = requests.post(url, data=json.dumps(cmd))

    print(response.status_code, response.reason)
    print(response.text)

def stoprecording():
    cmd = {
        'command':'recording.stop',
        'apikey': apikey,
        'date': int(time.time()),
        'cdn': cdn,
        'app': app,
        'stream': stream
    }
    print(cmd)
    response = requests.post(url, data=json.dumps(cmd))

    print(response.status_code, response.reason)
    print(response.text)

if __name__ == "__main__":

    if len(sys.argv) != 2:
        usage() 
   
    if sys.argv[1] == 'start':
        stoprecording()
    if sys.argv[1] == 'stop':
        stoprecording()
    else:
        usage() 
