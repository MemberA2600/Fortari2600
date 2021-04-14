from tkinter import Frame
from threading import Thread

class FrameContent:

    def __init__(self, loader, name, w, h, x, y, maxW, maxH):

        self.__loader = loader
        self.__loader.frames[name] = self


        self.__frame = Frame(self.__loader.tk, width=w, height=h)
        self.__frame.pack_propagate()
        self.__frame.grid_propagate()
        self.__frame.place(x=x, y=y)
        self.__baseW = w
        self.__baseH = h
        self.__baseX = x
        self.__baseY = y

        self.__maxW = maxW
        self.__maxH = maxH

        self.__changeSize()

        self.__lastScaleX = self.__loader.mainWindow.getScales()[0]
        self.__lastScaleY = self.__loader.mainWindow.getScales()[1]
        align = Thread(target=self.dinamicallyAlign)
        #self.__frame.config(bg="black") #Only for testing!
        align.daemon = True
        align.start()

    def getFrame(self):
        return(self.__frame)

    def getFrameSize(self):
        return (self.__frame.winfo_width(), self.__frame.winfo_height())

    def dinamicallyAlign(self):
        from time import sleep
        while True:
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

        self.__frame.config(width=self.__tempW)
        self.__frame.config(height=self.__tempH)

        self.__frame.place(x=self.__baseX * self.__lastScaleX, y=self.__baseY * self.__lastScaleY)