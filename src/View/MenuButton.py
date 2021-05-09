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
        self.__image=image

        self.stopThread = False
        #self.__loader.stopThreads.append(self)

        self.__contentHolder = self.__frame.getFrame()
        self.__img = self.__loader.io.getImg(self.__image, None)
        self.__function = function
        self.__functionEnter = functionEnter
        self.__functionLeave = functionLeave
        self.preventRun = False

        self.__button = Button(self.__contentHolder, name=image,
                               width=self.__loader.mainWindow.getConstant(),
                               height=self.__loader.mainWindow.getConstant(),
                               command=self.__function,
                               state=DISABLED)

        self.__button.bind("<Enter>", self.__functionEnter)
        self.__button.bind("<Leave>", self.__functionLeave)
        self.__button.config(bg=self.__loader.colorPalettes.getColor("window"))

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

    def __checkIfFalse(self, var):
        if var == False or var == None or var == "":
            return False
        return True

    def checkBinded(self):
        from time import sleep
        while self.__loader.mainWindow.dead==False and self.stopThread==False:
            if self.preventRun == False:
                try:
                    if self.__invertedBinding == True:
                        temp = not self.__checkIfFalse(self.__loader.bindedVariables[self.__bindedVar])
                    else:
                        temp = self.__checkIfFalse(self.__loader.bindedVariables[self.__bindedVar])

                    if temp == True:
                        self.__button.config(state=NORMAL)
                    else:
                        self.__button.config(state=DISABLED)
                except Exception as e:
                    self.__loader.logger.errorLog(e)

            sleep(1)

    def getButton(self):
        return(self.__button)

    def dinamicallyAlign(self):
        from time import sleep
        while self.__loader.mainWindow.dead==False and self.stopThread==False:
            if (self.__lastScaleX==self.__loader.mainWindow.getScales()[0]):
                sleep(0.05)
                continue
            self.__lastScaleX = self.__loader.mainWindow.getScales()[0]
            self.__resizeMe()
            self.__placer()

            sleep(0.02)

    def __resizeMe(self):
        self.__button.config(width=self.__loader.mainWindow.getConstant(),
                             height=self.__loader.mainWindow.getConstant())
        self.__img = self.__loader.io.getImg(self.__image, None)
        self.__button.config(image = self.__img)


    def __placer(self):
        self.__button.place(x=(self.__loader.mainWindow.getConstant()*self.__XPoz)+
                              (self.__XPoz*10*self.__frame.getFrameSize()[0]/600)+5, y = 5)