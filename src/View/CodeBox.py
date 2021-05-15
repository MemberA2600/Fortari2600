from tkinter import scrolledtext
from tkinter import *
from threading import Thread

class CodeBox:

    def __init__(self, loader, editor, frame):

        self.__loader = loader
        self.keyPress = False

        self.__bank = self.__loader.BFG9000.getSelected()[0]
        self.__section = self.__loader.BFG9000.getSelected()[1]
        self.__editor = editor
        self.__frame = frame
        self.__config = self.__loader.config

        self.__lastScaleX = self.__editor.getScales()[0]
        self.__lastScaleY = self.__editor.getScales()[1]

        self.box = scrolledtext.ScrolledText(self.__frame, width=999999, height=9999999, wrap=WORD)
        self.box.config(bg = self.__loader.colorPalettes.getColor("boxBackNormal"),
                          fg=self.__loader.colorPalettes.getColor("boxFontNormal"))

        self.getFont()
        self.box.pack(side=BOTTOM, anchor=S, fill=BOTH)
        self.loadCode()
        self.__loader.currentEditor = self.box

        self.stopThread = False
        self.__loader.stopThreads.append(self)

        t = Thread(target=self.checker)
        t.daemon = True
        t.start()


        self.box.bind("<Key>", self.keyPressed)
        self.box.bind("<KeyRelease>", self.keyReleased)



    def getFont(self):
        baseSize = int(self.__config.getValueByKey("codeBoxFont"))
        w = self.__editor.getWindowSize()[0] / 955
        h = self.__editor.getWindowSize()[1] / 686

        self.__fontSize = (baseSize * w * h)
        self.__font = self.__loader.fontManager.getFont(round(self.__fontSize), False, False, False)
        self.box.config(font=self.__font)

    def loadCode(self):
        self.box.delete(1.0, END)
        self.box.insert(1.0, self.__loader.virtualMemory.codes[self.__bank][self.__section].code)

    def checker(self):
        from time import sleep
        while (self.__loader.mainWindow.dead == False and self.stopThread==False):

            if (self.keyPress==True):
                sleep(0.5)
                if (self.keyPress == False):
                    self.__loader.BFG9000.saveAllCode()


            sleep(0.05)

    def keyPressed(self, event):
        self.keyPress = True
        self.__editor.changed = True

    def keyReleased(self, event):
        self.keyPress = False
