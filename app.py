# Robocup'23 - Camera Stream
# BSM Robotics
# Thomas Medina

from pysondb import db
from flask import Flask, render_template, Response
import cv2
#imports functions from auto.py
import auto

app = Flask(__name__)
camdb = db.getDb("camdb.json")

#database IDs for each camera
claw_id = 277044989003970700
front_left_id = 860846966079555970
front_right_id = 870675630757077322
back_id = 198339096107932300

#use the following command in your terminal to find device numbers
#v4l2-ctl --list-devices
#camera device numbers

#old(v1.0)^^^^^^ instructions
#new version automatically asigns indices

auto.checkUpdate()
final = bool(auto.getindexdb(209847509711096578, True))
if(not final):
    auto.run_auto()
else:
    print("Database Final")

claw_cam = auto.getindexdb(claw_id, False)
front_left = auto.getindexdb(front_left_id, False)
front_right = auto.getindexdb(front_right_id, False)
back = auto.getindexdb(back_id, False)

#get frame from each camera, designate if camera is claw or not
def get_frame(cam_num, claw):
    #set video capture device with device number, variables above
    camera = cv2.VideoCapture(cam_num)

    #camera width
    w=320
    #camera height
    h=240

    camera.set(3,w)
    camera.set(4,h)
    camera.set(cv2.CAP_PROP_FPS, 20)


    while True:
        ret, frame = camera.read()
        if not ret:
            break
        if not claw:
            alpha = 30
            beta = 1
            #sets frame to black and white if not claw camera
            newFrame = cv2.convertScaleAbs(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), alpha, beta)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', newFrame)[1].tobytes() + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes() + b'\r\n\r\n')

#main route
@app.route('/')
def index():
    return render_template('index.html')

#Updates the database to swap the indices 
@app.route('/swap', methods=['GET', 'POST'])
def swap():
    camdb.updateById(front_left_id,{"index":str(front_right)})
    camdb.updateById(front_right_id,{"index":str(front_left)})
    camdb.updateById(209847509711096578,{"index":"True"})
    print("Request recieved: Database updated")
    return render_template('index.html')

#swaps them back
@app.route('/unswap', methods=['GET', 'POST'])
def unswap():
    camdb.updateById(front_left_id,{"index":str(front_left)})
    camdb.updateById(front_right_id,{"index":str(front_right)})
    camdb.updateById(209847509711096578,{"index":"True"})
    print("Request recieved: Database updated")
    return render_template('index.html')

#Route to claw camera
@app.route('/video_feed0')
def video_feed0():
    return Response(get_frame(claw_cam, True), mimetype='multipart/x-mixed-replace; boundary=frame')

#Route to front left camera
@app.route('/video_feed1')
def video_feed1():
    return Response(get_frame(front_left, False), mimetype='multipart/x-mixed-replace; boundary=frame')

#Route to front right camera
@app.route('/video_feed2')
def video_feed2():
    return Response(get_frame(front_right, False), mimetype='multipart/x-mixed-replace; boundary=frame')

#Route to back camera
@app.route('/video_feed3')
def video_feed3():
    return Response(get_frame(back, False), mimetype='multipart/x-mixed-replace; boundary=frame')

#run flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
