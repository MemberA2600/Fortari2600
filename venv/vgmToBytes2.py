f = open("loadThis.txt", "r")
lines = f.read().replace("\r", "").split("\n")
f.close()

byteData = []
oneSample = 1487.0 / 65535.0
oneCycle  = 0.56
decimals  = 0
waitOp    = "$00"

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
       byteData.append(data)

    elif hex1 in ["61", "62", "63"]:
       register = int(0).to_bytes(1, "little")
       if hex2   == "62":
          waits = 735
       elif hex2 == "63":
          waits = 882

       else:
          waits = int("0x" + hex3 + hex2, 16)

       waits = (waits * oneSample) / oneCycle

       integer  = round(waits+decimals)
       decimals = (waits+decimals) - integer

       if integer > 0:
          if integer < 256:
              byteData.append(waitOp)
              xxx = hex(integer).replace("0x", "")
              if len(xxx) == 1:
                 xxx = "0" + xxx
              xxx = "$" + xxx

              byteData.append(xxx)

          else:
             while integer > 255:
                 byteData.append(waitOp)
                 byteData.append("$FF")
                 integer-=256

             if integer > 0:
                byteData.append(waitOp)
                xxx = hex(integer).replace("0x", "")
                if len(xxx) == 1:
                    xxx = "0" + xxx
                xxx = "$" + xxx

                byteData.append(xxx)

    byteData.append("|")

keys = []

"""
for num in range(0, 256):
    if len(keys) > 127: break
    xxx = hex(num).replace("0x", "")
    if len(xxx) == 1:
        xxx = "0" + xxx
    xxx = "$" + xxx

    key = xxx
    if key not in byteData:
        keys.append(key)
"""

keyMask   = "keyMask = "
otherMask = []

for num in range(0, 16):
    num = "$" + hex(num).replace("0x", "")
    num = num.upper()

    isItThere = False
    for item in byteData:
        if item.startswith(num):
           isItThere = True
           break

    if isItThere == False:
       if keyMask == "keyMask = ":
           keyMask += num + "0" + "\n"
           for num2 in range(0, 16):
               num2 = num + hex(num2).replace("0x", "")
               keys.append(num2.upper())
       else:
           for num2 in range(0, 16):
               num2 = num + hex(num2).replace("0x", "")
               otherMask.append(num2.upper())

byteText = "\tBYTE\t"
text     = ""

dataAll     = []
dataCounted = {}

for b in byteData:
    if b != "|":
       text += byteText + "#" + b + "\n"
    else:
       dataAll.append(text)
       if text not in dataCounted.keys():
          dataCounted[text] = 0

       dataCounted[text] += text.count("BYTE")
       text = ""

if "" in dataCounted.keys():
   del dataCounted[""]
   dataAll.pop(-1)

again = []

for key in dataCounted.keys():
    again.append([dataCounted[key], key])

again.sort(reverse=True)

if len(keys)  > 129: keys = keys[:129]
if len(again) > len(keys) - 1: again = again[:len(keys)]

replaceList = {}
returnByte = otherMask[0]
endByte    = otherMask[1]

# listIndexTable    = "\n\t_align\t"+ str(len(keys))     + "\nNAME_BankX_IndexTable\n"
listPointerTable  = "\n\t_align\t"+ str(len(keys) * 2) + "\nNAME_BankX_PointerTable\n"
listTheActualData = ""
fullText1 = "\n\talign\t256\nNAME_VGM_Full_Bank0\n"
fullText2 = "\n\talign\t256\nNAME_VGM_Full_Bank1\n"

for num in range(0, len(again)):
    key  = keys[num]
    data = again[num][1]
    title = "NAME_BankX_VGM_Data_"+ key + "\n"

    replaceList[data] = byteText + "#"  + key + "\n"
    # listIndexTable   += byteText + "#"  + key + "\n"
    listPointerTable += byteText + "#<" + title + byteText + "#>" + title

    listTheActualData += "\n\t_align\t" + str(data.count("BYTE")) + "\n" + title + data + byteText + "#" + returnByte +"\n"

byteLimit = 3600
closeFirst = False

for dataNum in range(0, len(dataAll)):
    if dataAll[dataNum] in replaceList.keys():
       dataAll[dataNum] = replaceList[dataAll[dataNum]]

    if fullText1.count("BYTE") + dataAll[dataNum].count("BYTE") > byteLimit\
       and closeFirst == False:
        closeFirst = True
        fullText1 += byteText + "#" + endByte + "\n"

    if closeFirst == False:
       fullText1 += dataAll[dataNum]
    else:
       fullText2 += dataAll[dataNum]

if closeFirst == False:
   fullText1 += byteText + "#" + endByte + "\n"
else:
   fullText2 += byteText + "#" + endByte + "\n"

fullText1 += "* Number of bytes: " + str(fullText1.count("BYTE")) + "\n"

if fullText2.count("BYTE") == 0:
    fullText2 = ""
else:
    fullText2 += "* Number of bytes: " + str(fullText2.count("BYTE")) + "\n"

constant1 = "NAME_VGM_endbyte = " + endByte + " \n"
constant2 = "NAME_VGM_returnbyte = " + returnByte + " \n"

lastText = keyMask + constant1 + constant2 + fullText1 + fullText2 + listPointerTable + listTheActualData

f = open("saved.txt", "w")
f.write(lastText)
f.close()
