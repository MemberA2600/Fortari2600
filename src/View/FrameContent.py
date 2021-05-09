from tkinter import Frame
from threading import Thread

class FrameContent:

    def __init__(self, loader, name, w, h, x, y, maxW, maxH, minW, minH):

        self.__loader = loader
        self.__loader.frames[name] = self

        self.stopThread = False
        #self.__loader.stopThreads.append(self)

        self.__frame = Frame(self.__loader.tk, width=w, height=h)
        self.__frame.pack_propagate(False)
        self.__frame.grid_propagate(False)
        self.__frame.place(x=x, y=y)
        self.__baseW = w
        self.__baseH = h
        self.__baseX = x
        self.__baseY = y

        self.__maxW = maxW
        self.__maxH = maxH
        self.__minW = minW
        self.__minH = minH


        self.__changeSize()

        self.__lastScaleX = self.__loader.mainWindow.getScales()[0]
        self.__lastScaleY = self.__loader.mainWindow.getScales()[1]
        align = Thread(target=self.dinamicallyAlign)
        self.__frame.config(bg=self.__loader.colorPalettes.getColor("window"))

        #self.__frame.config(bg="blue") #Only for testing!
        align.daemon = True
        align.start()

    def getFrame(self):
        return(self.__frame)

    def getFrameSize(self):
        return (self.__frame.winfo_width(), self.__frame.winfo_height())

    def dinamicallyAlign(self):
        from time import sleep
        while self.__loader.mainWindow.dead==False and self.stopThread==False:
            if (self.__lastScaleX==self.__loader.mainWindow.getScales()[0]
                    and self.__lastScaleY==self.__loader.mainWindow.getScales()[1]):
                sleep(0.05)
                continue
            self.__changeSize()
            sleep(0.02)

    def __changeSize(self):

        self.__lastScaleX = self.__loader.mainWindow.getScales()[0]
        self.__lastScaleY = self.__loader.mainWindow.getScales()[1]

        self.__tempW = self.__baseW * self.__lastScaleX
        self.__tempH = self.__baseH * self.__lastScaleY
        if self.__tempW > self.__maxW:
            self.__tempW = self.__maxW
        if self.__tempH > self.__maxH:
            self.__tempH = self.__maxH

        if self.__tempW < self.__minW:
            self.__tempW = self.__minW
        if self.__tempH < self.__minH:
            self.__tempH = self.__minH

        self.__frame.config(width=self.__tempW)
        self.__frame.config(height=self.__tempH)

        self.__frame.place(x=self.__baseX * self.__lastScaleX, y=self.__baseY * self.__lastScaleY)