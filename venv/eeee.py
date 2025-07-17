f = open("C:/Users/Member/Desktop/Lakások.csv", "r")
lines = f.read().split("\n")
f.close()

datas  = {}
datas2 = {}

lineNum = -1
keys   = []

for line in lines:
    lineNum += 1

    if lineNum in (0, 2, 42): continue

    line = line.split(";")

    if line == [] or line == ['']: continue

    if lineNum == 1:
       while "" in line:
            line.remove("")

       for item in line:
           keys.append(item)

    else:
        if line[0] not in datas:
           datas[line[0]] = []
           d    = datas
        else:
           datas2[line[0]] = []
           d    = datas2

        skip = True
        for item in line:
            if skip:
               skip = False
               continue
            d[line[0]].append(item)



toOut = ";"
for key in keys:6
    toOut += key + " - 2011;"
    toOut += key + " - 2022;"
toOut = toOut[:-1] + "\n"

for key in datas:
    toOut += key + ";"
    for itemNum in range(0, len(datas[key])):
        toOut += datas2[key][itemNum]  + ";"
        toOut += datas [key][itemNum] + ";"
    toOut = toOut[:-1] + "\n"

f = open("C:/Users/Member/Desktop/Lakások2.csv", "w")
f.write(toOut)
f.close()