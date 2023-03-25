f = open("loadThis.txt", "r")
lines = f.read().replace("\r", "").split("\n")
f.close()

byteData = []
oneSample  = 1487.0 / 65535.0
oneCycle   = 0.56
oneNTSCFrame = 63.5
onePALFrame  = 64
decimals   = 0
waitOp     = "$00"
firstByte  = "\t; Register"
secondByte = "\t; Reg. Data- !!!"
waitCode   = "\t; Wait"
waitNum    = "\t; of Frames - !!!"
zeroReg    = "\t; Save zero to reg"
endText    = "\t; End with XXX bytes"

usedRegisters = []

for line in lines:
    line = line[12:20]
    hex1 = line[0:2]
    hex2 = line[3:5]
    hex3 = line[6:8]

    if hex1 == "5A":
#       register = int("0x" + hex2, 16).to_bytes(1, "little")
#       data     = int("0x" + hex3, 16).to_bytes(1, "little")


       register = "$"+hex2
       data     = "$"+hex3

       usedRegisters.append(register)

       byteData.append(register + firstByte)
       byteData.append(data + secondByte)
       byteData.append("|")

    elif hex1 in ["61", "62", "63"]:
       register = int(0).to_bytes(1, "little")
       if hex2   == "62":
          waits = 735
       elif hex2 == "63":
          waits = 882

       else:
          waits = int("0x" + hex3 + hex2, 16)

       waits = (waits * oneSample) / oneNTSCFrame

       integer  = round(waits+decimals)
       decimals = (waits+decimals) - integer

       if integer > 0:
           # print(integer)
           if integer < 256:
              byteData.append(waitOp + waitCode)
              xxx = hex(integer).replace("0x", "")
              if len(xxx) == 1:
                 xxx = "0" + xxx
              xxx = "$" + xxx

              byteData.append(xxx + waitNum)
              byteData.append("|")

           else:
             while integer > 255:
                 byteData.append(waitOp + waitCode)
                 byteData.append("$FF" + waitNum)
                 integer-=256
                 byteData.append("|")

             if integer > 0:
                byteData.append(waitOp + waitCode)
                xxx = hex(integer).replace("0x", "")
                if len(xxx) == 1:
                    xxx = "0" + xxx
                xxx = "$" + xxx

                byteData.append(xxx + waitNum)
                byteData.append("|")

all8bits = []
for number in range(0, 256):
    number = hex(number).replace("0x", "")
    if len(number) == 1:
       number = "0" + number

    all8bits.append("$" + number.upper())

possibleKeys = []

usedRegisters.append("$00")

for byte in all8bits:
    if byte.startswith("$1"): continue
    if byte.startswith("$D"): continue

    if byte.upper() not in usedRegisters:
       possibleKeys.append(byte.upper())

byteConstantText = "\tBYTE\t"

endByte = possibleKeys[0]
endConstant = "#NAME#_VGM_EndByte = " + endByte + "\n"

backByte = possibleKeys[1]
backConstant = "#NAME#_VGM_BackByte = " + backByte + "\n"

jumpByte = possibleKeys[2]
jumpConstant = "#NAME#_VGM_JumpByte = " + jumpByte + "\n"

allTheData = []
segment    = ""
segments   = {}

for byte in byteData:
    if byte != "|":
       segment += byteConstantText + "#" + byte + "\n"
    else:
       allTheData.append(segment)
       segment = ""

dataText = "".join(allTheData)
segments = {}
for length in range(2, 32):
    for indexStart in range(0, len(allTheData)-length + 1):
        s = "".join(allTheData[indexStart:indexStart + length])

        if s not in segments.keys():
           segments[s] = 0

        occurs   = dataText.count(s)
        takesNow  = occurs * s.count("BYTE")
        wouldTake = occurs * 2 + s.count("BYTE") + 1

        if occurs > 1:
           segments[s] += takesNow - wouldTake

segmentList = []

for key in segments.keys():
    segmentList.append([segments[key], key])

segmentList.sort(reverse=True)

maxNum   = 0
bestOne  = 0
saveData = []
lastNum  = possibleKeys[3]

for theMax in range(3, 128):
    titleText = "#NAME#_VGM_Segment_BankX_"
#    jumpTable = "\n\t_align\tXXX\n"
    jumpTable = "\n"
    allSegments = ""

    for num in range(0, theMax):
        if num   >= len(segmentList)\
        or num+3 >= len(possibleKeys):
            break

        title = titleText + possibleKeys[num + 3]
        if num == 0:
           jumpTable += "\n#NAME#_VGM_JumpTable_BankX" + "\n"
           for filler in range(0, int(possibleKeys[3].replace("$", "0x"), 16) * 2):
               jumpTable += byteConstantText + "#0\n"

        difference = int(possibleKeys[num + 3].replace("$", "0x"), 16) - int(lastNum.replace("$", "0x"),16)
        for filler in range(0, (difference-1) *2):
           jumpTable += byteConstantText + "#0\n"

        jumpTable += byteConstantText + "#<" + title + "\n" + byteConstantText + "#>" + title + "\n"
#        allSegments += "\n\t_align\tXXX\n" +\
        allSegments += "\n" + \
                       title + "\n" + segmentList[num][1] + "\n" + byteConstantText + "#" + backByte + "\n###\n"

        replacer = byteConstantText + "#" + jumpByte + "\t; Jump to" + "\n" + byteConstantText + "#" + possibleKeys[num + 3] + "\t; somewhere! - !!!\n"

        dataText = dataText.replace(segmentList[num][1], replacer)
        lastNum  = possibleKeys[num + 3]

    jumpTable = jumpTable.replace("XXX", str(jumpTable.count("BYTE")))
    fullText = dataText + jumpTable + allSegments
    sumOfTakenBytes = fullText.count("BYTE")

    limitByBanks    = 4096 - (jumpTable.count("BYTE") + allSegments.count("BYTE") + 512)
    if limitByBanks < 1024: continue

    per = dataText.count("BYTE") / limitByBanks

    if bestOne == 0 or per < bestOne:
       maxNum   = theMax
       bestOne  = per
       saveData = [dataText, jumpTable, allSegments]

for dataNum in range(0, len(saveData)):
    text = saveData[dataNum]
    lines = text.split("\n")
    newLines = []
    for lineNum in range(0, len(lines), 2):
       default = True
       line = lines[lineNum]
       if firstByte in line:
          if   "$A" in line:
              newLines.append(line.replace("$A", "$1").replace(firstByte, zeroReg))
              default = False
          elif "$B" in line:
              newLines.append(line.replace("$B", "$D").replace(firstByte, zeroReg))
              default = False

       if default == True:
          newLines.append(lines[lineNum])
          try:
            newLines.append(lines[lineNum+1])
          except:
            pass

    saveData[dataNum] = "\n".join(newLines)

jumpTable   = saveData[1]
allSegments = saveData[2]
dataText    = saveData[0]
limitByBanks = 4096 - (jumpTable.count("BYTE") + allSegments.count("BYTE") + 640)
per = dataText.count("BYTE") / limitByBanks

# titleText = "\talign\t256\n#NAME#_VGM_Segment_BankX"
titleText = "\n#NAME#_VGM_Segment_BankX"

lines = dataText.split("\n")
newText = ""
first = True
byteCalc   = 0

bankNum = 0
for lineNum in range(0, len(lines)):
    line = lines[lineNum]

    shouldDoIt = False
    if byteCalc >= limitByBanks and "!!!" not in lines[lineNum]:
       shouldDoIt = True

    if "BYTE" in line:
       if first or shouldDoIt:
          if first == False: newText += byteConstantText + "#" + endByte + endText.replace("XXX", str(byteCalc)) + "\n&&&\n"
          if lineNum != len(lines) - 1:
             newText += titleText.replace("BankX", "Bank" + str(bankNum)) + "\n"
             bankNum +=1
          byteCalc = 0
          first = False

       newText  += lines[lineNum] + "\n"
       byteCalc += 1

newText += byteConstantText + "#" + endByte + endText.replace("XXX", str(byteCalc)) + "\n"
saveData[0] = newText

segments = saveData[2].split("###\n")
segments.pop(-1)

for segmentNum in range(0, len(segments)):
    segments[segmentNum] = segments[segmentNum].replace("XXX", str(segments[segmentNum].count("BYTE")))

saveData[2] = "".join(segments)

bankMainData = saveData[0].split("&&&")

for bankNum in range(0, len(bankMainData)):
    if bankNum == 0:
       constants =  endConstant + jumpConstant + backConstant
    else:
       constants = ""

    toSave = constants + bankMainData[bankNum] + saveData[1] + saveData[2]
    toSave = toSave.replace("BankX", "Bank"+str(bankNum)).replace("- !!!", "")

    f = open("saved"+str(bankNum)+".txt", "w")
    f.write(toSave)
    f.close()