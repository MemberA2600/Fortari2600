from tkinter import *
from PIL import Image as IMAGE, ImageTk
from threading import Thread

class SpaceShip:
    def __init__(self, loader, frame):
        self.__loader = loader

        self.__frame = frame
        self.__other = None
        self.hasRocket = True
        self.__rocketY = False
        self.__delay = self.__getRandom(0)
        self.__dontDoIt = False

        self.fuckYou = False
        self.stopThread = False
        self.__loader.stopThreads.append(self)

        self.__extraDelay = 0

        #self.__frames = self.__loader.rocketFrames
        self.__imgBuffer = self.__loader.rocketFrames

        self.__lastScaleX = self.__loader.mainWindow.getScales()[0]
        self.__lastScaleY = self.__loader.mainWindow.getScales()[1]

        self.__spaceLabel = Label(self.__frame, bg = "black",
                                  height=self.__frame.winfo_height(), width=self.__frame.winfo_width(), borderwidth = 0, highlightthickness=0)
        #self.__setBuffer()

        self.__spaceLabel.pack_propagate(False)
        self.__spaceLabel.pack(fill=BOTH)
        self.__item1 = None

        self.__loader.threadLooper.addToThreading(self, self.__drawCanvas, [])

        #t = Thread(target=self.__drawCanvas)
        #t.daemon = True
        #t.start()


    def setOther(self, other):
        self.__other = other

    def __getRandom(self, min):
        import random
        return(random.randint(10+min, 200+min))

    def __drawCanvas(self):
        if self.__frame != None and self.__loader.bigFrame.getMode() == "intro":
            try:
                if self.__dontDoIt == True:
                    self.__rocketY += 1
                    if self.__rocketY > 65:
                        self.__rocketY = False
                        self.__dontDoIt = False
                        if self.__other != None:
                            self.__other.fuckYou = False

                        import random
                        if self.__other!=None:
                            self.__extraDelay = random.randint(125, 200)
                        else:
                            self.__delay = random.randint(225, 700)
                        self.__item1 = None

                else:
                    if self.__rocketY == False:
                        self.hasRocket = False

                if self.__delay > 0:
                    self.__delay -= 1

                if self.__extraDelay>0:
                    self.__extraDelay-=1

                if self.__other !=None:
                    if self.hasRocket == False and self.__delay == 0:
                        if self.__other.hasRocket == False and self.fuckYou == False:
                            self.hasRocket = True
                            self.fuckYou = True
                            self.__dontDoIt = True
                            self.__rocketY = 1

                        else:
                            self.__delay = self.__getRandom(self.__extraDelay)
                else:
                    if self.hasRocket == False and self.__delay == 0:
                            self.hasRocket = True
                            self.__dontDoIt = True
                            self.__rocketY = 1

                #if self.__lastSizeX != self.__frame.winfo_width():
                #    self.__setBuffer()
                self.__spaceLabel.config(
                    image=self.__imgBuffer[self.__rocketY]
                )

            except Exception as e:
                self.__loader.logger.errorLog(e)