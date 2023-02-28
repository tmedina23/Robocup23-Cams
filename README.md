# Robocup23-Cams
## BSM Robotics
### Thomas Medina '23

Built for the ___ robot for Robocup 2023 in Bordeaux, France.

Built to run on a Raspberry Pi but can also be used on other devices.
Runs 4 Cameras simultaneously using opencv, and streams them locally to a flask page.

## Cloning Repository

```
git clone https://github.com/tmedina23/Robocup23-Cams.git
```

## Installing Dependencies

```
pip install Flask
pip install opencv-python
```
Note: opencv takes a long time to build, so make sure you have enough time for it to complete.

## Starting the stream

```
sudo python app.py
```
Once started, enter the IP adress of the device into your web browser to view the stream.

## Fiding and correcting the cameras

Before Starting the stream you will need to change the device numbers in app.py:
While cameras are pluged in, use the following command to find the device numbers for each of the cameras
```
v4l2-ctl --list-devices
```
The ouput should look like this, one for each device and with different numbers:
```
HD USB Camera: HD USB Camera (usb-3f980000.usb-1.2):
	/dev/video0
	/dev/video1
	/dev/media3
```
Take the top number (eg. "0" from "/dev/video0") for each camera and assign it to the variables as seen below. Then run the code and make sure each camera is in the right spot or adjust as needed.
```
#camera device numbers
front_left = 0
front_right = 4
claw_cam = 17
back = 8
```

## Implementation

The Flask app does run independently, but was built to be implementened with a motor controlling Flask app. See (The motor control github)[https://github.com/vcoppo23/Robocup] for an implementation.

Or to implement into your own project, add an image tag to your HTML page and let the source be "http://{ip address of device}/video_feed#" where the number is the video feed you like to implement. Example with multiple cameras:
```
<img src="http://000.000.00.000/video_feed0" title="Front Left">
<img src="http://000.000.00.000/video_feed1" title="Front Right">
<img src="http://000.000.00.000/video_feed2" title="Center Rear">
```
