f = open("C:/Users/Member/Desktop/Települések.csv", "r")
lines = f.read().split("\n")
f.close()

bigData = {}
keys = []
smallDate = {}

skip = 2

for line in lines:
    if skip > 0:
       skip -= 1
       continue

    line = line.split(";")
    while "" in line:
        line.remove("")

    if   len(line) == 0: continue
    if   len(line) == 1: bigData[line[0]] = {}
    else:
         if line[0] not in keys:
            keys.append(line[0])
            smallDate[line[0]] = []
         smallDate[line[0]].append([line[1], line[2]])

keys.sort()

index = -1
for bigKey in bigData.keys():
    index += 1
    for key in keys:
        bigData[bigKey][key] = smallDate[key][index]

lastData = {}
for key in bigData:
    lastData[key + " - 2011"] = {}
    lastData[key + " - 2022"] = {}

    for subKey in bigData[key]:
        lastData[key + " - 2011"][subKey] = bigData[key][subKey][0].replace(" ","")
        lastData[key + " - 2022"][subKey] = bigData[key][subKey][1].replace(" ","")

textToPrint = ";"
for key in lastData:
    textToPrint += key + ";"

textToPrint = textToPrint[:-1] + "\n"

for subKey in keys:
    textToPrint += subKey + ";"
    for key in lastData:
        textToPrint += lastData[key][subKey] + ";"

    textToPrint = textToPrint[:-1] + "\n"

file = open("C:/Users/Member/Desktop/Települések2.csv", "w")
file.write(textToPrint)
file.close()