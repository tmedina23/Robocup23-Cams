# Robocup'23 - Camera Stream
# BSM Robotics
# Thomas Medina

import subprocess
import cv2
import numpy as np
from pysondb import db

output = subprocess.check_output(['v4l2-ctl', '--list-devices'])
searching_for1 = "HD USB Camera: HD USB Camera"
cams = []
indices = []
semifinal = [999,999]
final = [999,999,999,999]

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start,)
        if start == -1: return
        yield start
        start += len(sub)

instances1 = find_all(str(output), searching_for1)

def init_vars(output):
    for x in range(len(instances1)):
        name = output[instances1:instances1+len(instances1)]
        cams.append(name)
        index = output[instances1+len(instances1)+38:instances1+len(instances1)+40]
        indices.append(index)
        print(name)
        print(index)

def assign():
    for l in range(len(cams)):
        #if claw cam
        if (cams[l] == "HD USB Camera: HD USB Camera"):
            semifinal[0] = indices[l]
            final[0] = indices[l]
        #if front-left cam
        elif (cams[l] == "USB 2.0 Camera: HD USB Camera"):
            semifinal[1] = indices[l]
            final[1] = indices[l]
        #if front-right/back cam
        else:
            semifinal.append(indices[l])

    return semifinal

print(output)
print("\n")
init_vars(output)
print("\n")
print(*cams, sep = ", ")
print("\n")
print(*indices, sep = ", ")
