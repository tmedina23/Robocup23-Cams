import subprocess

output = subprocess.check_output(['v4l2-ctl' , '--list-devices'])

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)

list(find_all(output, "\n"))

print(output)