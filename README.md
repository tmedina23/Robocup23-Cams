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
sudo apt-get install v4l-utils
```
Note: opencv takes hours to build (no seriously), so make sure you have enough time for it to complete.

## Running onboot.py when the pi boots
in progress...

## Starting the stream

```
sudo python app.py
```
Once started, enter the IP adress of the device into your web browser to view the stream.

## Swaping Indexes
Two of the cameras (front left and front right) have identical names, so if you notice they aren't in the right spot on the html page you can use the command swap() in the console to visually swap the images on screen, and update the database so it'll stay if you reboot the flask stream. There is also an unswap() function that returns it to the way it was to begin with.

To use the commands, right click anywhere on the page, click on inspect element, then click console at the top of the popup, then type the command swap(), or unswap() with parenthesis and hit enter.

## Implementation

The Flask app does run independently, but was built to be implementened with a motor controlling Flask app. See [the motor control github](https://github.com/vcoppo23/Robocup) for an implementation.

Or to implement into a different project, add an image tag to your HTML page and let the source be "http://{ip address of camera device}/video_feed#" where the number is the video feed you like to implement. Example with multiple cameras:
```
<img src="http://000.000.00.000/video_feed0" title="Front Left">
<img src="http://000.000.00.000/video_feed1" title="Front Right">
<img src="http://000.000.00.000/video_feed2" title="Center Rear">
```

To implement the swap() and unswap() add the following code to the project as a part of the javascript where "000.000.00.000" is the ip address of the camera pi:

```
function swap(){
      document.getElementById("front_left").src="http://000.000.00.000/video_feed2";
      document.getElementById("front_right").src="http://000.000.00.000/video_feed1";
      $.ajax({
				url: 'http://000.000.00.000/swap',
				type: 'POST',
				success: function(response) {
					console.log(response);
				},
				error: function(error) {
					console.log(error);
				}
			});
}
function unswap(){
    document.getElementById("front_left").src="http://000.000.00.000/video_feed1";
    document.getElementById("front_right").src="http://000.000.00.000/video_feed2";
    $.ajax({
		  url: 'http://000.000.00.000/unswap',
		  type: 'POST',
			success: function(response) {
				console.log(response);
			},
			error: function(error) {
				console.log(error);
			}
		});
}
```
