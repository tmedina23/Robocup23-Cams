# Robocup'23 - Camera Stream
# BSM Robotics
# Thomas Medina

import subprocess
import cv2
import numpy as np
from pysondb import db

#Runs the command and saves the output
#if you don't know what happens when you run these commands, please try them on your own.
output = str(subprocess.check_output(['v4l2-ctl', '--list-devices']))
output_ls = str(subprocess.check_output(['lsusb']))
output_ip = str(subprocess.check_output(['ifconfig']))
#System names for each of the camera devices we are looking for
#There are only 3 names instead of four because 2 cameras will have the same name
searching = {"USB 2.0 Camera: HD USB Camera", "HD USB Camera: HD USB Camera", "HD USB Camera: USB Camera"}
#names of each camera get saved here
cams = []
#index of each camera get saved here
indices = []

#get the databse
camdb=db.getDb("camdb.json")

#helper function
#Splices the 'output' to find the name of the device and the index.
def name_index(instance, device):
    #instance is the index of the device name, .find is passed as an argument
    name = output[instance:instance+len(device)]
    #add that to the end of the cams array
    cams.append(name)
    #finds the index of the using the device name
    #index is always 38 characters after the end of the device name
    index = output[instance+len(device)+38:instance+len(device)+40]
    #if the index is one character
    if("\\" in index):
        index = output[instance+len(device)+38:instance+len(device)+39]
        indices.append(index)
    #if the index is two characters
    else:
        indices.append(index)

#Sets the arrays using data from the subprocess command
#this is where the name_index function gets used
def set_arrays():
    #for each of the 3 device names
    for device in searching:
        #the index of the device name
        instance = output.find(device)
        #if the name is the duplicate name
        if (device == "HD USB Camera: USB Camera"):
            #finds the index twice
            name_index(instance, device)
            name_index(output.find(device, instance+len(device)+1), device)
        else:
            #just once
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
            camdb.updateById("860846966079555970",{"index":str(indices[l])})
            dupe = True
        elif (cams[l] == "HD USB Camera: USB Camera" and dupe == True):
            camdb.updateById("870675630757077322",{"index":str(indices[l])})

#function not used in this file, helper function for app.py
#pass the second argument as True to pass the index as a string
def getindexdb(id, ret_string):
    camdata = str(camdb.getById(id))
    #{"name": "final","pos": "final","index": "False","id": 209847509711096578}
    splitcomma = camdata.split(",")[2]
    #"index": "False"
    index1 = splitcomma.split(":")[1]
    # "False"
    if(ret_string):
        #False
        index = index1.replace("'","").strip()
    else:
        index = int(index1.replace("'","").strip())
    return index     

#check for changes in device_number using "lsusb"
def checkUpdate():
    #split by row
    all_devices = output_ls.split("\\n")
    #highest device number
    highest = 0
    #for each line in the output
    for x in range(len(all_devices)-1):
        #splice to find the device number
        presliced = all_devices[x].split(":")[0]
        dev_number = int(presliced[-2:])
        #saves the highest device number by the end of the loop
        if(dev_number > highest):
            highest = dev_number
    print("Current Highest Device Number: " + str(highest))
    #if the most recent highest device number is greater than the one saved in the database
    if(highest > getindexdb(283699290575417516, False)):
        #update the db
        camdb.updateById(209847509711096578,{"index":"False"})
        camdb.updateById(283699290575417516,{"index":highest})
        print("Database Updated: New highest dev_number")
    else:
        #sets the final value to true
        print("No database changes made")
        camdb.updateById(209847509711096578,{"index":"True"})

def ip():
    index = output_ip.find('inet 192')
    ip = output_ip[index+5:index+19]
    camdb.updateById(252889469432313574,{"index":ip})
    print("updated ip")

#runs everthing at once
def run_auto():
    print("running subprocess...")
    print("assigning values to variables...")
    set_arrays()
    print("updating database...")
    updateDB()
    print("complete")
