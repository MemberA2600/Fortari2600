
f = open("447.txt", "r")
t = f.read()
f.close()

lines = t.replace("\r", "").split("\n")

all = [ [], [], [], [], [], [] ]

for line in lines:
    bytes = line.split(" ")
    bytes.pop(0)
    for num in range(0, 6):
        all[num].append("\tBYTE\t#" + bytes[num] + "\n")

for num in range(0, 6):
    all[num] = "Earth_Part" + str(num-0) + "\n" + "".join(all[num][::-1])


f = open("Earth.asm", "w")
f.write("\n".join(all))
f.close()