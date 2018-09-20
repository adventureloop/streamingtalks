import asyncio
from aiohttp import web
import json
import random
import os
import time
import struct
import socket
import sys

from collections import deque

wsclients = []

async def handle(request):
    indexpage = None

    with open('index.html', 'r') as indexfile:
        indexpage=indexfile.read()
    return web.Response(text=indexpage, content_type='text/html')

async def wshandler(request):
    print('web socket')
    ws = web.WebSocketResponse(protocols=['SUPERNET'])
    await ws.prepare(request)

    wsclients.append(ws)
   
    async for msg in ws:
        if msg.type == web.MsgType.binary:
            ws.send_bytes(msg.data)
        elif msg.type == web.MsgType.close:
            break
    return ws

async def updatestats(app):
    while True:
        await asyncio.sleep(1)

        # record how many rx/tx bytes since last check
        print('updatestats BRIDGEPPS: {}'.format(BRIDGEPPS))

        # we need to handle disconnects
        closed = []
        for client in wsclients:
            if not client.closed:
                await client.send_str(json.dumps({'internal':[]}))
            else:
                closed.append(client)
        for x in closed:
            wsclients.remove(x)

# next to go we can do this in python now
async def streamsh(app):
    command = os.path.dirname(os.path.realpath(__file__)) + '/stream.sh'

    # Create the subprocess, redirect the standard output into a pipe
    create = asyncio.create_subprocess_shell(command,
        stdout=asyncio.subprocess.PIPE)
    proc = yield create

    print('stream', proc)

    while RUNSTREAM:
        data = yield proc.stdout.readline()
    proc.terminate()

async def streampy(app):
    command = os.path.dirname(os.path.realpath(__file__)) + '/stream.sh'

    # Create the subprocess, redirect the standard output into a pipe
    create = asyncio.create_subprocess_shell(command,
        stdout=asyncio.subprocess.PIPE)
    proc = yield create

    print('stream', proc)

    while RUNSTREAM:
        data = yield proc.stdout.readline()
    proc.terminate()

def stream_cb(pad, info, pdata):
    print('called')
    return Gst.PadProbeReturn.OK

async def stream(app):
    global STREAMPPS
    Gst.init(None)

    pipeline ="flvmux name=muxer streamable=true \
! rtmpsink location='rtmp://bsdstreams-origin.secdn.net/bsdstreams-origin/live/268bf' \
autoaudiosrc \
! audioconvert \
! wavenc \
! wavparse \
! audioconvert ! audioresample \
! audio/x-raw, rate=48000 \
! avenc_aac \
! muxer. \
udpsrc port=5000 \
! tsdemux \
! queue \
! h264parse \
! muxer."

    pipe = Gst.parse_launch(pipeline)
    data = {start: time.time(), interval:1, pkts:0}

    udpsrc = pipe.get_child_by_name('udpsrc0')
    pad = udpsrc.get_static_pad('src')
    pad.add_probe(Gst.PadProbeType.DATA_BOTH, datacb, data)

    loop = app.loop

    bus = pipe.get_bus()
    bus.add_signal_watch()
    bus.connect ("message", bus_call, loop)

    # start play back and listen to events
    pipe.set_state(Gst.State.PLAYING)
    try:
        loop.run()
    except:
        pass


async def bridge(app):
    global BRIDGEPPS

    group = '239.255.42.42'
    mport = 5004

    baddr = '192.168.1.2'
    bport = 5000
    bridgetarget = (baddr, bport)

    # Create a socket
    msock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    msock.bind(('0.0.0.0', mport))
    msock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, 
        socket.inet_aton(group) + socket.inet_aton('192.168.1.2'))

    bsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #bsock.connect(bridgetarget)

    start = time.time()
    count = 0
    while RUNBRIDGE:
        #try:
            data, sender = yield msock.recvfrom(1500)
            print('recv')

            done = time.time()
            if done - start > 1: # 1 second
                start = time.time()
                BRIDGEPPS = count
                count = 0
                print(BRIDGEPPS)
            else:
                count = count + 1

            if BRIDGEFORWARD:
                try: 
                    bsock.sendto(data, bridgetarget)
                except socket.error as e:
                    pass
        #    # we are going to get send errors we don't care
        #    if e.errno != socket.errno.ECONNREFUSED:
        #        print(e)
        #        raise e
        #    pass

async def start_background_tasks(app):
    app['updatestats'] = app.loop.create_task(updatestats(app))

    #app['stream'] = app.loop.create_task(streamsh(app))
    #app['stream'] = app.loop.create_task(streampy(app))
    app['stream'] = app.loop.create_task(stream(app))

    app['bridge'] = app.loop.create_task(bridge(app))

async def cleanup_background_tasks(app):
    app['bridge'].cancel()
    app['stream'].cancel()

    await app['bridge']
    await app['stream']

if __name__ == "__main__":

    RUNSTREAM = True
    RUNBRIDGE = True
    BRIDGEFORWARD = True
    BRIDGEPPS = 0

    app = web.Application()

    app.router.add_static('/d3', "d3")
    app.router.add_static('/css', "css")
    app.router.add_static('/js', "js")
    app.router.add_static('/images', "images")

    app.router.add_get('/ifstatus', wshandler)
    app.router.add_get('/', handle)

    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)

    try:
        print("started webapp")
        web.run_app(app)
    except KeyboardInterrupt:
        print("Received exit, exiting")

        RUNSTREAM = False
        RUNBRIDGE = False

        app.loop.close()
