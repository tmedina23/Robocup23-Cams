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
pip install pysondb
pip install numpy
```
Note: opencv takes hours to build (no seriously), so make sure you have enough time for it to complete.

## Running onboot.py when the pi boots


## Starting the stream

```
sudo python app.py
```
Once started, enter the IP adress of the device into your web browser to view the stream.

## Known errors

## Swaping Indexes

## Implementation

The Flask app does run independently, but was built to be implementened with a motor controlling Flask app. See https://github.com/vcoppo23/Robocup for an implementation.

Or to implement into your own project, add an image tag to your HTML page and let the source be "http://{ip address of device}/video_feed#" where the number is the video feed you like to implement. Example with multiple cameras:
```
<img src="http://000.000.00.000/video_feed0" title="Front Left">
<img src="http://000.000.00.000/video_feed1" title="Front Right">
<img src="http://000.000.00.000/video_feed2" title="Center Rear">
```
