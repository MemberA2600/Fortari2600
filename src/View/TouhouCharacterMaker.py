from tkinter import *
import os

class TouhouCharacterMaker:
    def __init__(self, loader):

        self.dead = False

        self.__loader = loader
        self.__dictionaries = self.__loader.dictionaries

        self.__config = self.__loader.config
        self.__dictionaries = self.__loader.dictionaries
        self.__screenSize = self.__loader.screenSize
        self.__soundPlayer = self.__loader.soundPlayer
        self.__fileDialogs = self.__loader.fileDialogs

        from FontManager import FontManager
        self.__fontManager = FontManager(self.__loader)

        self.__fontSize = int(self.__screenSize[0]/1300 * self.__screenSize[1]/1050*14)
        self.__colors = self.__loader.colorPalettes
        self.__colorDict = self.__loader.colorDict

        self.__first   = True
        self.__focused = None
        self.__screenSize = self.__loader.screenSize

        self.__largeFont = self.__fontManager.getFont(self.__fontSize*1.3, False, False, False)
        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize * 0.80), False, False, False)
        self.__smallerFont = self.__fontManager.getFont(int(self.__fontSize * 0.65), False, False, False)

        w = round(self.__screenSize[0] / 2)
        h = round(self.__screenSize[1]/2  - 40)

        self.__topLevelWindow  = Toplevel()
        self.__topLevelWindow.title("Touhou Character Maker")
        self.__topLevelWindow.geometry("%dx%d+%d+%d" % (w, h, (self.__screenSize[0]/2-w/2), (self.__screenSize[1]/2-h/2-50)))
        self.__topLevelWindow.resizable(False, False)

        self.__topLevelWindow.config(bg=self.__loader.colorPalettes.getColor("window"))
        self.__topLevelWindow.iconbitmap("others/img/icon.ico")

        self.__topLevelWindow.deiconify()
        self.__topLevelWindow.focus()

        self.__addElements(self)

        try:
            from os import mkdir
            mkdir("temp/")
        except:
            pass

        self.__topLevelWindow.mainloop()
        self.dead = True

        try:
            from shutil import rmtree
            rmtree('temp/')
        except:
            pass

    def getTopLevelDimensions(self):
        return(round(self.__screenSize[0] / 3),
               round(self.__screenSize[1]/3  - 40))

    def __addElements(self, top):
        self.__topLevel = top

        self.__numOfFrames  = 0
        self.__currentFrame = -1
        self.__frameNumSTR = StringVar()
        self.__frameNumSTR.set("0")

        self.__data = []
        self.__colorData = []

        from time import sleep
        while self.__topLevelWindow.winfo_width() < 2: sleep(0.0000001)

        self.__sizes = [self.__topLevelWindow.winfo_width() // 5 * 2, self.__topLevelWindow.winfo_width() // 5, self.__topLevelWindow.winfo_width() * 2]

        self.__upperFrame     = Frame(self.__topLevelWindow,
                                      bg = self.__loader.colorPalettes.getColor("window"),
                                      width = self.__topLevelWindow.winfo_width(), height = self.__topLevelWindow.winfo_height() // 8 * 7

                                      )
        self.__upperFrame.pack_propagate(False)
        self.__upperFrame.pack(side=TOP, anchor=N, fill=X)

        self.__lowerFrame = Frame(self.__topLevelWindow,
                                  bg=self.__loader.colorPalettes.getColor("window"),
                                  width=self.__topLevelWindow.winfo_width(),
                                  height=self.__topLevelWindow.winfo_height() // 8

                                  )
        self.__lowerFrame.pack_propagate(False)
        self.__lowerFrame.pack(side=TOP, anchor=N, fill=X)

        self.__upperFrameSubs = []

        h = self.__topLevelWindow.winfo_height() // 8 * 7 // 24

        for num in range(0, 3):
            self.__upperFrameSubs.append(Frame(self.__upperFrame,
                                      bg = self.__loader.colorPalettes.getColor("window"),
                                      width = self.__sizes[num],
                                      height = self.__topLevelWindow.winfo_height() // 8 * 7))

            self.__upperFrameSubs[-1].pack_propagate(False)
            self.__upperFrameSubs[-1].pack(side=LEFT, anchor=E, fill=Y)

            if    num == 0:
                  self.__buttons      = []
                  self.__buttonFrames = []

                  w = self.__sizes[num] // 16

                  self.__addToDataBlank()

                  for numH in range(0, 24):
                      self.__buttonFrames.append(Frame(self.__upperFrameSubs[num],
                                          bg = self.__loader.colorPalettes.getColor("boxBackNormal"),
                                          width = self.__sizes[num],
                                          height = h))

                      self.__buttonFrames[-1].pack_propagate(False)
                      self.__buttonFrames[-1].pack(side=TOP, anchor=N, fill=X)

                      b = self.__buttonFrames[-1]
                      self.__buttons.append([])

                      for numW in range(0, 16):
                          self.__buttonFrames.append(Frame(b,
                                                           bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                                           width = w,
                                                           height=h))

                          self.__buttonFrames[-1].pack_propagate(False)
                          self.__buttonFrames[-1].pack(side=LEFT, anchor=W, fill=Y)

                          self.__buttons[-1].append(
                              Button(self.__buttonFrames[-1],
                                     bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                     width=w, height=h, activebackground = self.__loader.colorPalettes.getColor("highLight"),
                                     name = str(numH) + "_" + str(numW), relief=GROOVE)
                          )

                          self.__buttons[-1][-1].pack_propagate(False)
                          self.__buttons[-1][-1].pack(side=TOP, anchor=N, fill=BOTH)

                          self.__buttons[-1][-1].bind("<Button-1>", self.__clicked)

            elif  num == 1:
                  self.__colorFrames  = []
                  self.__colorEntries = []
                  w = self.__sizes[num] // 4

                  for numH in range(0, 24):
                      self.__colorFrames.append(Frame(self.__upperFrameSubs[num],
                                          bg = self.__loader.colorPalettes.getColor("boxBackNormal"),
                                          width = self.__sizes[num],
                                          height = h))

                      self.__colorFrames[-1].pack_propagate(False)
                      self.__colorFrames[-1].pack(side=TOP, anchor=N, fill=X)

                      b = self.__colorFrames[-1]
                      self.__colorEntries.append([])

                      for numW in range(0, 4):
                          self.__colorFrames.append(Frame(b,
                                                          bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                                                          width=w,
                                                          height=h))

                          self.__colorFrames[-1].pack_propagate(False)
                          self.__colorFrames[-1].pack(side=LEFT, anchor=E, fill=Y)

                          from HexEntry2 import HexEntry

                          self.__colorEntries[-1].append(
                              HexEntry(self.__loader, self.__colorFrames[-1], self.__colors,
                              self.__colorDict, self.__smallerFont, ["$0e", "$1e", "$88", "$44"],
                                       numW, None, self.__setColorData))
            elif  num == 2:
                  self.__canvas = Canvas(self.__upperFrameSubs[num], bg="black", bd=0,
                                       width=self.__sizes[num], relief='ridge',
                                       height=h * 24 - 3
                                       )

                  self.__canvas.pack_propagate(False)
                  self.__canvas.pack(side=TOP, anchor=N, fill=X)

        self.__backImage = self.__loader.io.getImg("backwards", (48,48))
        self.__forImage = self.__loader.io.getImg("forwards", (48,48))
        self.__saveImage = self.__loader.io.getImg("open", (48,48))
        self.__openImage = self.__loader.io.getImg("save", (48,48))
        self.__pozImage = self.__loader.io.getImg("positive", (48,48))
        self.__negImage = self.__loader.io.getImg("negative", (48,48))

        self.__controllerFrames = []

        self.__icons = [self.__backImage, None, self.__forImage, self.__pozImage, self.__negImage, self.__openImage, self.__saveImage]
        self.__controllers = []
        self.__functions   = [self.prevFrame, None, self.nextFrame, self.__addToDataBlank, self.__deleteCurrent, self.__save, self.__open]

        w = self.__topLevelWindow.winfo_width() // len(self.__icons)
        h = self.__topLevelWindow.winfo_height() // 8

        for num in range(0, len(self.__icons)):
            self.__controllerFrames.append(Frame(self.__lowerFrame,
                                            bg=self.__loader.colorPalettes.getColor("window"),
                                            width=w,
                                            height=h))
            self.__controllerFrames[-1].pack_propagate(False)
            self.__controllerFrames[-1].pack(side=LEFT, anchor=E, fill=Y)

            if self.__icons[num] != None:
               self.__controllers.append(
                   Button(self.__controllerFrames[-1], bg=self.__loader.colorPalettes.getColor("window"),
                                   image=self.__icons[num],
                                   width= w,
                                   command=self.__functions[num])
               )
            else:
                self.__controllers.append(
                    Entry(self.__controllerFrames[-1], bg=self.__loader.colorPalettes.getColor("boxBackNormal"),
                          width=99,
                          fg=self.__loader.colorPalettes.getColor("boxFontNormal"),
                          textvariable=self.__frameNumSTR, name="frameNum",
                          font=self.__largeFont, justify=CENTER, state = DISABLED,
                          command=self.__functions[num])
                )

            self.__controllers[-1].pack_propagate(False)
            self.__controllers[-1].pack(side=LEFT, anchor=W, fill=BOTH)

    def prevFrame(self):
        if self.__numOfFrames == 1 or self.__currentFrame == 0: return

        self.__currentFrame -= 1
        self.__recolorPixels()

    def nextFrame(self):
        if self.__numOfFrames == 1 or self.__currentFrame == self.__numOfFrames - 1: return

        self.__currentFrame += 1
        self.__recolorPixels()

    def __recolorPixels(self):
        for y in range(0, 24):
            for x in range(0, 16):
                self.__colorPixel(y, x, None)

        self.__frameNumSTR.set(str(self.__currentFrame))
        self.__redrawCanvas()


    def __setColorData(self, event):
        gotIt = False
        for y in range(0, 24):
            for x in range(0, 4):
                if event.widget == self.__colorEntries[y][x].getEntry():
                   gotIt = True
                   break

            if gotIt: break

        self.__colorData[y][x] = self.__colorEntries[y][x].getValue()

        self.__redrawCanvas()
        #print(self.__colorEntries[y][x].getValue())
        #print(y, x, self.__colorEntries[y][x].getValue())


    def __addToDataBlank(self):
        from copy import deepcopy

        self.__data.insert(self.__currentFrame + 1, [])

        self.__numOfFrames  += 1
        self.__currentFrame += 1

        for n in range(0, 24):
            self.__data[self.__currentFrame].append([0] * 16)
            self.__colorData.append(["$0e", "$1e", "$88", "$44"])

        self.__frameNumSTR.set(str(self.__currentFrame))

        if self.__first:
           self.__first = False
        else:
           self.__recolorPixels()


    def __clicked(self, event):
        name = str(event.widget).split(".")[-1]

        y = int(name.split("_")[0])
        x = int(name.split("_")[1])

        self.__data[self.__currentFrame][y][x] = (self.__data[self.__currentFrame][y][x] + 1) % 3
        self.__colorPixel(y, x, self.__data[self.__currentFrame][y][x])
        self.__redrawCanvas()

    def __colorPixel(self, y, x, val):
        if val == None:
           val =  self.__data[self.__currentFrame][y][x]

        colors = [self.__loader.colorPalettes.getColor("boxBackNormal"),
                  self.__loader.colorPalettes.getColor("boxFontNormal"),
                  self.__loader.colorPalettes.getColor("boxBackUnSaved")]

        if val > 0 or self.__numOfFrames == 1:
           self.__buttons[y][x].config(bg = colors[val])
        else:
            if self.__currentFrame > 0:
               lastFrame = self.__currentFrame - 1
            else:
               lastFrame = self.__numOfFrames - 1

            colors2 = [self.__loader.colorPalettes.getColor("boxBackNormal"),
                       self.__loader.colorPalettes.getColor("boxFontUnSaved"),
                       self.__loader.colorPalettes.getColor("boxFontUnSaved")
                       ]

            self.__buttons[y][x].config(bg=colors2[self.__data[lastFrame][y][x]])

    def __deleteCurrent(self):
        if self.__numOfFrames == 1: return 
        
        self.__numOfFrames  -= 1
        
        self.__data.pop(self.__currentFrame)
        self.__currentFrame -= 1
        
        if self.__currentFrame < 0: self.__currentFrame = self.__numOfFrames - 1
        
        self.__frameNumSTR.set(str(self.__currentFrame))
        self.__recolorPixels()

    def __redrawCanvas(self):
        self.__canvas.clipboard_clear()
        self.__canvas.delete("all")

        stepX = self.__canvas.winfo_width()  // 16
        stepY = self.__canvas.winfo_height() // 24

        for y in range(0, 24):
            colors = [
                self.__colorData[y][0],
                self.__colorData[y][1],
                self.__colorData[y][2],
                self.__colorData[y][3]
            ]

            for x in range(0, 16):
                if x > 7:
                   adder = 2
                else:
                   adder = 0

                if self.__data[self.__currentFrame][y][x] != 0:
                   num = self.__data[self.__currentFrame][y][x] - 1 + adder

                   self.__canvas.create_rectangle(x * stepX, y * stepY, (x + 1) * stepX, (y + 1) * stepY,
                                               outline = "", fill=self.__colorDict.getHEXValueFromTIA(colors[num]))

    def __save(self):
        fileName = self.__fileDialogs.askForFileName("saveFile", True, ["a26", "*"],
                                                      "*")
        if fileName == "": return

        f = open(fileName, "w")
        f.write(str(self.__numOfFrames) + "\n")

        for fNum in range(0, self.__numOfFrames):
            for y in range(0,24):
                string = ""

                for x in range(0,16):
                    string += str(self.__data[fNum][y][x]) + " "

                string += " ".join(self.__colorData[y])

                f.write(string + '\n')
        f.close()

        if fileName.endswith(".a26"): fileName = fileName.replace(".a26", ".asm")

        f = open(fileName, "w")

        spriteSides = ["L", "R"]
        spriteNums  = ["P0", "P1"]

        toWrite = ""

        for spriteSide in range(0, 2):
            for spriteNum in range(0, 2):
                label = "#NAME#_" + spriteSides[spriteSide] + "_" + spriteNums[spriteNum] + "_Pointers"
                
                text = "\t_align\t" + str(self.__numOfFrames * 2) + "\n" + label + "\n"
                for fNum in range(0, self.__numOfFrames):
                    for zzz in ("<", ">"):
                        text += "\tBYTE\t#" + zzz + "#NAME#_" + spriteSides[spriteSide] + "_" + spriteNums[spriteNum] + "_" + str(fNum) + "\n"

                toWrite += text + "\n"

        for fNum in range(0, self.__numOfFrames):
            for spriteSide in range(0, 2):
                for spriteNum in range(0, 2):
                    label = "#NAME#_" + spriteSides[spriteSide] + "_" + spriteNums[spriteNum] + "_" + str(fNum)

                    text = "\t_align\t24\n" + label + "\n"
                    for y in range(23, -1, -1):
                        theByte = ""
                        
                        for x in range(spriteSide * 8, (spriteSide + 1) * 8 ):
                            if self.__data[fNum][y][x] == spriteNum + 1:
                               theByte += "1"
                            else:
                               theByte += "0"

                        text += "\tBYTE\t#%" + theByte + "\n"
                    toWrite += text + "\n"

        for spriteSide in range(0, 2):
            for spriteNum in range(0, 2):
                label = "#NAME#_" + spriteSides[spriteSide] + "_" + spriteNums[spriteNum] + "_Color"
                text = "\t_align\t24\n" + label + "\n"

                for y in range(23, -1, -1):
                    text += "\tBYTE\t#" + self.__colorData[y][spriteNum + (spriteSide * 2)] + "\n"

                toWrite += text + "\n"

        f.write(toWrite)
        f.close()

    def __open(self):
        fileName = self.__fileDialogs.askForFileName("openFile", False, ["a26", "*"],
                                                      "*")
        if fileName == "": return

        try:
            f = open(fileName, "r")
            lines = f.read().replace("\r","").split("\n")
            f.close()

            numOfLines = int(lines[0])
            self.__numOfFrames  = 0
            self.__currentFrame = -1

            lines.pop(0)
            self.__data = []
            self.__colorData = []

            for fNum in range(0, numOfLines):
                self.__addToDataBlank()
                for y in range(0, 24):
                    line = lines[y + (fNum * 24)].split(" ")
                    for x in range(0,20):
                        if x > 15:
                           cNum = x - 16
                           self.__colorData[y][cNum] = line[x]
                           self.__colorEntries[y][cNum].setValue(line[x])
                        else:
                           self.__data[fNum][y][x] = int(line[x])

            self.__recolorPixels()

        except Exception as e:
            import traceback

            print(traceback.print_exc())

