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

        self.__extraDelay = 0

        self.__lastScaleX = self.__loader.mainWindow.getScales()[0]
        self.__lastScaleY = self.__loader.mainWindow.getScales()[1]

        self.__spaceCanvas = Canvas(self.__frame, bg = "black", height=self.__frame.winfo_height(), width=self.__frame.winfo_width(), borderwidth = 0, highlightthickness=0)
        self.__spaceCanvas.pack_propagate(False)
        self.__spaceCanvas.grid_propagate(False)
        self.__spaceCanvas.pack(side=BOTTOM, fill=BOTH, anchor=CENTER)

        self.__getSpaceShip()

        t = Thread(target=self.__drawCanvas)
        t.daemon = True
        t.start()

    def __getSpaceShip(self):
        self.__spaceShip = ImageTk.PhotoImage(IMAGE.open(str("others/img/spaceship.png"))
                                              .resize(( round(self.__frame.winfo_width()*0.75) , round(self.__frame.winfo_width()*0.75*3.11)))
                                                )


    def setOther(self, other):
        self.__other = other

    def __getRandom(self, min):
        import random
        return(random.randint(10+min, 200+min))

    def __drawCanvas(self):
        from time import sleep
        self.__item1 = None
        while self.__loader.mainWindow.dead == False and self.__frame!=None:
            try:
                if (self.__lastScaleX != self.__loader.mainWindow.getScales()[0] or
                        self.__lastScaleY != self.__loader.mainWindow.getScales()[1]
                ):
                    self.__item1 = None
                    self.__item2 = None
                    self.__item3 = None
                    self.__spaceCanvas.clipboard_clear()
                    self.__spaceCanvas.delete("all")


                if (self.__lastScaleX != self.__loader.mainWindow.getScales()[0] or
                    self.__lastScaleY != self.__loader.mainWindow.getScales()[1]
                    ) or self.hasRocket == True:

                    self.__lastScaleX = self.__loader.mainWindow.getScales()[0]
                    self.__lastScaleY = self.__loader.mainWindow.getScales()[1]

                    self.__spaceCanvas.config(width=self.__frame.winfo_width(),
                                              height=self.__frame.winfo_height())
                    self.__getSpaceShip()
                    self.__spaceCanvas.clipboard_clear()
                    #self.__spaceCanvas.delete("all")

                    if self.__rocketY !=False:

                        self.__item1 = self.__spaceCanvas.create_image(
                            self.__spaceCanvas.winfo_width() * 0.15,
                            self.__rocketY,
                            image=self.__spaceShip,
                            anchor=NW
                        )

                        try:
                            self.__spaceCanvas.tag_lower(self.__item1)
                            self.__spaceCanvas.tag_lower(self.__item1)
                        except:
                            pass

                    self.__item2 =self.__spaceCanvas.create_rectangle(self.__spaceCanvas.winfo_width()*0.1, (round(self.__spaceCanvas.winfo_height()*0.92)),
                                                        self.__spaceCanvas.winfo_width() * 0.9, self.__spaceCanvas.winfo_height()*0.95,
                                                        fill="gray", outline="")
                    self.__item3 =self.__spaceCanvas.create_rectangle(0, (round(self.__spaceCanvas.winfo_height()*0.95)),
                                                        999999, self.__spaceCanvas.winfo_height(),
                                                        fill="sandy brown", outline="")

                if self.__dontDoIt == True:
                    self.__rocketY = self.__rocketY - round(self.__spaceCanvas.winfo_height() * 0.02)
                    if self.__rocketY < self.__spaceShip.height() * (-1.1):
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
                            self.__rocketY = self.__spaceCanvas.winfo_height()

                        else:
                            self.__delay = self.__getRandom(self.__extraDelay)
                else:
                    if self.hasRocket == False and self.__delay == 0:
                            self.hasRocket = True
                            self.__dontDoIt = True
                            self.__rocketY = self.__spaceCanvas.winfo_height()

                #print(self.__delay, self.hasRocket)
                sleep(0.04)
            except Exception as e:
                self.__loader.logger.errorLog(e)