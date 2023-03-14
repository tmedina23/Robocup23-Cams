# Robocup'23 - Camera Stream
# BSM Robotics
# Thomas Medina

import subprocess
import cv2
import numpy as np
from pysondb import db

output = str(subprocess.check_output(['v4l2-ctl', '--list-devices']))
searching = {"USB 2.0 Camera: HD USB Camera", "HD USB Camera: HD USB Camera", "HD USB Camera: USB Camera"}
cams = []
indices = []
final = [999,999]

def name_index(instance, device):
    name = output[instance:instance+len(device)]
    cams.append(name)
    index = output[instance+len(device)+38:instance+len(device)+39]
    indices.append(index)

def set_arrays():
    for device in searching:
        instance = output.find(device)
        if (device == "HD USB Camera: USB Camera"):
            name_index(instance, device)
            name_index(output.find(device, instance+len(device)+1), device)
        else:
            name_index(instance,device)

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
set_arrays()
print("\n")
print("Name: " + str(instance) +" "+ str(len(searching_for1)))
print(*cams, sep = ", ")
print("\n")
print("Index: " + str(instance+38))
print(*indices, sep = ", ")