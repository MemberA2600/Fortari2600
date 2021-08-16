from PIL import ImageTk, Image as thisIsTheImage
from threading import Thread
from tkinter import *

class PitFallHarry:

    def __init__(self, window, master, loader, font):
        self.__window = window
        self.__loader = loader
        self.__master = master
        self.__font = font
        self.setBuffer()

        self.stopThread = False
        self.__loader.stopThreads.append(self)

        self.__bg = "gold"
        self.__spriteNum = 0
        self.__harryFrame = Frame(master.getTopLevel(),
                                  width=master.getTopLevelDimensions()[0], height=10000)
        self.__harryFrame.pack(side=TOP, anchor=N, fill=Y)
        self.__harryFrame.pack_propagate(False)
        self.__harryFrame.config(bg=self.__bg)

        self.__h = self.__harryFrame.winfo_height()
        self.__w = round(self.__h*0.76)

        self.__spriteCounter = 0
        self.__harryPoz = self.__master.getTopLevelDimensions()[0]/2-self.__w/2

        self.__getDifference()

        self.__harryLabel = Label(self.__harryFrame, bg=self.__bg)
        self.__setSprite(1)

        self.__harryMaxX = self.__master.getTopLevelDimensions()[0]-self.__w
        self.__placer()


        m = Thread(target=self.__move)
        m.start()

    def setBuffer(self):
        self.__imageBuffer = []
        for num in range(1,7):
            self.__imageBuffer.append(thisIsTheImage.open(str("others/img/harry" + str(num) + ".png")))

    def __placer(self):
        if self.__window.dead==False and self.stopThread==False:
            try:
                self.__harryLabel.place(x=self.__harryPoz, y=0)
            except Exception as e:
                self.__loader.logger.errorLog(e)


    def __setSprite(self, num):
        if self.__spriteNum != num:
            self.__spriteNum = num
            i = self.__imageBuffer[num-1].resize((self.__w, self.__h), thisIsTheImage.ANTIALIAS)
            if self.__difference>0:
                self.__img = ImageTk.PhotoImage(i.transpose(thisIsTheImage.FLIP_LEFT_RIGHT))
            else:
                self.__img = ImageTk.PhotoImage(i)
            try:
                self.__harryLabel.config(image = self.__img)
            except Exception as e:
                self.__loader.logger.errorLog(e)


    def __getDifference(self):
        import mouse
        if self.__window.dead==False and self.stopThread==False:
            try:
                self.__difference = mouse.get_position()[0] - (self.__w*0.5+self.__harryPoz+self.__master.getTopLevel().winfo_x())
            except Exception as e:
                self.__loader.logger.errorLog(e)


    def __increment(self):
        if self.__spriteCounter>4:
            self.__spriteCounter = 0
        else:
            self.__spriteCounter+=1

    def __harryStop(self):
        self.__setSprite(1)
        self.__spriteCounter = 0

    def __harryMove(self, num):
        self.__setSprite(self.__spriteCounter + 1)
        self.__increment()
        self.__harryPoz += num
        self.__placer()

    def __move(self):
        while self.__window.dead == False and self.stopThread==False:
            from time import sleep

            while self.__harryLabel.winfo_width()==1:
                try:
                    self.__harryLabel.config(width=self.__harryFrame.winfo_height(),
                                             height=round(self.__h * 0.76))

                    self.__harryLabel.place(x=self.__harryPoz, y=0)
                except:
                    pass

            self.__getDifference()
            if abs(self.__difference)<15:
                self.__harryStop()
            elif self.__difference>14:
                if self.__harryPoz<self.__harryMaxX:
                    self.__harryMove(10)
                else:
                    self.__harryStop()
            elif self.__difference<-15:
                if self.__harryPoz>0:
                    self.__harryMove(-10)
                else:
                    self.__harryStop()

            if self.__harryPoz>self.__harryMaxX:
                self.__harryPoz = self.__harryMaxX
            elif self.__harryPoz<0:
                self.__harryPoz = 0


            sleep(0.04)