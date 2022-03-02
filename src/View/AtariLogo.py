from tkinter import *
from PIL import Image as IMAGE, ImageTk
from threading import Thread

class AtariLogo:

    def __init__(self, loader, main, left, right):
        self.__loader = loader
        self.__main = main
        self.__left = left
        self.__right = right

        self.__frames = self.__loader.atariFrames
        self.__counter = 0

        self.stopThread = False
        self.__loader.stopThreads.append(self)

        from SpaceShip import SpaceShip
        self.__spaceShip1 = SpaceShip(self.__loader, self.__left)
        self.__spaceShip2 = SpaceShip(self.__loader, self.__right)
        self.__spaceShip1.setOther(self.__spaceShip2)
        self.__spaceShip2.setOther(self.__spaceShip1)

        self.__imageBuffer = self.__loader.atariFrames
        #self.__createLotsOfImages()

        self.__onlyLabel = Label(self.__main, bd=0, bg="black")
        self.__onlyLabel.pack(padx=0, pady=0, fill=BOTH)

        self.__lastX = self.__loader.mainWindow.getScales()[0]
        self.__lastY = self.__loader.mainWindow.getScales()[1]
        self.__sizing = False

        self.__setCurrentImage(0)

        t = Thread(target=self.nextFrame)
        t.daemon=True
        t.start()

        #s = Thread(target=self.resize)
        #s.daemon=True
        #s.start()


    """
    def __createLotsOfImages(self):
        self.__imageBuffer=[]
        self.__sizing = True
        #self.__lastSizeX = self.__main.winfo_height()*round(self.__loader.mainWindow.getScales()[0])
        for num in range(0,19):
            self.__imageBuffer.append(ImageTk.PhotoImage(self.__frames[num].resize((
            self.__main.winfo_height()*round(self.__loader.mainWindow.getScales()[0])
            , self.__main.winfo_height()*round(self.__loader.mainWindow.getScales()[1])
        ), IMAGE.ANTIALIAS)))
        self.__sizing = False
    """

    def __setCurrentImage(self, num):
        try:
            if self.__onlyLabel in self.__main.pack_slaves():
                #if self.__imageBuffer[num].width() != self.__lastSizeX:
                #    self.__createLotsOfImages()

                self.__onlyLabel.config(image=self.__imageBuffer[num])
        except Exception as e:
            self.__loader.logger.errorLog(e)

    def nextFrame(self):
        from time import sleep
        while(self.__loader.mainWindow.dead==False and self.stopThread == False
              and self.__loader.bigFrame.getMode() == "intro"
        ):
            if self.__counter<18:
                self.__counter+=1
            else:
                self.__counter=0
            if self.__sizing == False:
                self.__setCurrentImage(self.__counter)
            sleep(0.02)
    """
    def resize(self):
        from time import sleep
        while(self.__loader.mainWindow.dead==False and self.stopThread == False):
            if (self.__lastX != self.__loader.mainWindow.getScales()[0] and
                self.__lastY != self.__loader.mainWindow.getScales()[1]):
                self.__lastX = self.__loader.mainWindow.getScales()[0]
                self.__lastY = self.__loader.mainWindow.getScales()[1]

                self.__createLotsOfImages()

            sleep(0.04)
    """