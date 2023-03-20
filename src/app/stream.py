#!/usr/bin/env python


#--------------------------------------------------------------------#

__author__ = 'Andreas Gising <andreas.gising@ri.se>'
__version__ = '0.1.0'
__copyright__ = 'Copyright (c) 2022, RISE'
__status__ = 'development'

#--------------------------------------------------------------------#

# See this code as notes rather than anything else..
# Evaluate if this should be added as a method in camera class


from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
from picamera2 import Picamera2
import time

print("Hello")
picam2 = Picamera2()
video_config = picam2.create_video_configuration({"size": (640, 480)})
picam2.configure(video_config)
encoder = H264Encoder(bitrate=1000000, repeat=True, iperiod=15)
# output = FfmpegOutput("-f hls -hls_time 4 -hls_list_size 5 -hls_flags delete_segments -hls_allow_cache 0 stream.m3u8")
print("world")
output = FfmpegOutput("-f dash -window_size 5 -use_template 1 -use_timeline 1 stream.mpd")
picam2.start_recording(encoder, output)
time.sleep(9999999)
print("Tiem is somehow up..")
