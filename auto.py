# Robocup'23 - Camera Stream
# BSM Robotics
# Thomas Medina

import subprocess
import cv2
import numpy as np
from pysondb import db

output = subprocess.check_output(['v4l2-ctl', '--list-devices'])
searching_for1 = "media" #+8
searching_for2 = "(" #-2
searching_for3 = ")" #+14
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

instances1 = list(find_all(str(output), searching_for1))
instances2 = list(find_all(str(output), searching_for2))
instances3 = list(find_all(str(output), searching_for3))

def init_vars(output):
    for x in range(len(instances1)):
        name = output[instances1[x]+8:instances2[x]-2]
        cams.append(name)
        index = output[instances3[x]+14:instances3[x]+15]
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
print(assign())
