from tkinter import Button
from PIL import ImageTk, Image
from threading import Thread

class MenuButton:

    def __init__(self, boss, master, frame, image, XPoz, function):
        self.__boss = boss
        self.__master = master
        self.__frame = frame
        self.__XPoz = XPoz

        self.__contentHolder = self.__frame.getFrame()
        self.__img = ImageTk.PhotoImage(Image.open("others/img/"+image+".png"))
        self.__function = function

        self.__button = Button(self.__contentHolder, width=32, height=32, command=self.__function)
        self.__button.config(image = self.__img)

        self.__lastScaleX = self.__boss.getScales()[0]
        self.__placer()

        align = Thread(target=self.dinamicallyAlign)
        align.start()

    def getButton(self):
        return(self.__button)

    def dinamicallyAlign(self):
        from time import sleep
        while True:
            if (self.__lastScaleX==self.__boss.getScales()[0]):
                sleep(0.05)
                continue
            self.__lastScaleX = self.__boss.getScales()[0]
            self.__placer()

            sleep(0.02)

    def __placer(self):
        self.__button.place(x=(32*self.__XPoz)+
                              (self.__XPoz*10*self.__frame.getFrameSize()[0]/600)+5, y = 5)