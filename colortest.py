# importing required libraries
import cv2
import numpy as np
from flask import Flask, render_template, Response
import threading

app = Flask(__name__)

# taking the input from webcam
vid = cv2.VideoCapture(6)

# running while loop just to make sure that
# our program keep running until we stop it
def get_frame(cam_num):
    camera = cv2.VideoCapture(cam_num)
    while True:
        ret, frame = camera.read()
        if not ret:
            break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes() + b'\r\n\r\n')
	
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(get_frame(6), mimetype='multipart/x-mixed-replace; boundary=frame')

def run_thread(target, *args):
    thread = threading.Thread(target=target, args=args)
    thread.start()

def test():
	while True:

		# capturing the current frame
		_, frame = vid.read()

		# setting values for base colors
		b = frame[:, :, :1]
		g = frame[:, :, 1:2]
		r = frame[:, :, 2:]

		# computing the mean
		b_mean = np.mean(b)
		g_mean = np.mean(g)
		r_mean = np.mean(r)

		# displaying the most prominent color
		if (b_mean > g_mean and b_mean > r_mean):
			print("Blue")
		if (g_mean > r_mean and g_mean > b_mean):
			print("Green")
		else:
			print("Red")


if __name__ == '__main__':
    run_thread(test)
    run_thread(app.run, "host='0.0.0.0'", "port=80")