from tkinter import Button, NORMAL, DISABLED
from PIL import ImageTk, Image
from threading import Thread

class MenuButton:

    def __init__(self, loader, frame, image, XPoz,
                 function, functionEnter, functionLeave, bindedVar,
                 invertedBinding, bindedOut):
        self.__loader = loader
        self.__loader.menuButtons[image] = self

        self.__frame = frame
        self.__XPoz = XPoz
        self.__bindedVar = bindedVar
        self.__invertedBinding = invertedBinding
        self.__bindedOut = bindedOut

        self.__contentHolder = self.__frame.getFrame()
        self.__img = ImageTk.PhotoImage(Image.open("others/img/"+image+".png"))
        self.__function = function
        self.__functionEnter = functionEnter
        self.__functionLeave = functionLeave
        self.preventRun = False

        self.__button = Button(self.__contentHolder, name=image, width=32, height=32, command=self.__function)

        self.__button.bind("<Enter>", self.__functionEnter)
        self.__button.bind("<Leave>", self.__functionLeave)

        self.__button.config(image = self.__img)

        self.__lastScaleX = self.__loader.mainWindow.getScales()[0]
        self.__placer()

        align = Thread(target=self.dinamicallyAlign)
        align.start()

        if (self.__bindedVar != None):
            binder = Thread(target=self.checkBinded)
            binder.daemon = True
            binder.start()

        if (self.__bindedOut !=None):
            bind2 = Thread(target=self.__bindedOut, args=[self])
            bind2.daemon = True
            bind2.start()

    def checkBinded(self):
        from time import sleep
        while True:
            if self.preventRun == False:
                if self.__invertedBinding == False:
                    temp = self.__bindedVar
                else:
                    temp = not self.__bindedVar


                if temp == True:
                    self.__button.config(state=NORMAL)
                else:
                    self.__button.config(state=DISABLED)
            sleep(1)

    def getButton(self):
        return(self.__button)

    def dinamicallyAlign(self):
        from time import sleep
        while True:
            if (self.__lastScaleX==self.__loader.mainWindow.getScales()[0]):
                sleep(0.05)
                continue
            self.__lastScaleX = self.__loader.mainWindow.getScales()[0]
            self.__placer()

            sleep(0.02)

    def __placer(self):
        self.__button.place(x=(32*self.__XPoz)+
                              (self.__XPoz*10*self.__frame.getFrameSize()[0]/600)+5, y = 5)