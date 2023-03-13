# Robocup'23 - Camera Stream
# BSM Robotics
# Thomas Medina

import subprocess
import cv2
import numpy as np
from pysondb import db

output = subprocess.check_output(['v4l2-ctl', '--list-devices'])
searching_for1 = "USB 2.0 Camera: HD USB Camera"
cams = []
indices = []
final = [999,999]

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start,)
        if start == -1: return
        yield start
        start += len(sub)

instances1 = list(find_all(str(output), searching_for1))

def init_vars(output):
    for x in range(len(instances1)):
        name = output[instances1[x]:instances1[x]+len(searching_for1)]
        cams.append(name)
        index = output[instances1[x]+len(searching_for1)+38:instances1[x]+len(searching_for1)+40]
        indices.append(index)
        print(name)
        print(index)

def assign():
    for l in range(len(cams)):
        #if claw cam
        if (cams[l] == "HD USB Camera: HD USB Camera"):
            final[0] = indices[l]
        #if front-left cam
        elif (cams[l] == "USB 2.0 Camera: HD USB Camera"):
            final[1] = indices[l]
        #if front-right/back cam
        else:
            final.append(indices[l])

    return final

print(str(output))
print("\n")
init_vars(output)
print("\n")
print(*cams, sep = ", ")
print("\n")
print(*indices, sep = ", ")
