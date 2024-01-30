from shutil import copy2
from os import walk
from os.path import exists

batchTxt = []
itemCounter = 0
lastLetter = ""
gotos      = {}

for root, dirs, files in walk("E:\VGMs"):
    for file in files:
        if (".vmg" in file.lower()) or (".vgz" in file.lower()):
            path = root + "\\" + file
            newName = root.split("\\")[-1][0:4]+"_" + "".join(".".join(file.split(".")[:-1]).split(" ")[0:])[0:3]
            newPath = "E:\VGMs\\" + newName

            if exists(newPath) == False and root != "E:\VGMs":
               copy2(path, newPath)
            if root != "E:\VGMs":
               batchTxt.append(":item_"+str(itemCounter)+"\n")
               gotos[str(itemCounter)] = batchTxt[-1]
               if newName[0] != lastLetter:
                  batchTxt.append(":letter_"+newName[0].lower()+"\n")
                  gotos[newName[0].lower()] = batchTxt[-1]

               batchTxt.append("SBVGM.exe -a " + newName + "\n")
               itemCounter += 1
               lastLetter  = newName[0]

f = open("E:\VGMs\play.bat", "w")
for item in gotos:
    f.write("IF %1=="+item+ " GOTO " + gotos[item])

f.write("".join(batchTxt))
f.close()

