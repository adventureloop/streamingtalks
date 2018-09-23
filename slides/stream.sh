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

# mux together the rtlsdr and the unicast feed to an rtmp stream
sudo rtl_fm -M am -f 229.7M -s 15k -l 150 -E swagc \
        | gst-launch-1.0 -e \
        flvmux name=muxer streamable=true \
        ! rtmpsink location='rtmp://bsdstreams-origin.secdn.net/bsdstreams-origin/live/268bf' \
        fdsrc \
        ! audio/x-raw, format=S16LE, channels=1, layout=interleaved, rate=15000 \
        ! audioconvert ! audioresample \
        ! audio/x-raw, rate=4000 \
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

# rtmp stream the mixer unicast feed
gst-launch-1.0 -e \
        flvmux name=muxer streamable=true \
        ! rtmpsink location='rtmp://bsdstreams-origin.secdn.net/bsdstreams-origin/live/268bf' \
        udpsrc port=5000 \
        ! 'video/mpegts, systemstream=(boolean)true, packetsize=(int)1318' \
        ! tsdemux \
        ! 'video/x-h264' \
        ! queue \
        ! h264parse \
        ! muxer.
exit

# rtmp stream the audio only
sudo rtl_fm -M am -f 229.7M -s 15k -l 150 -E swagc \
        | gst-launch-1.0 -e \
        flvmux name=muxer streamable=true \
        ! rtmpsink location='rtmp://bsdstreams-origin.secdn.net/bsdstreams-origin/live/268bf' \
        fdsrc \
        ! audio/x-raw, format=S16LE, channels=1, layout=interleaved, rate=15000 \
        ! audioconvert ! audioresample \
        ! audio/x-raw, rate=4000 \
        ! wavenc \
        ! wavparse \
        ! audioconvert ! audioresample \
        ! audio/x-raw, rate=48000 \
        ! avenc_aac \
	! muxer. \
exit

# mux together the rtlsdr source and the udp unicast feed into an mp4
sudo rtl_fm -M am -f 229.7M -s 15k -l 150 -E swagc \
        | gst-launch-1.0 -e \
        mp4mux name=muxer\
        ! filesink location=foo.mp4 
        fdsrc \
        ! audio/x-raw, format=S16LE, channels=1, layout=interleaved, rate=15000 \
        ! audioconvert ! audioresample \
        ! audio/x-raw, rate=4000 \
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
# take the rtlsdr audio and turn it into aac
sudo rtl_fm -M am -f 229.7M -s 15k -l 150 -E swagc \
        | gst-launch-1.0 -e fdsrc \
        ! audio/x-raw, format=S16LE, channels=1, layout=interleaved, rate=15000 \
        ! audioconvert ! audioresample \
        ! audio/x-raw, rate=4000 \
        ! wavenc \
        ! wavparse \
        ! audioconvert ! audioresample \
        ! audio/x-raw, rate=48000 \
        ! avenc_aac \
        ! mp4mux \
        ! filesink location=foo.mp4
exit

# take the unicast feed and turn it into an mp4
gst-launch-1.0 \
        udpsrc port=5000 \
        ! 'video/mpegts, systemstream=(boolean)true, packetsize=(int)1318' \
        ! tsdemux \
        ! 'video/x-h264' \
        ! queue \
        ! h264parse \
        ! mp4mux \
        ! filesink location=test.mp4
exit

# mux together audio and video save to file
sudo rtl_fm -M am -f 229.7M -s 15k -l 150 -E swagc \
        | gst-launch-1.0 -e fdsrc \
        ! audio/x-raw, format=S16LE, channels=1, layout=interleaved, rate=15000 \
        ! audioconvert ! audioresample \
        ! audio/x-raw, rate=4000 \
        ! wavenc \
        ! wavparse \
        ! audioconvert ! audioresample \
        ! audio/x-raw, rate=48000 \
        ! avenc_aac \
        ! mp4mux name=muxer \
        ! filesink location=foo.mp4 \
        ! udpsrc port=5000 \
        ! 'video/mpegts, systemstream=(boolean)true, packetsize=(int)1318' \
        ! tsdemux \
        ! 'video/x-h264' \
        ! queue \
        ! h264parse \
        ! muxer.
exit
