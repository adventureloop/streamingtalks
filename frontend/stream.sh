#!/bin/sh

# mux together the audio in and the unicast feed to an rtmp stream
gst-launch-1.0 -e \
        flvmux name=muxer streamable=true \
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
        ! 'video/mpegts, systemstream=(boolean)true, packetsize=(int)1318' \
        ! tsdemux \
        ! 'video/x-h264' \
        ! queue \
        ! h264parse \
        ! muxer.
exit
