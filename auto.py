import subprocess

output = subprocess.check_output(['v4l2-ctl --listdevices'])
print(output)