from tkinter import Frame
from threading import Thread

class FrameContent:

    def __init__(self, boss, master, w, h, x, y):
        self.__boss = boss
        self.__frame = Frame(master, width=w, height=h)
        self.__frame.pack_propagate()
        self.__frame.grid_propagate()
        self.__frame.place(x=x, y=y)
        self.__baseW = w
        self.__baseH = h
        self.__baseX = x
        self.__baseY = y
        self.__originalW = self.__boss.getWindowSize()[0]
        self.__originalH = self.__boss.getWindowSize()[1]
        self.__lastW = self.__boss.getWindowSize()[0]
        self.__lastH = self.__boss.getWindowSize()[1]
        align = Thread(target=self.dinamicallyAlign)
        align.start()

    def getFrame(self):
        return(self.__frame)

    def getFrameSize(self):
        return (self.__frame.winfo_width(), self.__frame.winfo_height())

    def dinamicallyAlign(self):
        from time import sleep
        while True:
            sleep(0.01)
            if (self.__lastW==self.__boss.getWindowSize()[0] and self.__lastH==self.__boss.getWindowSize()[1]):
                continue
            self.__lastW = self.__boss.getWindowSize()[0]
            self.__lastH = self.__boss.getWindowSize()[1]
            horMulti = self.__lastW / self.__originalW
            verMulti = self.__lastH / self.__originalH
            self.__frame.config(width=self.__baseW*horMulti)
            self.__frame.config(height=self.__baseH*verMulti)
            self.__frame.place(x=self.__baseX*horMulti, y=self.__baseY*verMulti)