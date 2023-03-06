import subprocess

output = subprocess.check_output(['v4l2-ctl', '--list-devices'])
searching_for1 = "media" #+8
searching_for2 = "(" #-2
searching_for3 = ")" #+14
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

instances1 = list(find_all(str(output), searching_for1))
instances2 = list(find_all(str(output), searching_for2))
instances3 = list(find_all(str(output), searching_for3))

def init_vars(output):
    for x in range(len(instances2)):
        name = output[instances1[x]+8:instances2[x]-2]
        cams.append(name)
        index = output[instances3[x]+14:instances3[x]+15]
        indices.append(index)
        print(name + " " + str(index))

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
print("\n")
init_vars(output)
print("\n")
print(assign())
