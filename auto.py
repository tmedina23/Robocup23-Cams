import subprocess

output = subprocess.check_output(['usb-devices'])
print(output)