# rise_camera
## Direct control
Simple code snippets for starting and stopping videorecording on remote raspberry pi via ssh, implemented as bash scripts. Current implementation requires that the output filename ends in .h264.

Set up the raspberry pi camera in non legacy mode
sudo raspi-config
select interface opt
select camera
select non legacy option
save and reboot

Check out the code and test the camera app
```
python3 camera.py --output=my_file.h264 --duration=10
```

## Remote controlling
Now test to start and stop video recording from remote host.
Setup a ssh config such as the remote can be reached without password input. Edit .ssh/config to look something like this. It this case Hostname 'my_pi' is defined in /etc/hosts:

```
Host ssh_to_my_pi
    Hostname my_pi
    IdentityFile ~/.ssh/id_rsa
    IdentitiesOnly yes
    User my_username
```

Check out the code.
Execute the start cam script.
```
./start_cam.sh -i ssh_to_my_pi -d 10 -o test.h264
```

If you want to stop recording in advance, open an other terminal and execute stop script
```
./stop_cam.sh -i ssh_to_my_pi
```

# live stream
To also enable live streaming, we use the open source project mediamtx (earlier rtsp-simple-server), https://github.com/bluenviron/mediamtx


Setup camera as non legacy camera, (should already be done).
Sudo Raspi-config, interfaces, camera, non-legacy. Reboot.

Get binary from release page, extract it. This binary is for a RaspberryPi4 with 64-bit OS.
```
wget -c  https://github.com/bluenviron/mediamtx/releases/download/v1.0.0/mediamtx_v1.0.0_linux_arm64v8.tar.gz -O - | tar -xz
```

This outdated version whats is tested earliers and works good for the Raspberry 3Bplus, 32bit OS, but try the 1+ versions first..
```
wget -c  https://github.com/aler9/rtsp-simple-server/releases/download/v0.21.6/rtsp-simple-server_v0.21.6_linux_armv7.tar.gz -O - | tar -xz
```


Move binary to /usr/local/bin/

Move config (.yml) to /usr/local/etc/

Edit config file. Set parameters to make server not occupying the camera if noone looks at the stream.

An example of paths-section in the config file follows, 'stream' relates to the web adress the stream will appear on. Only one set of config paramters per source is allowed. Replace the path 'all' with 'stream' as below.

```
paths:
  stream:
    source: rpiCamera
    sourceOnDemand: yes
    # If sourceOnDemand is "yes", readers will be put on hold until the source is
    # ready or until this amount of time has passed.
    sourceOnDemandStartTimeout: 10s
    # If sourceOnDemand is "yes", the source will be closed when there are no
    # readers connected and this amount of time has passed.
    sourceOnDemandCloseAfter: 3s
    # If the source is "rpiCamera", these are the Raspberry Pi Camera parameters.
    # ID of the camera
    rpiCameraCamID: 0
    # width of frames
    rpiCameraWidth: 1920
    # height of frames
    rpiCameraHeight: 1080
    # flip horizontally
    rpiCameraHFlip: false
    # flip vertically
    rpiCameraVFlip: false
    # brightness [-1, 1]
    rpiCameraBrightness: 0
    # contrast [0, 16]
    rpiCameraContrast: 1
    # saturation [0, 16]
    rpiCameraSaturation: 1
    # sharpness [0, 16]
    rpiCameraSharpness: 1
    # exposure mode.
    # values: normal, short, long, custom
    rpiCameraExposure: normal
    # auto-white-balance mode.
    # values: auto, incandescent, tungsten, fluorescent, indoor, daylight, cloudy, custom
    rpiCameraAWB: auto
    # denoise operating mode.
    # values: off, cdn_off, cdn_fast, cdn_hq
    rpiCameraDenoise: "off"
    # fixed shutter speed, in microseconds.
    rpiCameraShutter: 0
    # metering mode of the AEC/AGC algorithm.
    # values: centre, spot, matrix, custom
    rpiCameraMetering: centre
    # fixed gain
    rpiCameraGain: 0
    # EV compensation of the image [-10, 10]
    rpiCameraEV: 0
    # Region of interest, in format x,y,width,height
    rpiCameraROI:
    # tuning file
    rpiCameraTuningFile:
    # sensor mode, in format [width]:[height]:[bit-depth]:[packing]
    # bit-depth and packing are optional.
    rpiCameraMode:
    # frames per second
    rpiCameraFPS: 30
    # period between IDR frames
    rpiCameraIDRPeriod: 60
    # bitrate
    #rpiCameraBitrate: 1000000
    rpiCameraBitrate: 5000000
    # H264 profile
    rpiCameraProfile: main
    # H264 level
    rpiCameraLevel: '4.1'
    # Autofocus mode
    # values: auto, manual, continuous
    rpiCameraAfMode: auto
    # Autofocus range
    # values: normal, macro, full
    rpiCameraAfRange: normal
    # Autofocus speed
    # values: normal, fast
    rpiCameraAfSpeed: normal
    # Lens position (for manual autofocus only), will be set to focus to a specific distance
    # calculated by the following formula: d = 1 / value
    # Examples: 0 moves the lens to infinity.
    #           0.5 moves the lens to focus on objects 2m away.
    #           2 moves the lens to focus on objects 50cm away.
    rpiCameraLensPosition: 0.0
    # Specifies the autofocus window, in the form x,y,width,height where the coordinates
    # are given as a proportion of the entire image.
    rpiCameraAfWindow:

    # Username required to publish.
    # SHA256-hashed values can be inserted with the "sha256:" prefix.
    publishUser:
    # Password required to publish.
    # SHA256-hashed values can be inserted with the "sha256:" prefix.
    publishPass:
    # IPs or networks (x.x.x.x/24) allowed to publish.
    publishIPs: []

    # Username required to read.
    # SHA256-hashed values can be inserted with the "sha256:" prefix.
    readUser:
    # password required to read.
    # SHA256-hashed values can be inserted with the "sha256:" prefix.
    readPass:
    # IPs or networks (x.x.x.x/24) allowed to read.
    readIPs: []

    # Command to run when this path is initialized.
    # This can be used to publish a stream and keep it always opened.
    # This is terminated with SIGINT when the program closes.
    # The following environment variables are available:
    # * RTSP_PATH: path name
    # * RTSP_PORT: server port
    # * G1, G2, ...: regular expression groups, if path name is
    #   a regular expression.
    runOnInit:
    # Restart the command if it exits suddenly.
    runOnInitRestart: no

    # Command to run when this path is requested.
    # This can be used to publish a stream on demand.
    # This is terminated with SIGINT when the path is not requested anymore.
    # The following environment variables are available:
    # * RTSP_PATH: path name
    # * RTSP_PORT: server port
    # * G1, G2, ...: regular expression groups, if path name is
    #   a regular expression.
    runOnDemand:
    # Restart the command if it exits suddenly.
    runOnDemandRestart: no
    # Readers will be put on hold until the runOnDemand command starts publishing
    # or until this amount of time has passed.
    runOnDemandStartTimeout: 10s
    # The command will be closed when there are no
    # readers connected and this amount of time has passed.
    runOnDemandCloseAfter: 10s

    # Command to run when the stream is ready to be read, whether it is
    # published by a client or pulled from a server / camera.
    # This is terminated with SIGINT when the stream is not ready anymore.
    # The following environment variables are available:
    # * RTSP_PATH: path name
    # * RTSP_PORT: server port
    # * G1, G2, ...: regular expression groups, if path name is
    #   a regular expression.
    runOnReady:
    # Restart the command if it exits suddenly.
    runOnReadyRestart: no

    # Command to run when a clients starts reading.
    # This is terminated with SIGINT when a client stops reading.
    # The following environment variables are available:
    # * RTSP_PATH: path name
    # * RTSP_PORT: server port
    # * G1, G2, ...: regular expression groups, if path name is
    #   a regular expression.
    runOnRead:
    # Restart the command if it exits suddenly.
    runOnReadRestart: no
```

These are the crucial settings for not occupying the camera more than wanted. We cannot stream and record to file, so we want the streaming service to let go of the resource when not in use. Streaming and recording can be achieved if streaming in steps.
```
    sourceOnDemand: yes
    # If sourceOnDemand is "yes", readers will be put on hold until the source is
    # ready or until this amount of time has passed.
    sourceOnDemandStartTimeout: 10s
    # If sourceOnDemand is "yes", the source will be closed when there are no
    # readers connected and this amount of time has passed.
    sourceOnDemandCloseAfter: 3s
```
Make sure to upgrade to latest 'libcamera' release

```sudo apt update && sudo apt install libcamera0```

Create service:
```
sudo tee /etc/systemd/system/mediamtx.service >/dev/null << EOF
[Unit]
After=network.target
[Service]
ExecStart=/usr/local/bin/mediamtx /usr/local/etc/mediamtx.yml
[Install]
WantedBy=multi-user.target
EOF
```

Start service to test
```
sudo systemctl start mediamtx.service
```

If succesful enable the service
```
sudo systemctl enable mediamtx.service
```

Look at stream at http://ip_of_the_pi:8889/stream/
