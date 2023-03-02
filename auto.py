import subprocess

output = subprocess.check_output(['v4l2-ctl' , '--list-devices'])
print(output)