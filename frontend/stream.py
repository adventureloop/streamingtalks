#!/usr/bin/env python3

'''
Simple example to demonstrate dynamically adding and removing source elements
to a playing pipeline.
'''

import sys
import random

import gi
gi.require_version('Gst', '1.0')
gi.require_version('GLib', '2.0')
gi.require_version('GObject', '2.0')
from gi.repository import GLib, GObject, Gst

class ProbeData:
    def __init__(self, pipe, src):
        self.pipe = pipe
        self.src = src

def bus_call(bus, message, loop):
    t = message.type
    if t == Gst.MessageType.EOS:
        sys.stdout.write("End-of-stream\n")
        loop.quit()
    elif t == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        sys.stderr.write("Error: %s: %s\n" % (err, debug))
        loop.quit()
    return True

def dispose_src_cb(src):
    src.set_state(Gst.State.NULL)

def probe_cb(pad, info, pdata):
    peer = pad.get_peer()
    pad.unlink(peer)
    pdata.pipe.remove(pdata.src)
    # Can't set the state of the src to NULL from its streaming thread
    GLib.idle_add(dispose_src_cb, pdata.src)

    pdata.src = Gst.ElementFactory.make('videotestsrc')
    pdata.src.props.pattern = random.randint(0, 24)
    pdata.pipe.add(pdata.src)
    srcpad = pdata.src.get_static_pad ("src")
    srcpad.link(peer)
    pdata.src.sync_state_with_parent()

    GLib.timeout_add_seconds(1, timeout_cb, pdata)

    return Gst.PadProbeReturn.REMOVE

def timeout_cb(pdata):
    srcpad = pdata.src.get_static_pad('src')
    srcpad.add_probe(Gst.PadProbeType.IDLE, probe_cb, pdata)
    return GLib.SOURCE_REMOVE

def viewpipelinedata_cb(pad, info, pdata):
    print(pdata + ': data')
    return Gst.PadProbeReturn.OK

def streampipelinedata_cb(pad, info, pdata):
    print(pdata + ': data')
    return Gst.PadProbeReturn.OK

def viewvideopipeline(datacb):
    pipeline = "udpsrc port=5000 \
! tsdemux \
! queue \
! h264parse \
! avdec_h264 \
! autovideosink"

    print(pipeline)
    pipe = Gst.parse_launch(pipeline) 

    udpsrc = pipe.get_child_by_name('udpsrc0')
    print(udpsrc)
    pad = udpsrc.get_static_pad('src')
    pad.add_probe(Gst.PadProbeType.DATA_BOTH, datacb, 'view cb')

    return pipe

def streamvideopipeline(datacb):
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

    print(pipeline)
    pipe = Gst.parse_launch(pipeline) 

    udpsrc = pipe.get_child_by_name('udpsrc0')
    print(udpsrc)
    pad = udpsrc.get_static_pad('src')
    pad.add_probe(Gst.PadProbeType.DATA_BOTH, datacb, 'stream')

    return pipe

def muxdpipeline():
    pipe = Gst.Pipeline.new('muxd')

def main(args):
    GObject.threads_init()
    Gst.init(None)

    pipe = streamvideopipeline(streampipelinedata_cb)

    loop = GObject.MainLoop()

    bus = pipe.get_bus()
    bus.add_signal_watch()
    bus.connect ("message", bus_call, loop)
   
    # start play back and listen to events
    pipe.set_state(Gst.State.PLAYING)
    try:
      loop.run()
    except:
      pass
    
    # cleanup
    pipe.set_state(Gst.State.NULL)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
