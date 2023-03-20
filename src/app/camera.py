#!/usr/bin/env python

#https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf
import time
from picamera2 import Picamera2
from libcamera import Transform
from picamera2.encoders import H264Encoder
import argparse
import signal

#--------------------------------------------------------------------#

__author__ = 'Andreas Gising <andreas.gising@ri.se>'
__version__ = '0.1.0'
__copyright__ = 'Copyright (c) 2022, RISE'
__status__ = 'development'

#--------------------------------------------------------------------#

class Camera():
  def __init__(self,output_file, iperiod, duration):
    self.picam2 = Picamera2()
    self.output_file = output_file
    self.iperiod = iperiod
    self.duration = duration
    self.ctrl_c = False

  # A handler for signals
  def handler(self, signum, frame):
    print(signum, frame)
    signame = signal.Signals(signum).name
    print(f'Signal handler received signal {signame}')
    if signame == "SIGINT":
      print("Received Ctrl-C")
      self.ctrl_c = True

  def init_handler(self):
    # Use ctrl-c signal (SIGINT) to stop camera recording
    signal.signal(signal.SIGINT, self.handler)

  def main(self):
    self.init_handler()
    video_config = self.picam2.create_video_configuration(transform=Transform(hflip=True,vflip=True))
    self.picam2.configure(video_config)
    #encoder = H264Encoder(bitrate=50000000, iperiod=1)
    encoder = H264Encoder(iperiod=self.iperiod)

    self.picam2.start_recording(encoder, self.output_file)
    elapsed = 0
    while self.duration > elapsed and not self.ctrl_c:
      time.sleep(1)
      # Precision is good enough for the application
      elapsed += 1
    self.picam2.stop_recording()

  def kill(self):
    self.picam2 = None

#--------------------------------------------------------------------#
def _main():
  # parse command-line arguments
  parser = argparse.ArgumentParser(description='APP "app_noise"', allow_abbrev=False, add_help=False)
  parser.add_argument('-h', '--help', action='help', help=argparse.SUPPRESS)
  parser.add_argument('--output', type=str, help='output file.h264', required=True)
  parser.add_argument('--iperiod', type=int, default=1, help='Intra frames', required=False)
  parser.add_argument('--duration', type=int, default=10, help='rec time in seconds', required=False)

  args = parser.parse_args()

  # Create the camera class
  try:
    cam = Camera(output_file=args.output, iperiod=args.iperiod, duration=args.duration)
  except:
    print(f'Could not fetch camera')
    exit()

  # Try to run main
  try:
    cam.main()
  except KeyboardInterrupt:
    print('Shutdown due to keyboard interrupt', end='\r')

  # Try to kill gracefully
  try:
    cam.kill()
  except:
    print(f'unexpected exception\n{traceback.format_exc()}')


#--------------------------------------------------------------------#
if __name__ == '__main__':
  _main()
