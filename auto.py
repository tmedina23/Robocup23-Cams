# Robocup'23 - Camera Stream
# BSM Robotics
# Thomas Medina

import subprocess
import cv2
import numpy as np
from pysondb import db

output = str(subprocess.check_output(['v4l2-ctl', '--list-devices']))
searching_for1 = "USB 2.0 Camera: HD USB Camera"
cams = []
indices = []
final = [999,999]

instance = output.find(searching_for1)

def init_vars():
    name = output[instance:instance+len(searching_for1)]
    cams.append(name)
    index = output[instance+len(searching_for1)+38:instance+len(searching_for1)+39]
    indices.append(index)

def init_vars_split():
    split_newline = output.split('\n\n')
    for x in split_newline:
        name = x.split(" (")[0]
        index = x.split("video")[1]
        cams.append(name)
        indices.append(index)

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

print("Testing Og way:")
print("\n")
print(output)
init_vars()
print("\n")
print("Name: " + str(instance) +" "+ str(len(searching_for1)))
print(*cams, sep = ", ")
print("\n")
print("Index: " + str(instance+38))
print(*indices, sep = ", ")