from tkinter import *
from PIL import Image as IMAGE, ImageTk
from threading import Thread

class AtariLogo:

    def __init__(self, loader, main, left, right):
        self.__loader = loader
        self.__main = main
        self.__left = left
        self.__right = right


        self.__frames = []
        self.__counter = 0

        for num in range(1, 20):
            num = str(num)
            if len(num) == 1:
                num = "0" + str(num)
            self.__frames.append(IMAGE.open("others/img/logo/"+num+".gif"))

        self.__imageBuffer = []
        self.__createLotsOfImages()

        self.__onlyLabel = Label(self.__main, bd=0, bg="black")
        self.__onlyLabel.pack(padx=0, pady=0)

        self.__lastX = self.__loader.mainWindow.getScales()[0]
        self.__lastY = self.__loader.mainWindow.getScales()[1]
        self.__sizing = False

        self.__setCurrentImage(0)

        t = Thread(target=self.nextFrame)
        t.daemon=True
        t.start()

        s = Thread(target=self.resize)
        s.daemon=True
        s.start()


    def __createLotsOfImages(self):
        self.__imageBuffer=[]
        self.__sizing = True
        for num in range(0,19):
            self.__imageBuffer.append(ImageTk.PhotoImage(self.__frames[num].resize((
            self.__main.winfo_height()*round(self.__loader.mainWindow.getScales()[0])
            , self.__main.winfo_height()*round(self.__loader.mainWindow.getScales()[1])
        ), IMAGE.ANTIALIAS)))
        self.__sizing = False

    def __setCurrentImage(self, num):
        try:
            self.__onlyLabel.config(image=self.__imageBuffer[num])
        except:
            pass

    def nextFrame(self):
        from time import sleep
        while(self.__loader.mainWindow.dead==False):
            if self.__counter<18:
                self.__counter+=1
            else:
                self.__counter=0
            if self.__sizing == False:
                self.__setCurrentImage(self.__counter)
            sleep(0.02)

    def resize(self):
        from time import sleep
        while(self.__loader.mainWindow.dead==False):
            if (self.__lastX != self.__loader.mainWindow.getScales()[0] and
                self.__lastY != self.__loader.mainWindow.getScales()[1]):
                self.__lastX = self.__loader.mainWindow.getScales()[0]
                self.__lastY = self.__loader.mainWindow.getScales()[1]

                self.__createLotsOfImages()

            sleep(0.04)