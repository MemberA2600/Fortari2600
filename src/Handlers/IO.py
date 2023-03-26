import os
from PIL import Image, ImageTk

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
        from shutil import copytree
        copytree(sourcedir, destdir)


    def removeDirWithFiles(self, dir):
        import shutil
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

        for item in self.loadWholeText("config"+os.sep+"syntax.txt").split("\n"):
            if item.startswith("*") or item.startswith("#"): continue
            self.__loader.syntaxList[item.split("=")[0]] = Command(self.__loader, item.split("=")[0], "=".join(item.split("=")[1:]).replace("\n","").replace("\r",""))

        stringConstants = self.__loader.stringConstants

        for item in self.loadWholeText("config"+os.sep+"strings.txt").split("\n"):
            name = item.split("=")[0]
            stringConstants[name] = {}

            secondPart = item.split("=")[1].split(",")
            stringConstants[name]["alias"] = secondPart[0][1:-1].split(" ")
            stringConstants[name]["value"] = int(secondPart[1])


        #print(stringConstants)

    def loadSubModule(self, name):
        return(open("templates/skeletons/"+name+".asm", "r").read())

    def loadKernelElement(self, name, element):
        return(open("templates/skeletons/"+name+"_"+element+".asm", "r").read())

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