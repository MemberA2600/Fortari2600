f = open("D:\PyCharm\P\\toDelete\\forTest44\pacaltext.txt", "r")
lines = f.read().replace("\r", "").split("\n")
f.close()

newLines = []

for line in lines:
    while len(line)%8 > 0: line+="0"
    newLines.insert(0, line)


segments = []
pointers = "#NAME#_ScrollingPlayfield_PointerTable\n"

for segmentNum in range(0, len(newLines[0])//8 + 1):
    currentName = "#NAME#_ScrollingPlayfield_"+str(segmentNum)
    segments.append(currentName +"\n")
    pointers+= "\tBYTE\t#<"+currentName+"\n\tBYTE\t#>" + currentName + "\n"

    if segmentNum == len(newLines[0])//8: break

    for line in newLines:
        startIndex = segmentNum * 8
        byte = line[startIndex : startIndex + 8]
        byte = "\tBYTE\t#%" + byte + "\n"
        segments[-1] += byte

print(pointers +"\n" + "\n".join(segments))