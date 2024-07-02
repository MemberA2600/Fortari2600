import os
from PIL import Image, ImageTk
import shutil
import re

class IO:

    def __init__(self, config, dict, loader):
        self.__config = config
        self.__dicts = dict
        self.__loader = loader

    def getImg(self, name, size):

        if (size == None):
            return(ImageTk.PhotoImage(Image.open("others/img/"+name+".png")
                                      .resize((self.__loader.mainWindow.getConstant(),
                                               self.__loader.mainWindow.getConstant()), Image.ANTIALIAS)))
        elif type(size) == tuple:
            return(ImageTk.PhotoImage(Image.open("others/img/"+name+".png")
                                      .resize(size), Image.ANTIALIAS))

        else:
            return(ImageTk.PhotoImage(Image.open("others/img/"+name+".png")
                                      .resize((size, size)), Image.ANTIALIAS))


    def checkIfValidFileName(self, name):
        from pathvalidate import ValidationError, validate_filename
        try:
            validate_filename(name)
            return(True)
        except ValidationError as e:
            return(False)

    def copyDirWithFiles(self, sourcedir, destdir):
        shutil.copytree(sourcedir, destdir)


    def removeDirWithFiles(self, dir):
        shutil.rmtree(dir)

    def loadWholeText(self, path):
        try:
            file = open(path, "r", encoding="latin-1")
            text = file.read()
            file.close()

        except:
            file = open(path, "rb")
            text = file.read().encode("latin-1")
            file.close()
        return(text)

    def getFileNamesInDir(self, dir):
        names = []

        for root, dirs, files in os.walk(dir):
            for file in files:
                names.append(".".join(file.split(".")[:-1]))

        return(names)

    def loadSyntax(self):
        from Command import Command

        skipFirst = True
        for item in self.loadWholeText("config"+os.sep+"syntax.csv").split("\n"):
            if item == "": continue
            if skipFirst == True:
               skipFirst = False
            else:
               item = item.replace("\r", "").split(";")
               if ",".join(item[1:]) == "": return
               self.__loader.syntaxList[item[0]] = Command(self.__loader, item[0], ",".join(item[1:]))

        stringConstants = self.__loader.stringConstants

        for item in self.loadWholeText("config"+os.sep+"strings.txt").split("\n"):
            name = item.split("=")[0]
            stringConstants[name] = {}

            secondPart = item.split("=")[1].split(",")
            stringConstants[name]["alias"] = secondPart[0][1:-1].split(" ")
            stringConstants[name]["value"] = int(secondPart[1])

        self.collectColorsConstants()
        #for c in stringConstants:
        #    print(c, stringConstants[c]["alias"])

    def collectColorsConstants(self):
        import webcolors

        allColors = {}

        for dictionary in [webcolors.HTML4_NAMES_TO_HEX,
                           webcolors.CSS2_NAMES_TO_HEX ,
                           webcolors.CSS21_NAMES_TO_HEX,
                           webcolors.CSS3_NAMES_TO_HEX  ]:
            for const in dictionary:
                if const not in allColors.keys():
                   allColors[const] = dictionary[const]

        for color in allColors:
            name = '"' + color + '"'
            integerColor = webcolors.hex_to_rgb(dictionary[color])

            self.__loader.stringConstants[name] = {"alias": [name.upper(), name[:2].upper() + name[2:].lower()],
                                                   "value": self.__loader.colorDict.getClosestTIAColor(integerColor.red, integerColor.green, integerColor.blue).upper()}

        for name in self.__loader.stringConstants:
            if name in ("True", "False"): continue
            secondAlias = self.__loader.stringConstants[name]["alias"][1]
            for compareName in self.__loader.stringConstants:
                if compareName in ("True", "False"): continue
                if name[1:-1] in compareName[1:-1]:
                   new = self.__loader.stringConstants[compareName]['alias'][1].replace(name[1:-1], secondAlias[1:-1])
                   if new not in self.__loader.stringConstants[compareName]['alias']: \
                                 self.__loader.stringConstants[compareName]['alias'].append(new)


    def loadRegOpCodes(self):
        return self.loadRegisters(), self.loadOpCodes()

    def loadRegisters(self):
        temp = {}
        file = open("templates/6507Registers.a26", "r")
        for line in file.readlines():
            line = line.split("=", 1)
            if (line[0].startswith("$") == False):
                line[0] = "$"+line[0]

            temp[line[0]] = line[1].replace("\r","").replace("\n","").replace(" ", "")

        file.close()
        return(temp)


    def loadOpCodes(self):
        temp = {}
        file = open("templates/opcodes.a26", "r")
        for line in file.readlines():
            line = line.split("=", 1)
            if (line[0].startswith("$") == False):
                line[0] = "$"+line[0]

            temp[line[0]] = {}
            sub = line[1].replace("\r","").replace("\n","")

            while(sub.endswith(" ")):
                sub = sub[:-1]

            sub = sub.split(" ")
            temp[line[0]]["opcode"] = sub[0]
            if len(sub) == 1:
                temp[line[0]]["format"] = None
                temp[line[0]]["bytes"] = 1
            else:
                temp[line[0]]["format"] = sub[1]
                temp[line[0]]["bytes"] = int(sub[1].count("a")/2)+1

        file.close()
        return(temp)

    def loadSubModule(self, name):
        return(open("templates/skeletons/"+name+".asm", "r").read())

    def loadKernelElement(self, name, element):
        txt = open("templates/skeletons/"+name+"_"+element+".asm", "r").read()

        if self.__loader.virtualMemory.includeKernelData:
           txt = txt.replace("!!!MAINVARS!!!", open("templates/skeletons/"+name+"_"+element+"_sysVars.asm", "r").read())
           startAddress = 0xd1
        else:
           remove1 = re.findall(r'###Start-Main-Kernel.+###End-Main-Kernel'        , txt, re.DOTALL)[0]
           remove2 = re.findall(r'###Start-Main-Kernel-Sub.+###End-Main-Kernel-Sub', txt, re.DOTALL)[0]

           txt = txt.replace(remove1, "").replace(remove2, "")
           startAddress = 0x96

        if self.__loader.virtualMemory.includeJukeBox:
           txt = txt.replace("!!!MUSICVARS!!!", open("templates/skeletons/"+name+"_"+element+"_musicVars.asm", "r").read())

        if self.__loader.virtualMemory.includeCollisions:
           txt = txt.replace("!!!COLLISIONVARS!!!", open("templates/skeletons/"+name+"_"+element+"_collVars.asm", "r").read())

        return txt

    def loadTestElement(self, mode, name, element):
        return(open("templates/testCodes/"+mode+"_"+name+"_"+element+".asm", "r").read())

    def loadTestElementPlain(self, element):
        return(open("templates/testCodes/"+element+".asm", "r").read())

    def loadAnimationFrames(self, folder, maxNum, dataHolder, format, s):
        from PIL import Image as IMAGE

        for num in range(1, maxNum):
            num = str(num)
            if len(num) == 1:
                num = "0" + num
            dataHolder.append(
                self.returnResized(IMAGE.open(str("others/img/"+folder+"/" + num + "."+format)), s[0], s[1], s[2]))

    def loadCommandASM(self, name):
        return self.loadWholeText("templates"+os.sep+"commandASM"+os.sep+name+".asm")

    def returnResized(self, source, w, h, part):
        from PIL import Image as IMAGE

        return ImageTk.PhotoImage(source.resize((round(w*part), round(h))), IMAGE.ANTIALIAS)