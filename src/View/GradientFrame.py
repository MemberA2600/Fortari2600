from tkinter import *
from threading import Thread
from copy import deepcopy
from time import sleep
import re

class GradientFrame:

    def __init__(self, loader, frame, changeData, h, data, dead, height, fontSize, dataNum):
        self.__loader        = loader
        self.__mainFrame     = frame
        self.__changeData    = changeData
        self.__h             = round(h * 0.9)
        self.__data          = data
        self.dead            = dead
        self.height          = height
        self.__dataNum       = dataNum

        self.__config = self.__loader.config
        self.__dictionaries = self.__loader.dictionaries
        self.__screenSize = self.__loader.screenSize
        self.__soundPlayer = self.__loader.soundPlayer
        self.__fileDialogs = self.__loader.fileDialogs
        self.__fontManager = self.__loader.fontManager
        self.__fontSize = int(self.__screenSize[0] / 1300 * self.__screenSize[1] / 1050 * 14)
        self.__colors = self.__loader.colorPalettes
        self.__colorDict = self.__loader.colorDict

        self.__normalFont = self.__fontManager.getFont(self.__fontSize, False, False, False)
        self.__smallFont = self.__fontManager.getFont(int(self.__fontSize * 0.80), False, False, False)
        self.__miniFont = self.__fontManager.getFont(int(self.__fontSize * 0.65), False, False, False)
        self.__bigFont = self.__fontManager.getFont(int(self.__fontSize * 1.15), False, False, False)
        self.__bigFont2 = self.__fontManager.getFont(int(self.__fontSize * 1.5), False, False, False)

        self.__fontSize = fontSize
        self.__fonts = { "normal": self.__smallFont, "small": self.__miniFont}

        self.__optionsFrame  = Frame(self.__mainFrame, width=999999,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=self.__h // 3)

        self.__optionsFrame.pack_propagate(False)
        self.__optionsFrame.pack(side=TOP, anchor=N, fill=X)

        self.__canvas = Canvas(self.__mainFrame, bg="black", bd=0,
                               width=9999999,
                               height=self.__h)

        self.__canvas.pack_propagate(False)
        self.__canvas.pack(side=TOP, anchor=N, fill=BOTH)

        self.__option = IntVar()
        try:
            num = int(self.__data[self.__dataNum])
            self.__option.set(num)
        except:
            self.__option.set(1)

        self.__lastOption = 0
        t = Thread(target=self.addElements)
        t.daemon = True
        t.start()

    def addElements(self):
        while self.__optionsFrame.winfo_width() < 2:
            sleep(0.05)
        newH = self.__optionsFrame.winfo_height() // 4

        self.__frame1  = Frame(self.__optionsFrame, width=999999,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=newH)

        self.__frame1.pack_propagate(False)
        self.__frame1.pack(side=TOP, anchor=N, fill=X)

        self.__frame2  = Frame(self.__optionsFrame, width=999999,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=newH)

        self.__frame2.pack_propagate(False)
        self.__frame2.pack(side=TOP, anchor=N, fill=X)

        self.__frame3  = Frame(self.__optionsFrame, width=999999,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=newH)

        self.__frame3.pack_propagate(False)
        self.__frame3.pack(side=TOP, anchor=N, fill=X)

        self.__frame4  = Frame(self.__optionsFrame, width=999999,
                                   bg=self.__loader.colorPalettes.getColor("window"),
                                   height=newH)

        self.__frame4.pack_propagate(False)
        self.__frame4.pack(side=TOP, anchor=N, fill=X)

        self.__gradButton1 = Radiobutton( self.__frame1, width = 100,
                                             text=self.__dictionaries.getWordFromCurrentLanguage("gradient1"),
                                             bg=self.__colors.getColor("window"),
                                             fg=self.__colors.getColor("font"),
                                             justify=LEFT, font=self.__fonts[self.__fontSize],
                                             variable = self.__option,
                                             activebackground = self.__colors.getColor("highLight"),
                                             value = 1, name = "grad1"
        )

        self.__gradButton1.pack_propagate(False)
        self.__gradButton1.pack(fill=Y, side=LEFT, anchor=E)

        self.__gradButton2 = Radiobutton( self.__frame2, width = 100,
                                             text=self.__dictionaries.getWordFromCurrentLanguage("gradient2"),
                                             bg=self.__colors.getColor("window"),
                                             fg=self.__colors.getColor("font"),
                                             justify=LEFT, font=self.__fonts[self.__fontSize],
                                             variable = self.__option,
                                             activebackground = self.__colors.getColor("highLight"),
                                             value = 2, name = "grad2"
        )

        self.__gradButton2.pack_propagate(False)
        self.__gradButton2.pack(fill=Y, side=LEFT, anchor=E)

        self.__gradButton3 = Radiobutton( self.__frame3, width = 100,
                                             text=self.__dictionaries.getWordFromCurrentLanguage("gradient3"),
                                             bg=self.__colors.getColor("window"),
                                             fg=self.__colors.getColor("font"),
                                             justify=LEFT, font=self.__fonts[self.__fontSize],
                                             variable = self.__option,
                                             activebackground = self.__colors.getColor("highLight"),
                                             value = 3, name = "grad3"
        )

        self.__gradButton3.pack_propagate(False)
        self.__gradButton3.pack(fill=Y, side=LEFT, anchor=E)

        self.__gradButton4 = Radiobutton( self.__frame4, width = 100,
                                             text=self.__dictionaries.getWordFromCurrentLanguage("gradient4"),
                                             bg=self.__colors.getColor("window"),
                                             fg=self.__colors.getColor("font"),
                                             justify=LEFT, font=self.__fonts[self.__fontSize],
                                             variable = self.__option,
                                             activebackground = self.__colors.getColor("highLight"),
                                             value = 4, name = "grad4"
        )

        self.__gradButton4.pack_propagate(False)
        self.__gradButton4.pack(fill=Y, side=LEFT, anchor=E)

        self.__gradButton1.bind("<ButtonRelease-1>", self.XXX)
        self.__gradButton2.bind("<ButtonRelease-1>", self.XXX)
        self.__gradButton3.bind("<ButtonRelease-1>", self.XXX)
        self.__gradButton4.bind("<ButtonRelease-1>", self.XXX)

        while self.__canvas.winfo_width() < 2:
            sleep(0.005)


        self.reDrawCanvas()

    def reDrawCanvas(self):
        data = self.generateData()

        h = self.__canvas.winfo_height() // self.height
        self.__canvas.clipboard_clear()
        self.__canvas.delete("all")

        for colorNum in range(0, len(data)):
            color = self.__loader.colorDict.getHEXValueFromTIA(data[colorNum])
            self.__canvas.create_rectangle(0, colorNum * h,
                                           self.__canvas.winfo_width(),
                                           (colorNum + 1) * h,
                                           outline = "",
                                           fill = color
                                           )

    def generateData(self):
        data = []
        step = self.height // 4

        pattern = {
            1: [step * 4, step * 4, step * 3, step * 3, step * 2, step * 2, step * 1, step * 1],
            2: [step * 1, step * 1, step * 2, step * 2, step * 3, step * 3, step * 4, step * 4],
            3: [step * 1, step * 2, step * 3, step * 4, step * 4, step * 3, step * 2, step * 1],
            4: [step * 4, step * 3, step * 2, step * 1, step * 1, step * 2, step * 3, step * 4]
        }

        if self.__data[5].startswith("$"):
            baseColorNum = self.__data[5][1]
        else:
            baseColorNum = self.__loader.mainWindow.getLoopColor()[1]

        for num in pattern[self.__option.get()]:
            num = hex(num).replace("0x", "")
            while len(num) < 2:
                num = "0" + num
            num = "$" + baseColorNum + num[1]

            data.append(num)

        return(data)

    def XXX(self, event):
        name = int(str(event.widget).split(".")[-1][-1])
        self.__option.set(name)

        self.reDrawCanvas()
        self.__data[self.__dataNum] = str(self.__option.get())
        self.__changeData(self.__data)
