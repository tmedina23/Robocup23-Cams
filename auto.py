import subprocess

output = subprocess.check_output(['v4l2-ctl --list-devices'])
cams = []
indices = []
final = ["notassigned","notassigned","notassigned","notassigned"]

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start,)
        if start == -1: return
        yield start
        start += len(sub)

instances = list(find_all(str(output), "."))

def init_vars(output):
    for x in range(len(instances)):
        name = output[instances[x]-3:instances[x]]
        cams.append(name)
        index = output[instances[x]:instances[x]+3]
        indices.append(index)

def assign():
    for l in range(len(cams)):
        if (cams[l] == "uto"):
            final[0] = indices[l]
        elif (cams[l] == "DME"):
            final[1] = indices[l]
        elif (cams[l] == "app"):
            final[2] = indices[l]

    return final

print(output)
init_vars(output)
print(assign())
