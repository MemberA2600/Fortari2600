from PIL import ImageTk, Image as IMAGE
from threading import Thread
from tkinter import *
from time import sleep

class ET:

    def __init__(self, window, master, loader, mainBoss):
        self.__window = window
        self.__loader = loader
        self.__master = master
        self.__mainBoss = mainBoss

        self.dead       = False
        self.stopThread = False
        self.__loader.stopThreads.append(self)

        self.__forestFrame = Frame(self.__master.getFrame(), bg = "green", height=10000, width=master.getFrameSize()[0])
        self.__forestFrame.pack_propagate(False)
        self.__forestFrame.grid_propagate(False)
        self.__forestFrame.pack(side=BOTTOM, fill=BOTH, anchor=CENTER)

        self.__forestCanvas = Canvas(self.__forestFrame, bg = "green", height=10000, width=master.getFrameSize()[0])
        self.__forestCanvas.pack_propagate(False)
        self.__forestCanvas.grid_propagate(False)
        self.__forestCanvas.pack(side=BOTTOM, fill=BOTH, anchor=CENTER)

        self.__spriteCounter = 0
        self.__differenceX = 0
        self.__differenceY = 0
        #self.__lastDifferenceX = 9999
        #self.__lastDifferenceY = 9999

        self.__first = True

        self.__etX = 0
        self.__etY = 0

        self.__mirroring = False

        self.__setBuffer()

        forest = Thread(target=self.__forestD)
        forest.daemon = True
        forest.start()

        self.__loader.threadLooper.addToThreading(self, self.drawET, [], 1)

        #draw = Thread(target=self.drawET)
        #draw.daemon = True
        #draw.start()

    def __forestD(self):

        while self.__forestFrame.winfo_width()<2 or self.__forestCanvas.winfo_width() < 2:
           sleep(0.0001)

        """

        while self.__forestImg.height() < 2:
            self.__forest = IMAGE.open("others/img/etForest.png").resize(
                (self.__forestFrame.winfo_width(),
                 self.__forestFrame.winfo_height()
                 ), IMAGE.ANTIALIAS)

            self.__forestImg = ImageTk.PhotoImage(self.__forest)
            sleep(0.0001)
        """

        self.__forest = IMAGE.open("others/img/etForest.png").resize(
            (self.__forestFrame.winfo_width(),
             self.__forestFrame.winfo_height()
             ), IMAGE.ANTIALIAS)
        self.__forestImg = ImageTk.PhotoImage(self.__forest)

        self.__forestOfSteel = self.__forestCanvas.create_image(
            0, 0, image=self.__forestImg, anchor=NW
        )

    def __setBuffer(self):
        t = Thread(target=self.__setBufferThread)
        t.daemon = True
        t.start()

    def __setBufferThread(self):
        self.__imageBufferLeft = []
        self.__imageBufferRight = []

        while self.__forestCanvas.winfo_width() < 2:
            sleep(0.000001)
        self.__scale = self.__forestCanvas.winfo_width()/400

        while len(self.__imageBufferLeft) < 3 or len(self.__imageBufferRight) < 3:
            self.__imageBufferLeft = []
            self.__imageBufferRight = []
            try:
                for num in range(1,4):
                    self.__imageBufferLeft.append(IMAGE.open(str("others/img/et" + str(num) + ".png")).resize((round(self.__scale*17),
                            round(self.__scale*17)),
                           IMAGE.ANTIALIAS))
                    self.__imageBufferRight.append(IMAGE.open(str("others/img/et" + str(num) + ".png")).resize((round(self.__scale*17),
                            round(self.__scale*17)),
                           IMAGE.ANTIALIAS).transpose(IMAGE.FLIP_LEFT_RIGHT))
            except:
                sleep(0.00001)

        self.centerET()

    def drawET(self):
        if self.__master.getFrame().winfo_exists() == False:
           self.stopThread = True
           self.dead       = True

        try:
            moving = self.getDifference()
            if moving == False and self.__first == False:
                if self.__spriteCounter != 0:
                    # print(self.__spriteCounter)
                    self.__spriteCounter = 0
                    self.draw()

            else:
                self.draw()

        except Exception as e:
            self.__loader.logger.errorLog(e)

    def draw(self):
        self.__first = False
        #self.__forestCanvas.clipboard_clear()
        #self.__forestCanvas.delete("all")

        if self.__forestFrame.winfo_width() < 2: self.__forestD()

        self.__forestOfSteel = self.__forestCanvas.create_image(
            0, 0, image=self.__forestImg, anchor=NW
        )

        self.getETSprite(self.__spriteCounter + 1, self.__mirroring)

        self.__et = self.__forestCanvas.create_image(
            self.__etX,
            self.__etY,
            image=self.__spriteImage,
            anchor=NW
        )

    def getDifference(self):
        import mouse
        if self.__window.dead==False and self.stopThread==False:
            try:
                posX =(self.__etX+self.__mainBoss.getTopLevel().winfo_x()+
                                      self.__master.getFrame().winfo_x()+
                                    self.__spriteImage.width() / 2)

                self.__differenceX = mouse.get_position()[0] - posX

                posY =(self.__etY+self.__mainBoss.getTopLevel().winfo_y()+
                                      self.__forestFrame.winfo_y()+
                                      self.__spriteImage.height()/2
                       )

                self.__differenceY = mouse.get_position()[1] - posY

                #print(self.__differenceX, self.__differenceY)

                moving = self.move()

                if (moving == True):
                    if self.__differenceX>0:
                        self.__mirroring = False
                    else:
                        self.__mirroring = True

                    if self.__spriteCounter == 2:
                        self.__spriteCounter = 0
                    else:
                        self.__spriteCounter +=1

                return(moving)
            except Exception as e:
                self.__loader.logger.errorLog(e)


    def move(self):
        moving = False
        speed = self.__spriteImage.width()/8
        if self.__differenceX>10 and self.__etX<(self.__forestFrame.winfo_width()-self.__spriteImage.width()-self.__forestFrame.winfo_width()/15):
            self.__etX += speed
            moving = True
        if self.__differenceX<-10 and self.__etX>self.__forestFrame.winfo_width()/15:
            self.__etX -= speed
            moving = True

        h =  self.__forestFrame.winfo_width()-self.__spriteImage.height()-self.__forestFrame.winfo_height()/1.6
        #print(h, self.__etY)
        if self.__differenceY>10 and self.__etY<h:
            self.__etY += speed
            moving = True
        if self.__differenceY<-10 and self.__etY>self.__forestFrame.winfo_height()/9:
            self.__etY -= speed
            moving = True

        return(moving)




    def centerET(self):
        self.__etX = self.__forestCanvas.winfo_width()/2 - round(self.__scale*17)/2
        self.__etY = self.__forestCanvas.winfo_height()/2 - round(self.__scale*17)


    def getETSprite(self, num, mirror):
        if mirror == False:
            self.__spriteImage = ImageTk.PhotoImage(self.__imageBufferLeft[num-1])
        else:
            self.__spriteImage = ImageTk.PhotoImage(self.__imageBufferRight[num - 1])