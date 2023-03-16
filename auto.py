# Robocup'23 - Camera Stream
# BSM Robotics
# Thomas Medina

import subprocess
import cv2
import numpy as np
from pysondb import db

#Runs the command and saves the output
output = str(subprocess.check_output(['v4l2-ctl', '--list-devices']))
output_ls = str(subprocess.check_output(['lsusb']))
#System names for each camera device
searching = {"USB 2.0 Camera: HD USB Camera", "HD USB Camera: HD USB Camera", "HD USB Camera: USB Camera"}
#names of each camera get saved here
cams = []
#index of each camera get saved here
indices = []

#get the databse
camdb=db.getDb("camdb.json")

#helper function
def name_index(instance, device):
    name = output[instance:instance+len(device)]
    cams.append(name)
    index = output[instance+len(device)+38:instance+len(device)+40]
    if("\\" in index):
        index = output[instance+len(device)+38:instance+len(device)+39]
        indices.append(index)
    else:
        indices.append(index)

#Sets the arrays using data from the subprocess command
def set_arrays():
    for device in searching:
        instance = output.find(device)
        if (device == "HD USB Camera: USB Camera"):
            name_index(instance, device)
            name_index(output.find(device, instance+len(device)+1), device)
        else:
            name_index(instance,device)

#Updates the database using database ids and arrays
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

#function not used in this file, helper function for app.py
def getindexdb(id, ret_string):
    camdata = str(camdb.getById(id))
    splitcomma = camdata.split(",")[2]
    index1 = splitcomma.split(":")[1]
    if(ret_string):
        index = index1.replace("'","").strip()
    else:
        index = int(index1.replace("'","").strip())
    return index     

#check for changes in device_number using "lsusb"
def checkUpdate():
    print(output_ls)
    all_devices = output_ls.split("\n")
    for x in range(len(all_devices)):
        presliced = all_devices[x].split(":")[0]
        print(presliced)
        dev_number = int(presliced[-2:])
        print(dev_number)
        if(dev_number > getindexdb(283699290575417516,False)):
            camdb.updateById(209847509711096578,{"index":"False"})
            camdb.updateById(283699290575417516,{"index":dev_number})

#runs everthing at once
def run_auto():
    print("running subprocess...")
    print("assigning values to variables...")
    set_arrays()
    print("updating database...")
    updateDB()
    print("complete")

checkUpdate()