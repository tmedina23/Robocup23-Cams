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

camdb=db.getDb("camdb.json")

def name_index(instance, device):
    name = output[instance:instance+len(device)]
    cams.append(name)
    index = output[instance+len(device)+38:instance+len(device)+40]
    if("\\" in index):
        index = output[instance+len(device)+38:instance+len(device)+39]
        indices.append(index)
    else:
        indices.append(index)

def set_arrays():
    for device in searching:
        instance = output.find(device)
        if (device == "HD USB Camera: USB Camera"):
            name_index(instance, device)
            name_index(output.find(device, instance+len(device)+1), device)
        else:
            name_index(instance,device)

def updateDB():
    dupe = False
    for l in range(len(cams)):
        #if claw cam
        if (cams[l] == "HD USB Camera: HD USB Camera"):
            camdb.updateById("277044989003970700",{"index":str(indices[l])})
        #if back cam
        elif (cams[l] == "USB 2.0 Camera: HD USB Camera"):
            camdb.updateById("198339096107932300",{"index":str(indices[l])})
        elif (cams[l] == "HD USB Camera: USB Camera" and dupe == False):
            camdb.updateById("870675630757077322",{"index":str(indices[l])})
            dupe = True
        elif (cams[l] == "HD USB Camera: USB Camera" and dupe == True):
            camdb.updateById("860846966079555970",{"index":str(indices[l])})

def getindexdb(id):
    camdata = str(camdb.getById(id))
    splitcomma = camdata.split(",")[2]
    index1 = splitcomma.split(":")[1]
    index = int(index1.replace("'","").strip())
    return index        

def run_auto():
    print("running subprocess...")
    print("assigning values to variables...")
    set_arrays()
    print("updating database...")
    updateDB()
    print("complete")

run_auto()