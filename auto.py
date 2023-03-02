import subprocess

output = subprocess.check_output(['v4l2-ctl' , '--list-devices'])

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)

instances = list(find_all(str(output), "/dev/video", 10))

for x in range(len(instances)):
    substring = output[instances[x]-1:instances[x]+7]
    print(substring)

print(output)