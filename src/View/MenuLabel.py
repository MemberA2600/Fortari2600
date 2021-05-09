from threading import Thread
from tkinter import Label

class MenuLabel:

    def __init__(self, loader, frame, text, XPoz, fontmanager):
        self.__loader = loader

        self.__frame = frame
        self.__XPoz = XPoz
        self.__fontManager = fontmanager

        self.stopThread = False
        self.__loader.stopThreads.append(self)

        self.__contentHolder = self.__frame.getFrame()
        self.__label = Label(self.__contentHolder, text = text)

        self.__font = None
        self.__lastScaleX = self.__loader.mainWindow.getScales()[0]
        self.__lastScaleY = self.__loader.mainWindow.getScales()[1]
        self.__label.config(bg=self.__loader.colorPalettes.getColor("window"))



        self.__placer()
        align = Thread(target=self.dinamicallyAlign)
        align.daemon = True
        align.start()
        self.__setFont()

    def dinamicallyAlign(self):
        from time import sleep
        while self.__loader.mainWindow.dead==False and self.stopThread==False:
            if (self.__lastScaleX==self.__loader.mainWindow.getScales()[0]
                    and self.__lastScaleY==self.__loader.mainWindow.getScales()[1]):
                sleep(0.05)
                continue
            self.__lastScaleX = self.__loader.mainWindow.getScales()[0]
            self.__lastScaleY = self.__loader.mainWindow.getScales()[1]

            self.__placer()
            self.__setFont()
            sleep(0.02)

    def __placer(self):
        c = self.__loader.mainWindow.getConstant()
        self.__label.place(x=(self.__XPoz*c) +
                              (self.__XPoz*10*self.__frame.getFrameSize()[0]/600)+5, y = c*1.04+12)

    def __setFont(self):
        self.__font = self.__fontManager.getFont("normal", False, False, False)
        self.__label.config(font=self.__font)

    def setText(self, string):
        self.__label.config(text=string)

    def changePlace(self, num):
        self.__XPoz = num
        self.__placer()

    def changeColor(self, color):
        self.__label.config(fg=color)