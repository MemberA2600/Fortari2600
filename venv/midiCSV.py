f = open("C:\\breeze04.csv", "r")
data = f.read().replace("\r", "").split("\n")
f.close()

for line in data:
    line = line.split(",")
    if len(line) > 2:
       if line[2].startswith(" Note_"):
          note = int(line[3])
          vol  = int(line[4])

