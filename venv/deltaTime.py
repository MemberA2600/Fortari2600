f = open("track.txt", "r")
txt = f.read().replace("\r", "").replace("\t", 8 * " ").split("\n")
f.close()

delta = 0

for line in txt:
    line = line[:11]
    if len(line.replace(" ", "")) == 0: continue
    line = line.split(":")[-1].replace(" ", "")
    try:
       num  = int(line)
    except:
        continue
    if num == 0:continue
    delta += num

print(delta)