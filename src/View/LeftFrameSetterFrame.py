from tkinter import *
from threading import Thread

class LeftFrameSetterFrame:

    def __init__(self, loader, name, frame, title, father, height, baseSize, val, view,
                 addItems, applyFunction, valider, buttontText):
        self.__loader = loader
        self.__frame = frame
        self.__father = father
        self.__baseSize = baseSize
        self.__height=height
        self.__bank=val
        self.__section=view
        self.__name = name

        if name == "deliminatorFrame":
            self.delimiterChangerValid = valider
        elif name == "replacerFrame":
            self.replaceChangerValid = valider

        self.stopThread = False
        self.__loader.stopThreads.append(self)

        self.__h = self.__frame.winfo_height()*height

        self.__originalW = self.__frame.winfo_width()
        self.__originalH = self.__frame.winfo_height()

        self.__thisFrame = Frame(self.__frame, height=round(self.__h))
        self.__thisFrame.config(bg=self.__loader.colorPalettes.getColor("window"))

        self.__thisFrame.pack_propagate(False)
        self.__thisFrame.pack(side=TOP, anchor=NW, fill=X)

        self.__title = Label(self.__thisFrame, text = self.__loader.dictionaries.getWordFromCurrentLanguage(title), anchor="w")
        self.__title.config(bg=self.__loader.colorPalettes.getColor("window"))
        self.__title.config(fg=self.__loader.colorPalettes.getColor("font"))
        self.__title.pack(side=TOP, anchor=NE, fill=X)

        self.__lastX = self.__father.getScales()[0]
        self.__lastY = self.__father.getScales()[1]
        self.addedItems = []

        self.__loader.frames[name] = self

        if buttontText == None:
            buttontText = self.__loader.dictionaries.getWordFromCurrentLanguage("applyChanges")
        else:
            buttontText = self.__loader.dictionaries.getWordFromCurrentLanguage(buttontText)

        self.applyButton = Button(self.__thisFrame, text = buttontText)
        self.applyButton.config(bg=self.__loader.colorPalettes.getColor("window"))
        self.applyButton.config(fg=self.__loader.colorPalettes.getColor("font"))

        self.__applyFunction = applyFunction
        self.applyButton.config(command=self.__applyFunction)
        self.applyButton.pack(side=BOTTOM, fill=X)

        addItems(self, self.__thisFrame, self.addedItems)
        self.setFont()
        self.__title.config(font=self.__font)
        self.applyButton.config(font = self.__smallFont)

        t = Thread(target=self.sizing)
        t.daemon = True
        t.start()

    def disableButton(self):
        self.applyButton.config(state=DISABLED)

    def enableButton(self):
        self.applyButton.config(state=NORMAL)

    def setFont(self):
        w = self.__father.getSizes()[0]/640
        h = self.__father.getSizes()[1]/320
        self.__fontSize = (self.__baseSize*w*h)
        self.__font = self.__loader.fontManager.getFont(round(self.__fontSize), False, False, False)
        self.__smallFont = self.__loader.fontManager.getFont(round(self.__fontSize*0.8), False, False, False)
        for item in self.addedItems:
            try:
                item.config(font=self.__smallFont)
            except:
                pass

    def sizing(self):
        from time import sleep
        while self.__loader.mainWindow.dead==False and self.stopThread==False:
            if (self.__lastX != self.__father.getScales()[0] or
                self.__lastY != self.__father.getScales()[1]
            ):
                self.__lastX = self.__father.getScales()[0]
                self.__lastY = self.__father.getScales()[1]



                self.__h = self.__frame.winfo_height() * self.__height
                self.__thisFrame.config(height=round(self.__h))
                self.setFont()
                self.__title.config(font=self.__font)
                self.applyButton.config(font=self.__smallFont)
            if self.__name == "deliminatorFrame":
                self.delimiterChangerValid(self, self.entryVar)
            elif self.__name == "replacerFrame":
                self.replaceChangerValid(self, self.originalText)

            sleep(0.04)