from PIL import Image as IMG, ImageTk
from copy import deepcopy
from tkinter import *
from SubMenu import SubMenu

class PictureToCode:

    def __init__(self, loader, kernel, mode, w, changed):
        if mode == "playfield":
            self.__w = 40

            if kernel=="common":
                self.__mirroring = [0,1,1]
                self.__h = 42
        elif mode == "64pxPicture":
            self.__w = 64

        self.__mode = mode

        self.__loader = loader
        self.__mainWindow = self.__loader.mainWindow
        self.dead = False
        self.doThings = False

        self.__loader.stopThreads.append(self)

        self.__config = self.__loader.config
        self.__dictionaries = self.__loader.dictionaries
        self.__screenSize = self.__loader.screenSize
        self.__soundPlayer = self.__loader.soundPlayer
        self.__fileDialogs = self.__loader.fileDialogs
        self.__fontManager = self.__loader.fontManager
        self.__fontSize = int(self.__screenSize[0] / 1300 * self.__screenSize[1] / 1050 * 14)
        self.__colors = self.__loader.colorPalettes
        self.__colorDict = self.__loader.colorDict

        self.__screenSize = self.__loader.screenSize

        formats = [
            "bmp", "dds", "eps", "gif", "dib", "ico", "jpg", "jpeg", "pcx", "png", "tga", "tiff", "pdf"
        ]

        self.answer = self.__fileDialogs.askForFileName("loadPicture",
                                                   False, [formats, "*"], self.__mainWindow.projectPath)
        if self.answer !="":
            image = IMG.open(self.answer, "r")
            if image.mode != "RGB":
                image = image.convert("RGB")

            self.__image = image

            self.__func = None
            self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
            self.__smallFont = self.__fontManager.getFont(int(self.__fontSize * 0.80), False, False, False)
            self.__smallFont2 = self.__fontManager.getFont(int(self.__fontSize * 0.65), False, False, False)


            self.__window = SubMenu(self.__loader, "loadPicture", self.__screenSize[0] / 1.5,
                                    self.__screenSize[1] / 4 - 45, None, self.__addElements, 2)

            self.dead = True

            # Window is dead.
            if self.doThings == True:
                self.generateImage(mode, image, None)

    def generateImage(self, mode, image, testing):
        width, height = image.size
        multi = self.__w / width
        h = round(image.height * multi)

        self.Y = h
        self.__multiH = 1
        if self.Y > 255:
            self.Y = 255
        elif self.__mode == "playfield":
            if self.Y < self.__h:
                self.__multiH = round(self.__h / h)

        w = self.__w
        imageSized = image.resize((w, h), IMG.ANTIALIAS)
        imgColorData = imageSized.load()

        imageClone = deepcopy(imageSized)

        from PIL import ImageOps

        if self.__mode == "playfield":
            if self.__invert.get():
                imageClone = ImageOps.invert(imageClone)

            if self.__right.get():
                imageClone = ImageOps.mirror(imageClone)

        if mode == "playfield":
            fn = lambda x: 255 if x > int(self.__tres.get()) else 0
            altImage = deepcopy(imageClone).convert('L').point(fn, mode='1')
        elif self.__mode == "64pxPicture":
            fn1 = lambda x: 255 if x > int(self.__tres.get()) else 0
            fn2 = lambda x: 255 if x > int(self.__tres.get()) + 128 else 0
            altImage1 = deepcopy(imageClone).convert('L').point(fn1, mode='1')
            altImage2 = deepcopy(imageClone).convert('L').point(fn2, mode='1')

            pixels1 = altImage1.load()
            pixels2 = altImage2.load()

            W, H = altImage1.size

            pixels = []

            for Y in range(0, H):
                for X in range(0, W):
                    value = (pixels1[X, Y] + pixels2[X, Y]) // 2
                    # pixels.append((value, value, value))
                    # data+=chr(value) + chr(value) + chr(value)
                    pixels.append(value)
                    pixels.append(value)
                    pixels.append(value)

            altImage = IMG.frombytes("RGB", (w, h), bytes(pixels))

        # GetColors
        imgPixelData = altImage.load()

        if mode == "playfield":
            self.pixels = []
            self.pfColors = []
            self.bgColors = []

            self.getColorData(w, h, imgColorData, imgPixelData)
            self.getPFData(w, h, imgPixelData)

        elif mode == "64pxPicture":
            self.generateASM(w, h, imgColorData, imgPixelData, testing)


    def generateASM(self, w, h, imgColorData, imgPixelData, testing):
        #mergedImageData = {}
        mergedByLines = []

        for Y in range(0, h):
            tempLine = []
            """
            lineValues = {
                0: [], 127: [], 255: []
            }
            """
            for X in range(0, w):
                lineDict = {}
                lineDict["pixel"] = imgPixelData[X,Y]
                lineDict["color"] = imgColorData[X,Y]
                #mergedImageData[str(X)+","+str(Y)] = lineDict
                tempLine.append(lineDict)
                #lineValues[lineDict["pixel"][0]].append(lineDict["color"])

            lineStruct = self.decideLineColors(tempLine)
            mergedByLines.append(lineStruct)

        asm = self.getASM(mergedByLines, h)
        if testing == True:
            from threading import Thread
            t = Thread(target=self.compileThread, args=[asm, h])
            t.daemon=True
            t.start()
        else:
            file = open(self.__loader.mainWindow.projectPath+"/64px/"+self.__name+".asm", "w")
            file.write(asm)
            file.close()
            self.__loader.soundPlayer.playSound("Success")

    def compileThread(self, asm, h):
        from Compiler import Compiler
        C = Compiler(self.__loader, "common", "test64px", [asm, h])

    def getASM(self, data, h):
        pic64px_Sprite = [
            "pic64px_00\n",
            "pic64px_01\n",
            "pic64px_02\n",
            "pic64px_03\n",
            "pic64px_04\n",
            "pic64px_05\n",
            "pic64px_06\n",
            "pic64px_07\n"
        ]
        pic64px_Color = "pic64px_Color\n"
        pic64px_PF = "pic64px_PF\n"
        pic64px_PFColor = "pic64px_PFColor\n"
        pic64px_BGColor = "pic64px_BGColor\n"

        for Y in range(0, h):
            Y = h-1-Y
            #print(data[Y])
            spriteData = data[Y]["sprites"]["pixels"]
            spriteColor = data[Y]["sprites"]["color"]
            pfData = data[Y]["playfield"]["pixels"]
            pfColors = data[Y]["playfield"]["color"]
            bg = data[Y]["background"]

            for pixelNum in range(0,64,8):
                pic64px_Sprite[pixelNum//8] += ("\tBYTE\t#%"+
                                                spriteData[pixelNum:(pixelNum+8)]
                                                +"\n"
                                                )
            pic64px_Color += ("\tBYTE\t#"+ spriteColor+"\n")
            pic64px_PF += ("\tBYTE\t#%"+ pfData+"\n")
            pic64px_PFColor += ("\tBYTE\t#" + pfColors + "\n")
            pic64px_BGColor += ("\tBYTE\t#" + bg + "\n")


        allData = [
            pic64px_Sprite[0], pic64px_Sprite[1], pic64px_Sprite[2], pic64px_Sprite[3], pic64px_Sprite[4],
            pic64px_Sprite[5], pic64px_Sprite[6], pic64px_Sprite[7], pic64px_Color, pic64px_PF,
            pic64px_PFColor, pic64px_BGColor
        ]


        final = "\npic64px_data\n\talign\t256\n"
        bytes = 0
        for data in allData:
            numOfBytes = data.count("BYTE")
            if (bytes+numOfBytes) > 255:
                final+="\n\talign\t256\n" + data[:-1]
                bytes = 0
            else:
                final+=data[:-1]

            bytes+=numOfBytes
            bytes%=256

            final+="\t; "+str(bytes)+"\n\n"

        #print(final)
        return(final)


    def decideLineColors(self, lineValues):
        sums = {
            0: { "colors": [], "pixels": "", "dominantColor": None, "domiTIA": None, "pfError": 0, "allSet": 0},
            127: { "colors": [], "pixels": "", "dominantColor": None, "domiTIA": None, "pfError": 0, "allSet": 0},
            255: {"colors": [], "pixels": "", "dominantColor": None, "domiTIA": None, "pfError": 0, "allSet": 0}
        }

        lineStructure = {
            "background": "",
            "playfield": {"pixels1": "", "color": "", "pixels2": "", "pixels": ""},
            "sprites": {"pixels": "", "color": ""}
        }

        assign = {
            "background": 0,
            "playfield": 0,
            "sprites": 0
        }

        for pixelData in lineValues:
            if pixelData["pixel"][0] == 0:
                sums[0]["pixels"] += "1"
                sums[127]["pixels"] += "0"
                sums[255]["pixels"] += "0"
                sums[0]["colors"].append(pixelData["color"])

            elif pixelData["pixel"][0] == 127:
                sums[0]["pixels"] += "0"
                sums[127]["pixels"] += "1"
                sums[255]["pixels"] += "0"
                sums[127]["colors"].append(pixelData["color"])

            else:
                sums[0]["pixels"] += "0"
                sums[127]["pixels"] += "0"
                sums[255]["pixels"] += "1"
                sums[255]["colors"].append(pixelData["color"])

        for item in [0, 127, 255]:
            sums[item]["dominantColor"] = self.__colorDict.getDominantColor(sums[item]["colors"])
            if sums[item]["dominantColor"] != None:
                try:
                    sums[item]["domiTIA"] = self.__colorDict.getClosestTIAColor(sums[item]["dominantColor"][0],
                                                                             sums[item]["dominantColor"][2],
                                                                             sums[item]["dominantColor"][1])
                except:
                    print(sums[item]["dominantColor"])


            if (sums[item]["domiTIA"]) == None:
                (sums[item]["domiTIA"]) = "$00"

            pfError = 0
            for X in range(0,64,4):
                D = sums[item]["pixels"]
                p1 = int(D[0])
                p2 = int(D[1])
                p3 = int(D[2])
                p4 = int(D[3])

                if (p1+p2+p3+p4 == 4) or (p1+p2+p3+p4 == 0):
                    continue
                elif (p1+p2+p3+p4 == 2):
                    pfError+=2
                else:
                    pfError+=1

                string1 = sums[item]["pixels"][:32]
                string2 = sums[item]["pixels"][32:][::-1]

                for charNum in range(0,32):
                    if string1[charNum] != string2[charNum]:
                        pfError+=1
                sums[item]["allSet"] += (p1+p2+p3+p4)

            sums[item]["pfError"] = pfError

        notUsed = [0, 127, 255]

        #playfield
        temp={}
        for item in notUsed:
            temp[item] = sums[item]["pfError"]
        sorted(temp, key=temp.get)
        if sums[notUsed[0]]["pfError"] == sums[notUsed[1]]["pfError"] and sums[notUsed[1]]["pfError"] == sums[notUsed[2]]["pfError"]:
            grrr = {}
            for item in notUsed:
                grrr[item] = sums[item]["allSet"]
                sorted(grrr, key=grrr.get, reverse=True)
            key = list(grrr.keys())[0]
        else:
            if sums[list(temp.keys())[0]]["pfError"] == sums[list(temp.keys())[1]]["pfError"]:
                grrr = {}
                grrr[list(temp.keys())[0]] = sums[list(temp.keys())[0]]["allSet"]
                grrr[list(temp.keys())[1]] = sums[list(temp.keys())[1]]["allSet"]
                sorted(grrr, key=grrr.get, reverse=True)
                key = list(grrr.keys())[0]
            else:
                key = list(temp.keys())[0]

        notUsed.remove(key)

        lineStructure["playfield"]["color"] = sums[key]["domiTIA"]
        lineStructure["playfield"]["pixels1"] = sums[key]["pixels"][:32]+sums[key]["pixels"][:32][::-1]
        lineStructure["playfield"]["pixels2"] = sums[key]["pixels"][32:][::-1]+sums[key]["pixels"][32:]
        assign["playfield"] = key

        #background
        temp={}
        for item in notUsed:
            temp[item] = sums[item]["allSet"]
        sorted(temp, key=temp.get)
        notUsed.remove(list(temp.keys())[0])

        lineStructure["background"] = sums[list(temp.keys())[0]]["domiTIA"]
        assign["background"] = list(temp.keys())[0]

        #spite
        lineStructure["sprites"]["color"] = sums[notUsed[0]]["domiTIA"]
        lineStructure["sprites"]["pixels"] = sums[notUsed[0]]["pixels"]
        assign["sprites"] = notUsed[0]

        OK = [0,0]
        for pixelNum in range(0,64):
            if (sums[assign["background"]]["pixels"][pixelNum] == "1"
                    and lineStructure["playfield"]["pixels1"] == "0"
                    and lineStructure["sprites"]["pixels"] == "0"):
                OK[0]+=1
            elif (sums[assign["playfield"]]["pixels"][pixelNum] == "1"
                and lineStructure["playfield"]["pixels1"] == "1"
                  and lineStructure["sprites"]["pixels"] == "0"):
                OK[0]+=1
            elif (sums[assign["sprites"]]["pixels"][pixelNum] == "1"
                and lineStructure["sprites"]["pixels"] == "1"):
                OK[0] += 1

        for pixelNum in range(0,64):
            if (sums[assign["background"]]["pixels"][pixelNum] == "1"
                    and lineStructure["playfield"]["pixels2"] == "0"
                    and lineStructure["sprites"]["pixels"] == "0"):
                OK[1]+=1
            elif (sums[assign["playfield"]]["pixels"][pixelNum] == "1"
                and lineStructure["playfield"]["pixels2"] == "1"
                  and lineStructure["sprites"]["pixels"] == "0"):
                OK[1]+=1
            elif (sums[assign["sprites"]]["pixels"][pixelNum] == "1"
                and lineStructure["sprites"]["pixels"] == "1"):
                OK[1] += 1

        if OK[0] > OK[1]:
            lineStructure["playfield"]["pixels"] = lineStructure["playfield"]["pixels1"][::-1]
            newPF = ""
            newPF2 = ""

            for pixelNum in range(0,32,4):
                part1 = sums[assign["background"]]["pixels"][pixelNum:(pixelNum + 4)]
                part2 = sums[assign["background"]]["pixels"][(63 - pixelNum - 4):(63 - pixelNum)][::-1]

                pfPart = lineStructure["playfield"]["pixels"][pixelNum:(pixelNum + 4)]

                for pixelNum2 in range(0,4):
                    if part1[pixelNum2] == part2[pixelNum2] and part1[pixelNum2] == pfPart[pixelNum2]:
                        newPF+=part1[pixelNum2]
                    elif part1[pixelNum2] == part2[pixelNum2] and part1[pixelNum2] != pfPart[pixelNum2]:
                        newPF += part1[pixelNum2]
                    elif part1[pixelNum2] == pfPart[pixelNum2] and part1[pixelNum2] != pfPart[pixelNum2]:
                        newPF += pfPart[pixelNum2]
                    elif part1[pixelNum2] != pfPart[pixelNum2] and part1[pixelNum2] == pfPart[pixelNum2]:
                        newPF += pfPart[pixelNum2]
                    else:
                        newPF += pfPart[pixelNum2]


            for pixelNum in range(0,32,4):
                p1 = int(newPF[pixelNum])
                p2 = int(newPF[pixelNum + 1])
                p3 = int(newPF[pixelNum + 2])
                p4 = int(newPF[pixelNum + 3])

                if (p1+p2+p3+p4) > 1:
                    newPF2+="1"
                else:
                    newPF2+="0"

            lineStructure["playfield"]["pixels"] = newPF2


        else:
            lineStructure["playfield"]["pixels"] = lineStructure["playfield"]["pixels2"][::-1]
            newPF = ""
            newPF2 = ""

            for pixelNum in range(0, 32, 4):
                part1 = sums[assign["background"]]["pixels"][pixelNum:(pixelNum + 4)]
                part2 = sums[assign["background"]]["pixels"][(63 - pixelNum - 4):(63 - pixelNum)][::-1]

                pfPart = lineStructure["playfield"]["pixels"][pixelNum:(pixelNum + 4)]

                for pixelNum2 in range(0, 4):
                    if part1[pixelNum2] == part2[pixelNum2] and part1[pixelNum2] == pfPart[pixelNum2]:
                        newPF += part1[pixelNum2]
                    elif part1[pixelNum2] == part2[pixelNum2] and part1[pixelNum2] != pfPart[pixelNum2]:
                        newPF += part1[pixelNum2]
                    elif part1[pixelNum2] == pfPart[pixelNum2] and part1[pixelNum2] != pfPart[pixelNum2]:
                        newPF += pfPart[pixelNum2]
                    elif part1[pixelNum2] != pfPart[pixelNum2] and part1[pixelNum2] == pfPart[pixelNum2]:
                        newPF += pfPart[pixelNum2]
                    else:
                        newPF += pfPart[pixelNum2]

            for pixelNum in range(0,32,4):
                p1 = int(newPF[pixelNum])
                p2 = int(newPF[pixelNum + 1])
                p3 = int(newPF[pixelNum + 2])
                p4 = int(newPF[pixelNum + 3])

                if (p1+p2+p3+p4) > 1:
                    newPF2+="1"
                else:
                    newPF2+="0"

            lineStructure["playfield"]["pixels"] = newPF2

            while ((lineStructure["playfield"]["color"] == lineStructure["sprites"]["color"] and
                    lineStructure["sprites"]["color"] != "$00") or
                   (lineStructure["playfield"]["color"] == lineStructure["background"] and lineStructure[
                       "background"] != "$00") or
                   (lineStructure["sprites"]["color"] == lineStructure["background"] and lineStructure[
                       "background"] != "$00")):

                lineStructure["playfield"]["color"], lineStructure["sprites"]["color"] = self.colorNoEqual(
                    lineStructure["playfield"]["color"], lineStructure["sprites"]["color"],
                    assign["playfield"], assign["sprites"])

                lineStructure["playfield"]["color"], lineStructure["background"] = self.colorNoEqual(
                    lineStructure["playfield"]["color"], lineStructure["background"],
                    assign["playfield"], assign["background"])

                lineStructure["background"], lineStructure["sprites"]["color"] = self.colorNoEqual(
                    lineStructure["background"], lineStructure["sprites"]["color"],
                    assign["background"], assign["sprites"])

        return (lineStructure)

    def colorNoEqual(self, color1, color2, assignVal1, assignVal2):
        while (
                color1 == color2 and color1 != "$00"
        ):

            currentVal1 = int("0x" + color1[2], 16)
            currentVal2 = int("0x" + color2[2], 16)

            if currentVal1 > 8:
                if assignVal1 > assignVal2:
                    currentVal2 -= 2
                else:
                    currentVal1 -= 2
            elif currentVal1 < 9:
                if assignVal1 > assignVal2:
                    currentVal1 += 2
                else:
                    currentVal2 += 2
            color1 = color1[:-1] + hex(currentVal1).replace("0x", "")
            color2 = color2[:-1] + hex(currentVal2).replace("0x", "")

        return (color1, color2)

    def getPFData(self, w, h, pixelData):
        for Y in range(0, h):
            row = []
            for X in range(0,40):
                if X < 20:
                    row.append(pixelData[X,Y]//255)
                elif X < 28:
                    if self.__mirroring[2] == 1:
                        row.append(pixelData[20-(X-19), Y] // 255)

                    else:
                        row.append(pixelData[X, Y] // 255)
                elif X < 36:
                    if self.__mirroring[1] == 1:
                        row.append(pixelData[20-(X-19), Y] // 255)

                    else:
                        row.append(pixelData[X, Y] // 255)
                else:
                    if self.__mirroring[0] == 1:
                        row.append(pixelData[20-(X-19), Y] // 255)

                    else:
                        row.append(pixelData[X, Y] // 255)

            for m in range(0, self.__multiH):
                self.pixels.append(deepcopy(row))


    def getColorData(self, w, h, colorData, pixelData):
        for Y in range(0, h):
            #sumPF = [0,0,0]
            #sumBG = [0,0,0]
            PF = [0,0,0]
            BG = [0,0,0]

            pfList = []
            bgList = []

            for X in range(0, w):
                if (pixelData[X,Y] == 255):
                    #for num in range(0,3):
                        #sumPF[num]+=colorData[X,Y][num]
                    try:
                        pfList.append((colorData[X,Y][0], colorData[X,Y][2], colorData[X,Y][1]))
                    except:
                        pfList.append((colorData[X,Y]))
                else:
                    #for num in range(0,3):
                        #sumBG[num]+=colorData[X,Y][num]
                    try:
                        bgList.append((colorData[X,Y][0], colorData[X,Y][2], colorData[X,Y][1]))
                    except:
                        bgList.append((colorData[X,Y]))


            """
            for num in range(0, 3):
                PF[num] = round(sumPF[num]/w)
                BG[num] = round(sumBG[num]/w)

            """
            PF = self.__colorDict.getDominantColor(pfList)
            BG = self.__colorDict.getDominantColor(bgList)



            for m in range(0, self.__multiH):
                if PF != None:
                    pfC = self.__colorDict.getClosestTIAColor(PF[0], PF[1], PF[2])
                else:
                    try:
                        pfC = self.bgColors[-1]
                    except:
                        pfC="$00"

                pfNum = int(pfC.replace("$", "0x"), 16)


                if BG != None:
                    bgC = self.__colorDict.getClosestTIAColor(BG[0], BG[1], BG[2])
                else:
                    try:
                        bgC = self.pfColors[-1]
                    except:
                        bgC="$00"

                bgNum = int(bgC.replace("$", "0x"), 16)


                if abs( pfNum - bgNum ) < 4:
                    if (int("0x"+bgC[2], 16))>8:
                        bgC = bgC[:2] + str(hex(int("0x"+bgC[2], 16)-4)).replace("0x", "")
                    else:
                        bgC = bgC[:2] + str(hex(int("0x"+bgC[2], 16)+4)).replace("0x", "")


                self.pfColors.append( bgC )
                self.bgColors.append( pfC )




    def __addElements(self, top):
        self.__topLevel = top
        self.__topLevelWindow = top.getTopLevel()

        self.__imageFrame = Frame(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("window"))
        self.__imageFrame.config(
            width=round(self.__topLevel.getTopLevelDimensions()[0] /3))
        self.__imageFrame.pack_propagate(False)
        self.__imageFrame.pack(side=LEFT, anchor=W, fill=Y)

        self.__tres=StringVar()

        if self.__mode == "64pxPicture":
            self.__tres.set("84")
        else:
            self.__tres.set("128")

        self.__controllerFrame = Frame(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("window"))
        self.__controllerFrame.config(
            width=round(self.__topLevel.getTopLevelDimensions()[0] /3))
        self.__controllerFrame.pack_propagate(False)
        self.__controllerFrame.pack(side=LEFT, anchor=W, fill=Y)

        self.__titleLabel = Label(self.__controllerFrame, text=self.__dictionaries.getWordFromCurrentLanguage("thresholdSetter"),
                                  bg = self.__loader.colorPalettes.getColor("window"),
                                  fg = self.__loader.colorPalettes.getColor("font"), justify = "center",
                                  font=self.__normalFont
                                  )
        self.__titleLabel.pack(side=TOP, anchor=N, fill=X)

        self.__number = Entry(self.__controllerFrame, text=self.__dictionaries.getWordFromCurrentLanguage("thresholdSetter"),
                                  bg = self.__loader.colorPalettes.getColor("boxBackNormal"),
                                  fg = self.__loader.colorPalettes.getColor("boxFontNormal"), justify = "center",
                                  textvariable=self.__tres, width=999999999,
                                  font=self.__normalFont
                              )

        self.__number.bind("<KeyRelease>", self.__checkNumber)

        self.__number.pack(side=TOP, anchor=N, fill=X)
        self.__minus = self.__loader.io.getImg("negative", None)
        self.__plus = self.__loader.io.getImg("positive", None)

        self.__cBoxFrame = Frame(self.__controllerFrame, bg=self.__loader.colorPalettes.getColor("window"))
        self.__cBoxFrame.config(
            width=round(self.__topLevel.getTopLevelDimensions()[0] / 2),
            height=round(self.__topLevel.getTopLevelDimensions()[1] / 6))
        self.__cBoxFrame.pack_propagate(False)
        self.__cBoxFrame.pack(side=TOP, anchor=N, fill=BOTH)

        if self.__mode == "playfield":
            self.__invert = IntVar()
            self.__invert.set(0)

            self.__check = Checkbutton(self.__cBoxFrame, text=self.__dictionaries.getWordFromCurrentLanguage("invert"),
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       fg=self.__loader.colorPalettes.getColor("font"),
                                       font=self.__smallFont,
                                       variable=self.__invert, command=self.updateBlackAndWhite
                                       )
            self.__check.pack(side=LEFT, anchor=W, fill=X)

            self.__right = IntVar()
            self.__right.set(0)

            self.__rightB = Checkbutton(self.__cBoxFrame,
                                       text=self.__dictionaries.getWordFromCurrentLanguage("preferRight"),
                                       bg=self.__loader.colorPalettes.getColor("window"),
                                       fg=self.__loader.colorPalettes.getColor("font"),
                                       font=self.__smallFont,
                                       variable=self.__right, command=self.updateBlackAndWhite
                                       )
            self.__rightB.pack(side=RIGHT, anchor=E, fill=X)
        elif self.__mode == "64pxPicture":
            self.__thisLabel = Label(self.__cBoxFrame, text=self.__dictionaries.getWordFromCurrentLanguage("name"),
                                  bg = self.__loader.colorPalettes.getColor("window"),
                                  fg = self.__loader.colorPalettes.getColor("font"), justify = "center",
                                  font=self.__smallFont
                                  )
            self.__thisLabel.pack(side=LEFT, anchor=E)

            self.__thisFrame = Label(self.__cBoxFrame,
                                  bg = self.__loader.colorPalettes.getColor("window"), width=99999999)
            self.__thisFrame.pack_propagate(False)
            self.__thisFrame.pack(side=LEFT, anchor=E, fill=BOTH)


            self.__thisVar = StringVar()
            self.__thisVar.set("Best_Picture_Ever")
            self.__thisEntry = Entry(self.__thisFrame,
                  bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                  fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                  textvariable=self.__thisVar, width=999999999,
                  font=self.__smallFont
                  )

            self.__thisEntry.pack(side=TOP, fill=BOTH)
            self.__thisEntry.bind("<KeyRelease>", self.__checkNumber)



        self.__buttonFrame = Frame(self.__controllerFrame, bg=self.__loader.colorPalettes.getColor("window"))
        if self.__mode == "64pxPicture":
            self.__buttonFrame.config(
            width=round(self.__topLevel.getTopLevelDimensions()[0] / 2), height=round(self.__topLevel.getTopLevelDimensions()[1] / 6))
        else:
            self.__buttonFrame.config(
            width=round(self.__topLevel.getTopLevelDimensions()[0] / 2), height=round(self.__topLevel.getTopLevelDimensions()[1] / 4))
        self.__buttonFrame.pack_propagate(False)
        self.__buttonFrame.pack(side=TOP, anchor=N, fill=BOTH)

        self.__minusButton = Button(self.__buttonFrame, width=round(self.__topLevel.getTopLevelDimensions()[0] / 6),
                                    bg=self.__loader.colorPalettes.getColor("window"),
                                    image=self.__minus, command=self.__neg
                                    )
        self.__minusButton.pack_propagate(False)
        self.__minusButton.pack(side=LEFT, anchor=W, fill=Y)
        self.__positiveButton = Button(self.__buttonFrame, width=round(self.__topLevel.getTopLevelDimensions()[0] / 6),
                                    bg=self.__loader.colorPalettes.getColor("window"),
                                    image=self.__plus, command=self.__pos
                                    )
        self.__positiveButton.pack_propagate(False)
        self.__positiveButton.pack(side=LEFT, anchor=E, fill=Y)


        self.__buttonFrame2 = Frame(self.__controllerFrame, bg=self.__loader.colorPalettes.getColor("window"))
        if self.__mode == "64pxPicture":
            self.__buttonFrame2.config(
            width=round(self.__topLevel.getTopLevelDimensions()[0] / 2),
            height = round(self.__topLevel.getTopLevelDimensions()[1] / 2))
        else:
            self.__buttonFrame2.config(
            width=round(self.__topLevel.getTopLevelDimensions()[0] / 2),
            height = round(self.__topLevel.getTopLevelDimensions()[1] / 3))
        self.__buttonFrame2.pack_propagate(False)
        self.__buttonFrame2.pack(side=TOP, anchor=N, fill=BOTH)

        self.__okButton = Button(self.__buttonFrame2,
                                    bg=self.__loader.colorPalettes.getColor("window"),
                                    fg=self.__loader.colorPalettes.getColor("font"),
                                    text=self.__dictionaries.getWordFromCurrentLanguage("ok"),
                                    font=self.__smallFont, command=self.setAndKill
                                    )
        self.__okButton.pack_propagate(False)
        self.__okButton.pack(side=TOP, anchor=E, fill=X)

        if self.__mode == "64pxPicture":
            self.__okButton.config(text=self.__dictionaries.getWordFromCurrentLanguage("savePicture"))
            self.__testButton = Button(self.__buttonFrame2,
                                        bg=self.__loader.colorPalettes.getColor("window"),
                                        fg=self.__loader.colorPalettes.getColor("font"),
                                        text=self.__dictionaries.getWordFromCurrentLanguage("preview")[:-1],
                                        font=self.__smallFont, command=self.testingThread
                                        )
            self.__testButton.pack_propagate(False)
            self.__testButton.pack(side=TOP, anchor=E, fill=X)


        self.__cancelButton = Button(self.__buttonFrame2,
                                    bg=self.__loader.colorPalettes.getColor("window"),
                                    fg=self.__loader.colorPalettes.getColor("font"),
                                    text=self.__dictionaries.getWordFromCurrentLanguage("cancel"),
                                    font=self.__smallFont, command=self.killMe
                                    )
        self.__cancelButton.pack_propagate(False)
        self.__cancelButton.pack(side=TOP, anchor=E, fill=X)

        if self.__mode == "64pxPicture":
            self.__okButton.config(font=self.__smallFont2)
            self.__testButton.config(font=self.__smallFont2)
            self.__cancelButton.config(font=self.__smallFont2)

        self.__imageFrame2 = Frame(self.__topLevelWindow, bg=self.__loader.colorPalettes.getColor("window"))
        self.__imageFrame2.config(
            width=round(self.__topLevel.getTopLevelDimensions()[0] /3))
        self.__imageFrame2.pack_propagate(False)
        self.__imageFrame2.pack(side=LEFT, anchor=W, fill=Y)

        self.blackAndWhite()

    def testingThread(self):
        from threading import Thread

        t = Thread(target=self.testing)
        t.daemon = True
        t.start()

    def testing(self):
        self.generateImage(self.__mode, self.__image, True)

    def killMe(self):
        self.__topLevelWindow.destroy()
        self.dead=True

    def setAndKill(self):
        self.doThings = True
        if self.__mode == "64pxPicture":
            self.__name = self.__thisVar.get()
        self.killMe()

    def __checkNumber(self, event):
        num = 0
        try:
            num = int(self.__tres.get())
        except:
            self.__number.config(
                bg=self.__loader.colorPalettes.getColor("boxBackUnSaved"),
                fg=self.__loader.colorPalettes.getColor("boxFontSaved")
            )
        self.__number.config(
            bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
            fg=self.__loader.colorPalettes.getColor("boxFontNormal")
            )

        if num<0:
            num = self.__tres.set("0")
        elif self.__mode == "64pxPicture" and num>128:
            num = self.__tres.set("128")
        elif self.__mode == "playfield" and num>255:
            num = self.__tres.set("255")

        self.updateBlackAndWhite()

    def __pos(self):
        num = int(self.__tres.get())

        if self.__mode == "64pxPicture" and num<117:
            self.__tres.set(str(num + 10))
        elif self.__mode == "playfield" and num<245:
            self.__tres.set(str(num+10))

        self.updateBlackAndWhite()


    def __neg(self):
        num = int(self.__tres.get())

        if num>10:
            self.__tres.set(str(num-10))

        self.updateBlackAndWhite()

    def blackAndWhite(self):

        from copy import deepcopy

        #for slave in self.__imageFrame.pack_slaves():
        #    slave.destroy()

        h = round(self.__topLevel.getTopLevelDimensions()[1])
        image = IMG.open(self.answer, "r")
        width, height = image.size

        multi = h / height
        w = round(image.width * multi)

        imageSized = image.resize((w, h), IMG.ANTIALIAS)


        self.img1 = ImageTk.PhotoImage(imageSized)

        self.label1 = Label(self.__imageFrame,
            height=round(self.__topLevel.getTopLevelDimensions()[1]), image = self.img1
            )
        self.label1.pack(side=LEFT, fill=BOTH)

        self.label2 = Label(self.__imageFrame2,
            height=round(self.__topLevel.getTopLevelDimensions()[1]), image=self.img1
            )
        self.label2.pack(side=RIGHT, fill=BOTH)
        self.updateBlackAndWhite()

    def updateBlackAndWhite(self):
        image = IMG.open(self.answer, "r")
        from PIL import ImageOps
        import numpy as np

        if self.__mode == "playfield":
            try:
                image = ImageOps.invert(image)
                image = ImageOps.invert(image)
            except:
                self.__check.config(state=DISABLED)

            if self.__invert.get():
                image = ImageOps.invert(image)

            if self.__right.get():
                from PIL import ImageOps
                image = ImageOps.mirror(image)

        width, height = image.size
        h = round(self.__topLevel.getTopLevelDimensions()[1])


        multi = h / height
        w = round(image.width * multi)
        imageSized = image.resize((w, h), IMG.ANTIALIAS)

        if self.__mode == "playfield":
            fn = lambda x: 255 if x > int(self.__tres.get()) else 0
            altImage = deepcopy(imageSized).convert('L').point(fn, mode='1')
        elif self.__mode == "64pxPicture":
            fn1 = lambda x: 255 if x > int(self.__tres.get()) else 0
            fn2 = lambda x: 255 if x > int(self.__tres.get())+128 else 0
            altImage1 = deepcopy(imageSized).convert('L').point(fn1, mode='1')
            altImage2 = deepcopy(imageSized).convert('L').point(fn2, mode='1')

            pixels1 = altImage1.load()
            pixels2 = altImage2.load()

            W, H = altImage1.size

            pixels = []

            for Y in range(0, H):
                for X in range(0, W):
                    value = (pixels1[X,Y] + pixels2[X,Y]  )//2
                    #pixels.append((value, value, value))
                    #data+=chr(value) + chr(value) + chr(value)
                    pixels.append(value)
                    pixels.append(value)
                    pixels.append(value)


            altImage = IMG.frombytes("RGB", (w, h), bytes(pixels))

            #altImage1.save("temp/temp.png")
            #altImage = IMG.open("temp/temp.png")

        self.img2 = ImageTk.PhotoImage(altImage)
        self.label2.config(image = self.img2)

if __name__ == "__main__":
    code = PictureToCode("C:\cat.jpg", "common", "playfield", None)
