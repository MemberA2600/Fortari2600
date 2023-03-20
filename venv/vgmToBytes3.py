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
secondByte = "\t; SecondByte"

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

       byteData.append(register)
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
          if integer < 256:
              byteData.append(waitOp)
              xxx = hex(integer).replace("0x", "")
              if len(xxx) == 1:
                 xxx = "0" + xxx
              xxx = "$" + xxx

              byteData.append(xxx +secondByte)
              byteData.append("|")


          else:
             while integer > 255:
                 byteData.append(waitOp)
                 byteData.append("$FF" + secondByte)
                 integer-=256
                 byteData.append("|")

             if integer > 0:
                byteData.append(waitOp)
                xxx = hex(integer).replace("0x", "")
                if len(xxx) == 1:
                    xxx = "0" + xxx
                xxx = "$" + xxx

                byteData.append(xxx + secondByte)
                byteData.append("|")

#numbers = []
#for byte in byteData:
#    if byte != "|":
#       byte = int.to_bytes(int(byte.replace("$", "0x").split("\t")[0], 16), 1, "big")
#       numbers.append(byte)

#f = open("fuck.bin", "wb")
#for byte in numbers:
#    f.write(byte)
#f.close()

all8bits = []
for number in range(0, 256):
    number = hex(number).replace("0x", "")
    if len(number) == 1:
       number = "0" + number

    all8bits.append("$" + number.upper())

possibleKeys = []

for byte in all8bits:
    if byte.upper() not in byteData:
       possibleKeys.append(byte.upper())

byteConstantText = "\tBYTE\t"

endByte = possibleKeys[0]
endConstant = "\nNAME_VGM_EndByte = " + endByte + "\n"

backByte = possibleKeys[1]
backConstant = "\nNAME_VGM_BackByte = " + endByte + "\n"

jumpByte = possibleKeys[1]
backConstant = "\nNAME_VGM_JumpByte = " + endByte + "\n"

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

for theMax in range(3, 128):
    titleText = "NAME_VGM_Segment_"
    jumpTable = "\n\t_align\tXXX\n"
    allSegments = ""

    for num in range(0, theMax):
        if num >= len(segmentList):
            break
        title = titleText + all8bits[num]
        if num in [0, 128]:
           jumpTable += "\nNAME_VGM_JumpTable_" + str(num) + "\n"

        jumpTable += byteConstantText + "#<" + title + "\n" + byteConstantText + "#>" + title + "\n"
        allSegments += "\n\t_align\t" + str(segmentList[num][1].count("BYTE") + 1) + "\n" +\
                         title + "\n" + segmentList[num][1] + "\n" + byteConstantText + "#" + backByte + "\n"

        replacer = byteConstantText + "#" + jumpByte + "\n" + byteConstantText + "#" + all8bits[num] + "\t; Jumping!\n"

        dataText = dataText.replace(segmentList[num][1], replacer)

    jumpTable = jumpTable.replace("XXX", str(jumpTable.count("BYTE")))
    fullText = dataText + jumpTable + allSegments
    sumOfTakenBytes = fullText.count("BYTE")

    limitByBanks    = 4096 - (jumpTable.count("BYTE") + allSegments.count("BYTE") + 512)
    if limitByBanks < 1024: continue

    per = dataText.count("BYTE") / limitByBanks

    #print(theMax, limitByBanks, dataText.count("BYTE"), per)

    if bestOne == 0 or per < bestOne:
       maxNum   = theMax
       bestOne  = per
       saveData = [dataText, jumpTable, allSegments]

print("".join(saveData))
